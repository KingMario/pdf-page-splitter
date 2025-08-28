#!/usr/bin/env python3.11
"""
PDF Page Splitting Utility
Splits each page vertically or horizontally into two, starting from a specified page.
"""

import PyPDF2
import os
import argparse  # Import the argparse module


def parse_pages_string(pages_str):
    """
    Parse a pages string into a set of page numbers.
    
    Args:
        pages_str: String specifying pages (e.g., "1,3-5,7,9-12")
    
    Returns:
        set: Set of page numbers (1-based)
    
    Raises:
        ValueError: If the pages string is invalid
    """
    if not pages_str:
        return set()
    
    pages = set()
    
    try:
        # Split by commas to get individual parts
        parts = [part.strip() for part in pages_str.split(',')]
        
        for part in parts:
            if '-' in part:
                # Handle range (e.g., "3-5")
                start_str, end_str = part.split('-', 1)
                start = int(start_str.strip())
                end = int(end_str.strip())
                
                if start > end:
                    raise ValueError(f"Invalid range: {part} (start > end)")
                if start < 1 or end < 1:
                    raise ValueError(f"Invalid range: {part} (page numbers must be >= 1)")
                
                pages.update(range(start, end + 1))
            else:
                # Handle single page
                page = int(part.strip())
                if page < 1:
                    raise ValueError(f"Invalid page number: {page} (must be >= 1)")
                pages.add(page)
    
    except ValueError as e:
        if "invalid literal for int()" in str(e):
            raise ValueError(f"Invalid pages format: '{pages_str}'. Expected format: '1,3-5,7' or '2-4'")
        raise
    
    return pages


def split_pdf_pages(input_file, output_file, start_page=3, end_page=None, direction="vertical", pages_to_split=None):
    """
    Splits each page of a PDF file into two, starting from a specified page.
    
    Args:
        input_file: Path to the input PDF file
        output_file: Path to the output PDF file
        start_page: Page number to start splitting from (1-based index) - used when pages_to_split is None
        end_page: Page number to end splitting at (1-based index) - used when pages_to_split is None
        direction: Direction to split pages ("vertical" or "horizontal")
        pages_to_split: Set of specific page numbers to split (1-based). If provided, overrides start_page/end_page
    """

    try:
        with open(input_file, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            total_pages = len(reader.pages)
            print(f"Total pages in PDF: {total_pages}")
            
            # Determine which pages to split
            if pages_to_split is not None:
                # Use specific pages
                pages_to_process = pages_to_split
                # Validate that all specified pages exist
                invalid_pages = [p for p in pages_to_process if p > total_pages]
                if invalid_pages:
                    print(f"Warning: Pages {invalid_pages} exceed total page count ({total_pages})")
                    pages_to_process = {p for p in pages_to_process if p <= total_pages}
                
                if pages_to_process:
                    sorted_pages = sorted(pages_to_process)
                    print(f"Splitting specific pages: {sorted_pages}")
                else:
                    print("No valid pages to split")
            else:
                # Use start/end range (original behavior)
                if end_page and end_page < start_page:
                    print(f"Warning: End page ({end_page}) is before start page ({start_page}). No pages will be split.")
                    actual_end_page = start_page - 1  # No pages to split
                else:
                    actual_end_page = min(end_page, total_pages) if end_page else total_pages
                
                print(f"Splitting starts from page {start_page}")
                print(f"Splitting ends at page {actual_end_page}")
                
                pages_to_process = set(range(start_page, actual_end_page + 1))

            # Process all pages in order
            for i in range(1, total_pages + 1):
                page = reader.pages[i - 1]  # Convert to 0-based index for reader
                
                if i in pages_to_process:
                    # Split this page
                    # Get page dimensions
                    media_box = page.mediabox
                    width = float(media_box.width)
                    height = float(media_box.height)

                    print(f"Processing page {i} - Dimensions: {width} x {height}")

                    if direction == "vertical":
                        # Vertical split: Left and Right halves
                        # First half (left)
                        writer.add_page(page)
                        first_half = writer.pages[-1]
                        first_half.cropbox = PyPDF2.generic.RectangleObject([0, 0, width / 2, height])

                        # Second half (right)
                        writer.add_page(page)
                        second_half = writer.pages[-1]
                        second_half.cropbox = PyPDF2.generic.RectangleObject([width / 2, 0, width, height])

                        print(f"Split complete: Page {i} -> Left half + Right half")
                    
                    elif direction == "horizontal":
                        # Horizontal split: Top and Bottom halves
                        # First half (top)
                        writer.add_page(page)
                        first_half = writer.pages[-1]
                        first_half.cropbox = PyPDF2.generic.RectangleObject([0, height / 2, width, height])

                        # Second half (bottom)
                        writer.add_page(page)
                        second_half = writer.pages[-1]
                        second_half.cropbox = PyPDF2.generic.RectangleObject([0, 0, width, height / 2])

                        print(f"Split complete: Page {i} -> Top half + Bottom half")
                else:
                    # Keep this page as is
                    writer.add_page(page)
                    print(f"Keeping page {i} as is")

            # Save the output file
            with open(output_file, "wb") as output:
                writer.write(output)

            print(f"\nSplitting finished!")
            print(f"Input file: {input_file}")
            print(f"Output file: {output_file}")
            print(f"Original page count: {total_pages}")
            
            # Calculate output page count
            split_page_count = len(pages_to_process)
            output_page_count = total_pages + split_page_count  # Original pages + split pages
            print(f"Output page count: {output_page_count}")
            print(f"Pages split: {split_page_count}")

    except Exception as e:
        print(f"An error occurred during processing: {str(e)}")
        import traceback

        traceback.print_exc()
        return False

    return True


def main():
    # --- Parse command-line arguments using argparse ---
    parser = argparse.ArgumentParser(
        description="PDF Page Splitting Utility. Splits each page of a PDF file vertically or horizontally, starting from a specified page.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("input_file", help="Path to the input PDF file to be processed.")
    parser.add_argument(
        "-o",
        "--output",
        help="Path for the output file.\nIf not provided, it will be generated automatically from the input filename (e.g., 'input.pdf' -> 'input - Split.pdf').",
    )
    parser.add_argument(
        "-p",
        "--pages",
        help="Specific pages to split (e.g., '1,3-5,7' or '2-4').\nIf provided, overrides --start and --end options.\nSupports individual pages and ranges separated by commas.",
    )
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        default=3,
        help="The page number to start splitting from (1-based index).\nDefault is 3. Ignored if --pages is specified.",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        help="The page number to end splitting at (1-based index).\nIf not provided, splits until the end of the PDF. Ignored if --pages is specified.",
    )
    parser.add_argument(
        "-d",
        "--direction",
        choices=["vertical", "horizontal"],
        default="vertical",
        help="The direction to split pages.\n'vertical' splits into left and right halves (default).\n'horizontal' splits into top and bottom halves.",
    )
    args = parser.parse_args()

    # --- Set filenames based on arguments ---
    input_file = args.input_file

    if args.output:
        output_file = args.output
    else:
        # Auto-generate output filename if not specified
        base, ext = os.path.splitext(input_file)
        output_file = f"{base} - Split{ext}"

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    # Parse pages parameter if provided
    pages_to_split = None
    if args.pages:
        try:
            pages_to_split = parse_pages_string(args.pages)
            if not pages_to_split:
                print("Error: No valid pages specified.")
                return
        except ValueError as e:
            print(f"Error: {e}")
            return

    print("Starting PDF page splitting...")
    print("=" * 50)

    success = split_pdf_pages(
        input_file, 
        output_file, 
        start_page=args.start, 
        end_page=args.end, 
        direction=args.direction,
        pages_to_split=pages_to_split
    )

    if success:
        print("=" * 50)
        print("Processing complete!")

        # Check if the output file was created successfully
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"Output file size: {file_size:,} bytes")
        else:
            print("Warning: Output file not found.")
    else:
        print("=" * 50)
        print("Processing failed!")


if __name__ == "__main__":
    main()
