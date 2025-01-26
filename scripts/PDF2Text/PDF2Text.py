import os
import sys
import re
from pathlib import Path
import pdfplumber
from pdf2image import convert_from_path
from pytesseract import image_to_string

def sanitize_filename(filename):
    """Sanitize the filename by stripping unnecessary quotes and invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename.strip("\"' "))

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file, using OCR if necessary."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        
        if not text.strip():
            print("No embedded text found. Using OCR...")
            images = convert_from_path(pdf_path)
            for image in images:
                text += image_to_string(image, lang="eng+ara") + "\n"
    except Exception as e:
        raise RuntimeError(f"Error while processing PDF: {e}")

    return text

def list_files_in_directory(directory):
    """Display files in the script's directory."""
    print("\nFiles in the script's directory:")
    for file in directory.iterdir():
        print(f"  - {file.name}")

def filter_excluded_strings(text, exclusions):
    """Remove excluded strings from text."""
    for exclusion in exclusions:
        text = text.replace(exclusion, "")
    return text

def main():
    try:
        if len(sys.argv) < 3:
            print("Usage: python PDF2Text.py <mode> <pdf_path> [--export_path=<path>]")
            sys.exit(1)

        mode = sys.argv[1].strip().lower()
        pdf_path = sys.argv[2]
        export_path = Path("exports")

        for arg in sys.argv[3:]:
            if arg.startswith("--export_path="):
                export_path = Path(arg.split("=", 1)[1])
                break

        if not export_path.exists():
            export_path.mkdir(parents=True, exist_ok=True)

        if mode == "cli":
            script_directory = Path(__file__).parent.parent.parent
            list_files_in_directory(script_directory)

            if not os.path.exists(pdf_path):
                print(f"Error: PDF file not found at {pdf_path}")
                sys.exit(1)

        elif mode == "gui":
            if not os.path.exists(pdf_path):
                print(f"Error: PDF file not found at {pdf_path}")
                sys.exit(1)

        else:
            print("Invalid mode. Use 'cli' or 'gui'.")
            sys.exit(1)

        while True:
            text = extract_text_from_pdf(pdf_path)

            exclusions = []
            print("\nEnter strings to exclude from the extracted text (type 'DONE' when finished):")
            while True:
                exclusion = input("Exclude: ").strip()
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

            text = filter_excluded_strings(text, exclusions)

            output_name = sanitize_filename(Path(pdf_path).stem) + ".txt"
            output_path = export_path / output_name
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(text)

            print(f"Extraction complete. Text saved to '{output_path}'.")

            os.startfile(output_path)

            print("\nWould you like to reprocess the same file with additional exclusions? (yes/no):")
            if input().strip().lower() != "yes":
                break

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()