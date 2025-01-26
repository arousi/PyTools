import os
import sys
from pathlib import Path
from tkinter import filedialog
from PIL import Image
import re

def list_directory_contents():
    """List all contents of the current directory."""
    print("\nDirectory contents:")
    for item in os.listdir():
        print(f"  - {item}")

def list_images_with_extensions():
    """List images grouped by extensions."""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    images = [file for file in os.listdir() if os.path.splitext(file)[1].lower() in image_extensions]
    return images

def find_closest_match(image_name, images):
    """Find the closest match for the image name."""
    from difflib import get_close_matches
    matches = get_close_matches(image_name, images)
    return matches[0] if matches else None

def validate_image(image_path):
    """Validate if the file is a valid image."""
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def sanitize_filename(filename):
    """Sanitize the filename by stripping unnecessary quotes and invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename.strip("\"' "))

def main():
    """
    Main function to handle the workflow.
    """
    try:
        if len(sys.argv) < 2:
            print("Usage: python img2PDF.py <mode> [--export_path=<path>]")
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
            list_directory_contents()
            print("\nPlease place the image file to be converted in the script's directory.")
            print("Accepted file extensions: .jpg, .jpeg, .png, .bmp, .gif")
            image_name = input("Enter the name of the image file (with extension): ").strip()
            image_path = script_directory / image_name

            if not image_path.exists():
                print(f"Error: Image file not found at {image_path}")
                sys.exit(1)

            while True:
                # Step 1: List All Directory Contents
                list_directory_contents()

                # Step 2: List Images Grouped by Extensions
                images = list_images_with_extensions()
                if not images:
                    print("\nNo image files found in the current directory.")
                    return

                # Step 3: Ask User for the Image Name
                while True:
                    image_name = input("\nEnter the name of the image you want to convert to PDF (or type 'exit' to quit): ").strip()
                    if image_name.lower() == 'exit':
                        print("Exiting program. Goodbye!")
                        return

                    closest_match = find_closest_match(image_name, images)
                    if closest_match:
                        print(f"Closest match found: {closest_match}")
                        break
                    else:
                        print("No matching image found. Please try again.")

                # Validate the selected image
                if not validate_image(closest_match):
                    print(f"The file '{closest_match}' is not a valid image. Please try another file.")
                    continue

                # Step 4: Ask User for the PDF Name
                while True:
                    output_pdf_name = input("Enter the name for the output PDF file (without extension): ").strip()
                    output_pdf_path = export_path / f"{output_pdf_name}.pdf"

                    # Check if file exists
                    if output_pdf_path.exists():
                        overwrite = input(f"The file '{output_pdf_path}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
                        if overwrite == 'y':
                            break
                        elif overwrite == 'n':
                            print("Choose a different name.")
                        else:
                            print("Invalid input. Please enter 'y' or 'n'.")
                    else:
                        break

                # Convert image to PDF
                try:
                    with Image.open(closest_match) as img:
                        img.save(output_pdf_path, "PDF", resolution=100.0)
                    print(f"Image '{closest_match}' has been converted to PDF and saved as '{output_pdf_path}'.")
                except Exception as e:
                    print(f"Failed to convert image to PDF: {e}")

        elif mode == "gui":
            image_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
            if not image_path:
                print("No file selected. Exiting.")
                sys.exit(1)

            if not os.path.exists(image_path):
                print(f"Error: Image file not found at {image_path}")
                sys.exit(1)

            # Validate the selected image
            if not validate_image(image_path):
                print(f"The file '{image_path}' is not a valid image. Exiting.")
                sys.exit(1)

            # Convert image to PDF
            try:
                output_pdf_name = sanitize_filename(Path(image_path).stem) + ".pdf"
                output_pdf_path = export_path / output_pdf_name
                with Image.open(image_path) as img:
                    img.save(output_pdf_path, "PDF", resolution=100.0)
                print(f"Image '{image_path}' has been converted to PDF and saved as '{output_pdf_path}'.")
            except Exception as e:
                print(f"Failed to convert image to PDF: {e}")

        else:
            print("Invalid mode. Use 'cli' or 'gui'.")
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()