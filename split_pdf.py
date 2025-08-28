#!/usr/bin/env python3.11
"""
PDF Page Splitting Utility
Splits each page vertically or horizontally into two, starting from a specified page.
"""

import PyPDF2
import os
import argparse  # Import the argparse module


def split_pdf_pages(input_file, output_file, start_page=3, end_page=None, direction="vertical"):
    """
    Splits each page of a PDF file into two, starting from a specified page.
    
    Args:
        input_file: Path to the input PDF file
        output_file: Path to the output PDF file
        start_page: Page number to start splitting from (1-based index)
        end_page: Page number to end splitting at (1-based index)
        direction: Direction to split pages ("vertical" or "horizontal")
    """

    try:
        with open(input_file, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            total_pages = len(reader.pages)
            print(f"Total pages in PDF: {total_pages}")
            
            # Validate parameters
            if end_page and end_page < start_page:
                print(f"Warning: End page ({end_page}) is before start page ({start_page}). No pages will be split.")
                actual_end_page = start_page - 1  # No pages to split
            else:
                actual_end_page = min(end_page, total_pages) if end_page else total_pages
            
            print(f"Splitting starts from page {start_page}")
            print(f"Splitting ends at page {actual_end_page}")

            # Add pages before the starting page without modification
            for i in range(min(start_page - 1, total_pages)):
                writer.add_page(reader.pages[i])
                print(f"Keeping page {i+1} as is")

            # Process pages that need to be split
            for i in range(start_page - 1, actual_end_page):
                page = reader.pages[i]

                # Get page dimensions
                media_box = page.mediabox
                width = float(media_box.width)
                height = float(media_box.height)

                print(f"Processing page {i+1} - Dimensions: {width} x {height}")

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

                    print(f"Split complete: Page {i+1} -> Left half + Right half")
                
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

                    print(f"Split complete: Page {i+1} -> Top half + Bottom half")

            # Add pages after the end page without modification
            for i in range(actual_end_page, total_pages):
                writer.add_page(reader.pages[i])
                print(f"Keeping page {i+1} as is (after end page)")

            # Save the output file
            with open(output_file, "wb") as output:
                writer.write(output)

            print(f"\nSplitting finished!")
            print(f"Input file: {input_file}")
            print(f"Output file: {output_file}")
            print(f"Original page count: {total_pages}")
            
            # Calculate output page count: unchanged pages + split pages + pages after end
            unchanged_before = start_page - 1
            split_pages = actual_end_page - start_page + 1
            unchanged_after = total_pages - actual_end_page
            output_page_count = unchanged_before + (split_pages * 2) + unchanged_after
            print(f"Output page count: {output_page_count}")
            print(f"Pages split: {split_pages} (pages {start_page} to {actual_end_page})")

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
        "-s",
        "--start",
        type=int,
        default=3,
        help="The page number to start splitting from (1-based index).\nDefault is 3.",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        help="The page number to end splitting at (1-based index).\nIf not provided, splits until the end of the PDF.",
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

    print("Starting PDF page splitting...")
    print("=" * 50)

    success = split_pdf_pages(input_file, output_file, start_page=args.start, end_page=args.end, direction=args.direction)

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
