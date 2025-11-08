# PDF Merger

A simple Python script that merges all PDF files in a selected folder into a single PDF document.

## Download

**Don't want to install Python?** Download the ready-to-use executable for your operating system from the [Releases page](../../releases/latest):
- Windows: `simple-pdf-merger-windows.exe`
- macOS: `simple-pdf-merger-mac`
- Linux: `simple-pdf-merger-linux`

Just download and run - no installation required!

## Features

- Cross-platform folder selection dialog (Windows, Mac, Linux)
- Automatically orders PDFs by numbers found in filenames
- Excludes previously merged files from subsequent runs
- Shows merge order in output

## Prerequisites

- Python 3.6+
- PyPDF2 library
- customtkinter library

## Installation

```bash
pip install PyPDF2 customtkinter
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

## Developer Info

### GitHub Actions Setup

This project uses GitHub Actions to automatically build executables for Windows, macOS, and Linux.

**Workflow file location:** `.github/workflows/build.yml`

The workflow:
- Builds executables on every push to main/master
- Creates GitHub releases with all executables when a version tag is pushed
- Runs on all three platforms simultaneously

### Creating a Release

To create a new release with executables:

1. Commit and push your changes:
```bash
git add .
git commit -m "Your commit message"
git push
```

2. Create and push a version tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

3. GitHub Actions will automatically:
   - Build executables for Windows, macOS, and Linux
   - Create a new release on GitHub
   - Attach all three executables to the release

4. View your release at: `https://github.com/YOUR_USERNAME/YOUR_REPO/releases`

**Tag naming convention:** Use semantic versioning (e.g., `v1.0.0`, `v1.1.0`, `v2.0.0`)