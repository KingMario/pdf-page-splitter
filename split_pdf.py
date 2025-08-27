#!/usr/bin/env python3.11
"""
PDF Page Splitting Utility
Splits each page vertically into two, starting from a specified page.
"""

import PyPDF2
import os
import argparse  # Import the argparse module


def split_pdf_pages(input_file, output_file, start_page=3):
    """
    Splits each page of a PDF file vertically into two, starting from a specified page.
    """

    try:
        with open(input_file, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            total_pages = len(reader.pages)
            print(f"Total pages in PDF: {total_pages}")
            print(f"Splitting starts from page {start_page}")

            # Add pages before the starting page without modification
            for i in range(min(start_page - 1, total_pages)):
                writer.add_page(reader.pages[i])
                print(f"Keeping page {i+1} as is")

            # Process pages that need to be split
            for i in range(start_page - 1, total_pages):
                page = reader.pages[i]

                # Get page dimensions
                media_box = page.mediabox
                width = float(media_box.width)
                height = float(media_box.height)

                print(f"Processing page {i+1} - Dimensions: {width} x {height}")

                # Left half
                writer.add_page(page)
                left_page = writer.pages[-1]
                # Set cropbox directly (compatible with PyPDF2 v3.0+)
                left_page.cropbox = [0, 0, width / 2, height]

                # Right half
                writer.add_page(page)
                right_page = writer.pages[-1]
                # Set cropbox directly (compatible with PyPDF2 v3.0+)
                right_page.cropbox = [width / 2, 0, width, height]

                print(f"Split complete: Page {i+1} -> Left half + Right half")

            # Save the output file
            with open(output_file, "wb") as output:
                writer.write(output)

            print(f"\nSplitting finished!")
            print(f"Input file: {input_file}")
            print(f"Output file: {output_file}")
            print(f"Original page count: {total_pages}")
            print(f"Output page count: {(start_page - 1) + (total_pages - start_page + 1) * 2}")

    except Exception as e:
        print(f"An error occurred during processing: {str(e)}")
        import traceback

        traceback.print_exc()
        return False

    return True


def main():
    # --- Parse command-line arguments using argparse ---
    parser = argparse.ArgumentParser(
        description="PDF Page Splitting Utility. Splits each page of a PDF file vertically, starting from a specified page.",
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

    success = split_pdf_pages(input_file, output_file, start_page=args.start)

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
