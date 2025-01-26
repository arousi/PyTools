import os
from difflib import get_close_matches
from PIL import Image, UnidentifiedImageError
from reportlab.pdfgen import canvas


def list_directory_contents(directory: str = ".") -> None:
    """
    List all contents of the directory.
    """
    print("\nCurrent Directory Contents:")
    try:
        files = os.listdir(directory)
        for file in files:
            print(file)
    except OSError as e:
        print(f"Error accessing directory: {e}")


def list_images_with_extensions(directory: str = ".") -> list:
    """
    Lists images with extensions grouped together.
    """
    supported_extensions = {'.jpg', '.jpeg', '.png'}
    images = {}

    try:
        for file in os.listdir(directory):
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_extensions:
                images.setdefault(ext, []).append(file)

        print("\nImages Grouped by Extension:")
        for ext, files in images.items():
            print(f"{ext.upper()} Files:")
            for img in files:
                print(f"  - {img}")

        # Flatten the list of images
        return [img for img_list in images.values() for img in img_list]
    except OSError as e:
        print(f"Error accessing directory: {e}")
        return []


def find_closest_match(image_name: str, images: list) -> str:
    """
    Finds the closest match for the given image name from the list of images.
    """
    matches = get_close_matches(image_name.lower(), [img.lower() for img in images])
    if matches:
        return next(img for img in images if img.lower() == matches[0])
    return None


def validate_image(image_path: str) -> bool:
    """
    Validates if the image file can be opened by Pillow.
    """
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except UnidentifiedImageError:
        print(f"Invalid or corrupted image file: {image_path}")
        return False
    except Exception as e:
        print(f"Error validating image: {e}")
        return False


def convert_image_to_pdf(image_path: str, output_path: str) -> None:
    """
    Converts an image to a PDF document, setting metadata for the browser to display the file name.
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            c = canvas.Canvas(output_path, pagesize=(width, height))
            c.setTitle(os.path.basename(output_path))  # Set PDF title to display in browser
            c.drawImage(image_path, 0, 0, width, height)
            c.save()
        print(f"Successfully saved PDF: {output_path}")
    except Exception as e:
        print(f"Error converting image to PDF: {e}")


def main():
    """
    Main function to handle the workflow.
    """
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
            output_pdf_path = f"{output_pdf_name}.pdf"

            # Check if file exists
            if os.path.exists(output_pdf_path):
                overwrite = input(f"The file '{output_pdf_path}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
                if overwrite == 'y':
                    break
                elif overwrite == 'n':
                    print("Choose a different name.")
                else:
                    print("Invalid input. Please type 'y' or 'n'.")
            else:
                break

        # Step 5: Convert Image to PDF
        print(f"Converting '{closest_match}' to PDF...")
        convert_image_to_pdf(closest_match, output_pdf_path)


if __name__ == "__main__":
    main()
