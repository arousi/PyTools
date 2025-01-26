# PyTools 🌟
# Useful CLI Scripts Collection



## 📂 Project Structure

```
PyTools/
│
├── main.py                  # Entry point for selecting and running scripts
├── README.md                # Project documentation
├── config.json              # Configuration file
├── exports/                 # Directory for exported files
├── scripts/                 # Directory containing individual scripts
│   ├── img2PDF/             # Folder for the Image to PDF Converter tool
│   │   ├── img2PDF.py       
│   │   ├── reqs.txt         
│   │   ├── installReqs_img2PDF.bat 
│   ├── PDF2Text/            # Text Extraction tool from PDF
│   │   ├── PDF2Text.py      
│   │   ├── reqs.txt         
│   │   ├── installReqs_PDF2Text.bat 
```
## Current Scripts
### **start at `main.py`**
1. Open a terminal in the PyTools directory.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Follow the prompts to select the mode (CLI or GUI) and the tool you want to run.
   - If you select CLI mode, ensure the source file is placed inside the root directory.
   - If you select GUI mode, a file-picker dialog will appear for you to select the source file.

### 1. Main Script `main.py`
   This script provides a user-friendly interface to run the other scripts either in CLI or GUI mode.
- Features:
  
    - Tool Selection: Allows users to select which tool to run.
    
    - Requirement Installation: Installs necessary requirements for the selected tool.
    
    - File Selection: Prompts users to select the file to be processed.

  

### 2. Image to PDF Converter `img2PDF.py`
This script converts images (JPG, PNG) to PDF with ease. 
  
  - Features:
    - Displays images by file type (JPG, PNG) within the same script directory
    - Search for image files with partial or exact names.
    - Name the output PDF and override existing files if needed.
    - Allows you to convert multiple files without the need to re run it

### 3. PDF Text Extraction Script `PDF2Text.py`
   This script extracts text from PDF files, using OCR if necessary, and allows for the exclusion of specific strings from the output. 
- Features:
  
    - Tesseract OCR Installation: Checks for Tesseract OCR installation and provides a link to download it if not installed.
    
    - Filename Sanitization: Sanitizes filenames by removing unnecessary quotes and invalid characters.
    
    - Text Extraction: Extracts text from PDF files using pdfplumber and falls back to OCR using pytesseract if no embedded text is found.
    
    - Directory Listing: Lists files in the script's directory for easy selection.
    
    - Exclusion Filtering: Allows users to specify strings to be excluded from the extracted text.
    
    - Output: Saves the extracted text to a .txt file and opens it automatically.


---

## Installation and Usage

Any executable will be flagged by the antivirus, to stop that i needed to pay a fee for an orgnization providing a key signing service, Thus just "Add Exception" or run `python script-name.py` in your terminal

How to open Terminal?

Go to your downloaded/cloned scripts file, in the top side of the 'File Explorer' write cmd then Enter, do `python script-name.py`

voiala congrats you are now a hacker!
### **Using the Script**
1. Clone the repository:
   ```bash
   git clone https://github.com/arousi/PyTools.git
   ```
2. Double click the `reqs.bat` file:
   ```bash
   python 3.11 and all required libraries for all scripts will be installed
   ```
3. Navigate to /scripts or go to Releases for the noobs <3
4. Run the script within the same directory of the file you want to manipulate, all generated files will be there too



## 🌟 = Gratitude and Love

