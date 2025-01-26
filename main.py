import os
import sys

def display_menu():
    """
    Display the menu of available tools.
    
    :return: Dictionary of tools with their names, script paths, and batch file paths.
    """
    print("\nAvailable Tools:")
    tools = {
        "1": {"name": "Image to PDF Converter", "script": "scripts/img2PDF/img2PDF.py", "bat": "scripts/img2PDF/installReqs_img2PDF.bat"},
        "2": {"name": "PDF to Text Converter", "script": "scripts/PDF2Text/PDF2Text.py", "bat": "scripts/PDF2Text/installReqs_PDF2Text.bat"},
    }

    for key, tool in tools.items():
        print(f"{key}. {tool['name']}")

    return tools

def install_requirements(bat_file):
    """
    Runs the .bat file to install requirements.
    
    :param bat_file: Path to the batch file for installing requirements.
    """
    try:
        print(f"\nInstalling requirements using {bat_file}...")
        result = os.system(f"{bat_file}")
        if result == 0:
            print("Requirements installed successfully!")
        else:
            raise Exception(f"Error occurred while installing requirements. Error code: {result}")
    except Exception as e:
        print(f"Failed to install requirements: {e}")

def run_tool(script_path):
    """
    Executes the main script of a tool.
    
    :param script_path: Path to the main script file.
    """
    if os.path.exists(script_path):
        try:
            print(f"\nRunning tool: {script_path}\n")
            result = os.system(f"{sys.executable} {script_path}")
            if result != 0:
                raise Exception(f"Tool execution failed. Error code: {result}")
        except Exception as e:
            print(f"Failed to run the selected tool: {e}")
    else:
        print(f"\nError: Script not found at {script_path}")

def main():
    """
    Main function to handle user interactions and tool execution.
    """
    try:
        while True:
            print("\nWelcome to PyTools! Your collection of useful scripts.")
            tools = display_menu()
            choice = input("\nEnter the number or name of the tool you want to run (or type 'exit' to quit): ").strip()
            
            if choice.lower() == "exit":
                print("Exiting PyTools. Goodbye!")
                break

            # Match tool by number or name
            selected_tool = next((tool for key, tool in tools.items() if choice in {key, tool['name'].lower()}), None)

            if selected_tool:
                print(f"\nYou selected: {selected_tool['name']}")
                # Install requirements
                install_requirements(selected_tool["bat"])
                # Run the selected tool
                run_tool(selected_tool["script"])
            else:
                print("Invalid selection. Please try again.")
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting PyTools. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
