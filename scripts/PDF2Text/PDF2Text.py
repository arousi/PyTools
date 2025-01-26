import os
import sys
import re
from pathlib import Path
import pdfplumber
from pdf2image import convert_from_path
from pytesseract import image_to_string
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

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

def get_exclusions_gui():
    exclusions = []
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Exclusions", "Enter strings to exclude from the extracted text (comma-separated):")
    exclusion_input = simpledialog.askstring("Exclude", "Enter strings to exclude (comma-separated):")
    if exclusion_input:
        exclusions = [ex.strip() for ex in exclusion_input.split(',')]
    return exclusions

def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python PDF2Text.py <mode> [--export_path=<path>]")
            sys.exit(1)

        mode = sys.argv[1].strip().lower()
        export_path = Path(__file__).resolve().parents[1] / "exports"

        for arg in sys.argv[2:]:
            if arg.startswith("--export_path="):
                export_path = Path(arg.split("=", 1)[1])
                break

        if not export_path.exists():
            export_path.mkdir(parents=True, exist_ok=True)

        if mode == "cli":
            script_directory = Path(__file__).resolve().parents[2]
            list_files_in_directory(script_directory)
            print("\nPlease place the PDF file to be converted in the script's directory.")
            print("Accepted file extensions: .pdf")
            pdf_name = input("Enter the name of the PDF file (with extension): ").strip()
            pdf_path = script_directory / pdf_name

            if not pdf_path.exists():
                print(f"Error: PDF file not found at {pdf_path}")
                sys.exit(1)

        elif mode == "gui":
            pdf_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
            if not pdf_path:
                print("No file selected. Exiting.")
                sys.exit(1)

            if not os.path.exists(pdf_path):
                print(f"Error: PDF file not found at {pdf_path}")
                sys.exit(1)

        else:
            print("Invalid mode. Use 'cli' or 'gui'.")
            sys.exit(1)

        text = extract_text_from_pdf(pdf_path)
        while True:

            if mode == "cli":
                exclusions = []
                print("\nEnter strings to exclude from the extracted text (comma-separated):")
                exclusion_input = input("Exclude: ").strip()
                if exclusion_input:
                    exclusions = [ex.strip() for ex in exclusion_input.split(',')]
            else:
                exclusions = get_exclusions_gui()

            text = filter_excluded_strings(text, exclusions)

            output_name = sanitize_filename(Path(pdf_path).stem) + ".txt"
            output_path = export_path / output_name
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(text)

            print(f"Extraction complete. Text saved to '{output_path}'.")

            if sys.platform == "win32":
                os.startfile(output_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", output_path])
            else:
                subprocess.call(["xdg-open", output_path])

            if mode == "cli":
                print("\nWould you like to reprocess the same file with additional exclusions? Type 'yes' to reprocess or 'no' to exit:")
                if input().strip().lower() != "yes":
                    break
            else:
                if not messagebox.askyesno("Reprocess", "Would you like to reprocess the same file with additional exclusions?\n\nClick 'Yes' to reprocess or 'No' to exit."):
                    break

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()