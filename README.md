# PDF Merger

A simple Python script that merges all PDF files in a selected folder into a single PDF document.

## Features

- Cross-platform folder selection dialog (Windows, Mac, Linux)
- Automatically orders PDFs by numbers found in filenames
- Excludes previously merged files from subsequent runs
- Shows merge order in output

## Prerequisites

- Python 3.6+
- PyPDF2 library

## Installation

```bash
pip install PyPDF2
```

## Usage

1. Run the script:
```bash
python pdf_merger.py
```

2. Select a folder containing PDF files

3. The script will merge all PDFs and save as `{foldername}_MERGED.pdf`

## How It Works

- PDFs are sorted by the first number found in their filename
- Files without numbers are placed at the end
- Output files contain `_MERGED` identifier to prevent inclusion in future merges
- The merge order is printed to console for verification