# PDF Page Splitter

A Python utility that splits PDF pages vertically or horizontally, starting from a specified page number. This tool is useful for processing scanned documents or PDFs where you want to separate content that spans across pages horizontally or vertically.

## Features

- **Vertical and Horizontal Page Splitting**: Splits each page vertically into left and right halves, or horizontally into top and bottom halves
- **Flexible Page Selection**: Choose specific pages to split using individual pages (e.g., "1,3,5"), ranges (e.g., "2-4"), or mixed formats (e.g., "1,3-5,7")
- **Range-based Processing**: Alternatively, choose which page to start splitting from (default: page 3) and optionally which page to end at
- **Preserve Unselected Pages**: Pages not specified for splitting remain unchanged
- **Automatic Output Naming**: Generates output filename automatically if not specified
- **Command-line Interface**: Easy-to-use CLI with helpful arguments
- **Error Handling**: Robust error handling with detailed feedback

## Requirements

- Python 3.11+
- PyPDF2 library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/KingMario/pdf-page-splitter.git
cd pdf-page-splitter
```

2. Install the required dependency:
```bash
pip install PyPDF2
```

## Usage

### Basic Usage

Split a PDF starting from page 3 (default):
```bash
python split_pdf.py input.pdf
```

### Advanced Usage

Specify a custom output file:
```bash
python split_pdf.py input.pdf -o output.pdf
```

Start splitting from a different page:
```bash
python split_pdf.py input.pdf -s 5
```

End splitting at a specific page:
```bash
python split_pdf.py input.pdf -e 7
```

Split only pages 2 through 4:
```bash
python split_pdf.py input.pdf -s 2 -e 4
```

Split pages horizontally (top and bottom halves):
```bash
python split_pdf.py input.pdf -d horizontal
```

Split pages vertically (left and right halves - default):
```bash
python split_pdf.py input.pdf -d vertical
```

Combine options:
```bash
python split_pdf.py input.pdf -o my_split_document.pdf -s 2 -e 6 -d horizontal
```

Split specific pages using the flexible pages parameter:
```bash
python split_pdf.py input.pdf -p "1,3,5"
```

Split page ranges:
```bash
python split_pdf.py input.pdf -p "2-4"
```

Split mixed pages and ranges:
```bash
python split_pdf.py input.pdf -p "1,3-5,7" -d horizontal
```

### Command-line Arguments

- `input_file` (required): Path to the input PDF file to be processed
- `-o, --output` (optional): Path for the output file. If not provided, automatically generates filename (e.g., 'input.pdf' → 'input - Split.pdf')
- `-p, --pages` (optional): Specific pages to split (e.g., '1,3-5,7' or '2-4'). If provided, overrides --start and --end options. Supports individual pages and ranges separated by commas
- `-s, --start` (optional): The page number to start splitting from (1-based index). Default is 3. Ignored if --pages is specified
- `-e, --end` (optional): The page number to end splitting at (1-based index). If not provided, splits until the end of the PDF. Ignored if --pages is specified
- `-d, --direction` (optional): The direction to split pages. Choices are 'vertical' (default) or 'horizontal'. 'vertical' splits into left and right halves, 'horizontal' splits into top and bottom halves

### Help

View all available options:
```bash
python split_pdf.py --help
```

## How It Works

1. **Input Processing**: The tool reads the specified PDF file using PyPDF2
2. **Page Preservation**: Pages before the starting page are copied unchanged to the output
3. **Page Splitting**: From the starting page to the ending page (or end of PDF if not specified), each page is split according to the specified direction:
   - **Vertical** (default): Left half and right half
   - **Horizontal**: Top half and bottom half
4. **Page Preservation**: Pages after the ending page (if specified) are copied unchanged to the output
5. **Output Generation**: Creates a new PDF with the processed pages

## Example Output

### Example 1: Default behavior (vertical split, start page 3, no end page)
For a 5-page PDF with vertical splitting starting from page 3:
- Pages 1-2: Remain unchanged
- Page 3: Becomes pages 3 (left half) and 4 (right half)
- Page 4: Becomes pages 5 (left half) and 6 (right half)
- Page 5: Becomes pages 7 (left half) and 8 (right half)

Total output: 8 pages (2 unchanged + 6 split pages)

### Example 2: Horizontal split (start page 3, end page 4)
For a 5-page PDF with horizontal splitting from page 3 to page 4:
- Pages 1-2: Remain unchanged
- Page 3: Becomes pages 3 (top half) and 4 (bottom half)
- Page 4: Becomes pages 5 (top half) and 6 (bottom half)
- Page 5: Remains unchanged as page 7

Total output: 7 pages (2 unchanged before + 4 split pages + 1 unchanged after)

### Example 3: With end page specified (vertical split, start page 3, end page 4)
For a 5-page PDF with vertical splitting from page 3 to page 4:
- Pages 1-2: Remain unchanged
- Page 3: Becomes pages 3 (left half) and 4 (right half)
- Page 4: Becomes pages 5 (left half) and 6 (right half)
- Page 5: Remains unchanged as page 7

Total output: 7 pages (2 unchanged before + 4 split pages + 1 unchanged after)

### Example 4: Using flexible pages parameter (specific pages: 1,3,5)
For a 5-page PDF with vertical splitting of pages 1, 3, and 5:
- Page 1: Becomes pages 1 (left half) and 2 (right half)
- Page 2: Remains unchanged as page 3
- Page 3: Becomes pages 4 (left half) and 5 (right half)
- Page 4: Remains unchanged as page 6
- Page 5: Becomes pages 7 (left half) and 8 (right half)

Total output: 8 pages (original 5 pages + 3 additional split pages)

### Example 5: Using flexible pages parameter with ranges (pages: 2-4)
For a 5-page PDF with horizontal splitting of pages 2 through 4:
- Page 1: Remains unchanged as page 1
- Page 2: Becomes pages 2 (top half) and 3 (bottom half)
- Page 3: Becomes pages 4 (top half) and 5 (bottom half)
- Page 4: Becomes pages 6 (top half) and 7 (bottom half)
- Page 5: Remains unchanged as page 8

Total output: 8 pages (2 unchanged + 6 split pages)

## Error Handling

The tool includes comprehensive error handling for:
- Missing input files
- Invalid PDF files
- File permission issues
- Processing errors

## AI Attribution

**Note**: This script was entirely written by AI (Artificial Intelligence). The code was generated to provide a functional PDF page splitting utility with a clean command-line interface.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.