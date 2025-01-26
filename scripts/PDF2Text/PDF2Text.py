import os
import sys
import subprocess
import re
import shutil
from pathlib import Path
import webbrowser

# Tesseract installer link
TESSERACT_INSTALLER_LINK = "https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe"

# Required packages
required_packages = ["pdfplumber", "pdf2image", "Pillow", "pytesseract"]

# Ensure required libraries are installed
def install_packages():
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing missing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure Tesseract OCR is installed
def check_and_install_tesseract():
    if not shutil.which("tesseract"):
        print("Tesseract OCR is not installed.")
        print(f"Opening the Tesseract OCR installer link: {TESSERACT_INSTALLER_LINK}")
        webbrowser.open(TESSERACT_INSTALLER_LINK)
        input("Please install Tesseract OCR and press Enter to continue...")
    else:
        print("Tesseract OCR is already installed.")

# Sanitize the filename by stripping unnecessary quotes and invalid characters
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename.strip("\"' "))

# Extract text from a PDF file, using OCR if necessary
def extract_text_from_pdf(pdf_path):
    import pdfplumber
    from pdf2image import convert_from_path
    from pytesseract import image_to_string

    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        # If no text was extracted, fall back to OCR
        if not text.strip():
            print("No embedded text found. Using OCR...")
            images = convert_from_path(pdf_path)
            for image in images:
                text += image_to_string(image, lang="eng+ara") + "\n"

    except Exception as e:
        raise RuntimeError(f"Error while processing PDF: {e}")

    return text

# Display files in the script's directory
def list_files_in_directory(directory):
    print("\nFiles in the script's directory:")
    for file in directory.iterdir():
        print(f"  - {file.name}")

# Remove excluded strings from text
def filter_excluded_strings(text, exclusions):
    for exclusion in exclusions:
        text = text.replace(exclusion, "")
    return text

# Main function
def main():
    try:
        # Install required libraries
        print("Checking and installing required libraries...")
        install_packages()

        # Get the script directory
        script_directory = Path(__file__).parent

        while True:
            # List files in the directory
            list_files_in_directory(script_directory)

            # Ask for the PDF file name
            print("\nEnter the name of the PDF file (from the list above) or type 'exit' to quit:")
            pdf_name = sanitize_filename(input().strip())

            # Exit condition
            if pdf_name.lower() == "exit":
                print("Exiting the program. Goodbye!")
                break

            # Ensure file exists in the script's directory
            pdf_path = script_directory / pdf_name

            # Add ".pdf" suffix if not present
            if not pdf_path.suffix.lower() == ".pdf":
                pdf_path = pdf_path.with_suffix(".pdf")

            if not pdf_path.exists():
                print(f"The file '{pdf_name}' does not exist in the script's directory. Try again.")
                continue

            print(f"Processing file: {pdf_path.name}...")

            exclusions = []
            while True:
                print("\nPlease input a string to be excluded from the output in this format: \"not wanted string\".")
                print("Type 'DONE' to finish entering exclusions.")
                exclusion = input("String to exclude: ").strip()

                if exclusion.lower() == "done":
                    if not exclusions:
                        print("No exclusions provided. Proceeding without exclusions.")
                    break

                if exclusion.startswith('"') and exclusion.endswith('"'):
                    exclusions.append(exclusion.strip('"'))
                elif exclusion:
                    print(f"Invalid format! Make sure the string is enclosed in double quotes.")
                else:
                    print("Empty input detected. Please enter a valid string or type 'DONE'.")

            print("Processing PDF with exclusions applied...")
            try:
                # Extract text
                text = extract_text_from_pdf(pdf_path)

                # Apply exclusions
                text = filter_excluded_strings(text, exclusions)

                # Export to .txt
                output_name = pdf_path.stem + ".txt"
                output_path = script_directory / output_name
                with open(output_path, "w", encoding="utf-8") as output_file:
                    output_file.write(text)

                print(f"Extraction complete. Text saved to '{output_path}'.")

                # Open the output file
                os.startfile(output_path)

                # Ask if the user wants to reprocess with new exclusions
                print("\nWould you like to reprocess the same file with additional exclusions? (yes/no):")
                if input().strip().lower() != "yes":
                    break
            except Exception as e:
                print(f"An error occurred while processing the file: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
