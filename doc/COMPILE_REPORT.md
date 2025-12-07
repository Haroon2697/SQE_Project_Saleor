# How to Compile the LaTeX Report

## Prerequisites

Install LaTeX distribution:
- **Ubuntu/Debian:** `sudo apt-get install texlive-full`
- **macOS:** `brew install --cask mactex`
- **Windows:** Install MiKTeX or TeX Live

## Compilation Steps

### Option 1: Using pdflatex (Recommended)

```bash
cd /home/haroon/SQE/SQE_Project_Saleor/doc
pdflatex PROJECT_REPORT_MAIN.tex
pdflatex PROJECT_REPORT_MAIN.tex  # Run twice for references
```

### Option 2: Using latexmk (Automatic)

```bash
cd /home/haroon/SQE/SQE_Project_Saleor/doc
latexmk -pdf PROJECT_REPORT_MAIN.tex
```

## Output

The compiled PDF will be: `PROJECT_REPORT_MAIN.pdf`

## Troubleshooting

### Missing Packages

If you get package errors, install missing packages:
```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-extra texlive-fonts-recommended

# Or use tlmgr (TeX Live Manager)
sudo tlmgr install <package-name>
```

### Common Issues

1. **"File ended while scanning"** - Check for unmatched braces in content file
2. **"Undefined control sequence"** - Missing package, add `\usepackage{package}`
3. **"Missing \begin{document}"** - Check main file structure

## File Structure

- `PROJECT_REPORT_MAIN.tex` - Main document with preamble and structure
- `PROJECT_REPORT_CONTENT.tex` - All content sections (included by main file)

## Notes

- Run pdflatex twice to resolve all cross-references
- Check `.log` file for detailed error messages
- Tables may need multiple compilation passes

