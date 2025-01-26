import os
import sys
import json
import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess

EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {"is_new_user": 1}

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

def display_menu():
    tools = {
        "1": {"name": "Image to PDF Converter", "script": "scripts/img2PDF/img2PDF.py", "bat": "scripts/img2PDF/installReqs_img2PDF.bat", "filetypes": [("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]},
        "2": {"name": "PDF to Text Converter", "script": "scripts/PDF2Text/PDF2Text.py", "bat": "scripts/PDF2Text/installReqs_PDF2Text.bat", "filetypes": [("PDF files", "*.pdf")]},
    }
    return tools

def install_requirements(bat_file):
    try:
        bat_file_path = os.path.abspath(bat_file)
        print(f"\nInstalling requirements using {bat_file_path}...")
        result = subprocess.run(bat_file_path, shell=True)
        if result.returncode == 0:
            print("Requirements installed successfully!")
        else:
            raise Exception(f"Error occurred while installing requirements. Error code: {result.returncode}")
    except Exception as e:
        print(f"Failed to install requirements: {e}")

def run_tool(script_path, file_path):
    try:
        script_path = os.path.abspath(script_path)
        if os.path.exists(script_path):
            print(f"\nRunning tool: {script_path}\n")
            result = subprocess.run([sys.executable, script_path, "gui", file_path, "--export_path", EXPORT_DIR])
            if result.returncode != 0:
                raise Exception(f"Tool execution failed. Error code: {result.returncode}")
            print(f"Files exported to: {EXPORT_DIR}")
        else:
            print(f"\nError: Script not found at {script_path}")
    except Exception as e:
        print(f"Failed to run the selected tool: {e}")

def list_directory_contents():
    print("\nRoot Directory Contents:")
    for item in os.listdir():
        print(item)

def cli_mode():
    try:
        config = load_config()
        if config["is_new_user"] == 1:
            install_requirements("installReqs.bat")
            config["is_new_user"] = 0
            save_config(config)
            
        print("\nPlease place the file to be converted in the script's directory.")
        tools = display_menu()
        print("\nAvailable Tools:")
        for key, tool in tools.items():
            print(f"{key}. {tool['name']}")

        choice = input("\nEnter the number of the tool you want to run: ")
        if choice in tools:
            tool = tools[choice]
            install_requirements(tool["bat"])
            script_directory = os.path.dirname(os.path.abspath(__file__))
            list_directory_contents()
            print(f"Accepted file extensions: {', '.join([ext for _, ext in tool['filetypes']])}")
            file_name = input("Enter the name of the file (with extension): ").strip()
            file_path = os.path.join(script_directory, file_name)

            if not os.path.isfile(file_path):
                print("Invalid file path. Please provide a valid file.")
                return

            run_tool(tool["script"], file_path)
        else:
            print("Invalid choice. Exiting...")
    except Exception as e:
        print(f"Failed in CLI mode: {e}")

def gui_mode():
    try:
        def install_and_run():
            selected_idx = tool_listbox.curselection()
            if not selected_idx:
                messagebox.showwarning("No Selection", "Please select a tool to run.")
                return
            tool_key = tool_keys[selected_idx[0]]
            selected_tool = tools[tool_key]

            file_path = filedialog.askopenfilename(title="Select a file", filetypes=selected_tool["filetypes"])
            if not file_path:
                messagebox.showwarning("No File Selected", "Please select a file to process.")
                return

            try:
                install_requirements(selected_tool["bat"])
                run_tool(selected_tool["script"], file_path)
                messagebox.showinfo("Success", f"{selected_tool['name']} has been executed.\nFiles exported to: {EXPORT_DIR}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        root = tk.Tk()
        root.title("PyTools GUI")

        # Center the window on the screen
        window_width = 400
        window_height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        tk.Label(root, text="Select a Tool to Run").pack(pady=10)
        tools = display_menu()
        tool_keys = list(tools.keys())
        tool_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        for tool in tools.values():
            tool_listbox.insert(tk.END, tool["name"])
        tool_listbox.pack(pady=5)

        run_button = tk.Button(root, text="Run Tool", command=install_and_run)
        run_button.pack(pady=10)
        root.mainloop()
    except Exception as e:
        print(f"Failed in GUI mode: {e}")

if __name__ == "__main__":
    try:
        config = load_config()
        if config["is_new_user"] == 1:
            install_requirements("installReqs.bat")
            config["is_new_user"] = 0
            save_config(config)

        mode = input("\n1) for cli, or \n2) for gui\n2Enter mode : ").strip().lower()
        if mode == "1" or mode == "cli":
            cli_mode()
        elif mode == "2" or mode == "gui":
            gui_mode()
        else:
            print("Invalid mode. Exiting...")
    except Exception as e:
        print(f"Failed to start application: {e}")