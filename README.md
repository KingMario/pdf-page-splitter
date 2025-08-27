# PDF Page Splitter

A Python utility that splits PDF pages vertically, starting from a specified page number. This tool is useful for processing scanned documents or PDFs where you want to separate content that spans across pages horizontally.

## Features

- **Vertical Page Splitting**: Splits each page vertically into left and right halves
- **Selective Processing**: Choose which page to start splitting from (default: page 3)
- **Preserve Early Pages**: Pages before the starting page remain unchanged
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

Combine options:
```bash
python split_pdf.py input.pdf -o my_split_document.pdf -s 2
```

### Command-line Arguments

- `input_file` (required): Path to the input PDF file to be processed
- `-o, --output` (optional): Path for the output file. If not provided, automatically generates filename (e.g., 'input.pdf' → 'input - Split.pdf')
- `-s, --start` (optional): The page number to start splitting from (1-based index). Default is 3

### Help

View all available options:
```bash
python split_pdf.py --help
```

## How It Works

1. **Input Processing**: The tool reads the specified PDF file using PyPDF2
2. **Page Preservation**: Pages before the starting page are copied unchanged to the output
3. **Page Splitting**: From the starting page onwards, each page is split vertically:
   - Left half: Contains the left portion of the original page
   - Right half: Contains the right portion of the original page
4. **Output Generation**: Creates a new PDF with the processed pages

## Example Output

For a 5-page PDF with splitting starting from page 3:
- Pages 1-2: Remain unchanged
- Page 3: Becomes pages 3 (left half) and 4 (right half)
- Page 4: Becomes pages 5 (left half) and 6 (right half)
- Page 5: Becomes pages 7 (left half) and 8 (right half)

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