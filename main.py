import os
import sys
import json
import tkinter as tk
from tkinter import messagebox, filedialog

EXPORT_DIR = os.path.join(os.getcwd(), "exports")
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

CONFIG_FILE = "config.json"

def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        return {"is_new_user": 1}
    except Exception as e:
        print(f"Failed to load config: {e}")
        return {"is_new_user": 1}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file)
    except Exception as e:
        print(f"Failed to save config: {e}")

def display_menu():
    try:
        tools = {
            "1": {"name": "Image to PDF Converter", "script": "scripts/img2PDF/img2PDF.py", "bat": "scripts/img2PDF/installReqs_img2PDF.bat"},
            "2": {"name": "PDF to Text Converter", "script": "scripts/PDF2Text/PDF2Text.py", "bat": "scripts/PDF2Text/installReqs_PDF2Text.bat"},
        }
        return tools
    except Exception as e:
        print(f"Failed to display menu: {e}")
        return {}

def install_requirements(bat_file):
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
    try:
        if os.path.exists(script_path):
            print(f"\nRunning tool: {script_path}\n")
            result = os.system(f"{sys.executable} {script_path} --export_path={EXPORT_DIR}")
            if result != 0:
                raise Exception(f"Tool execution failed. Error code: {result}")
            print(f"Files exported to: {EXPORT_DIR}")
        else:
            print(f"\nError: Script not found at {script_path}")
    except Exception as e:
        print(f"Failed to run the selected tool: {e}")

def cli_mode():
    try:
        config = load_config()
        if config["is_new_user"] == 1:
            install_requirements("installReqs.bat")
            config["is_new_user"] = 0
            save_config(config)

        tools = display_menu()
        choice = input("\nEnter the number of the tool you want to run: ")
        if choice in tools:
            tool = tools[choice]
            install_requirements(tool["bat"])
            run_tool(tool["script"])
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

            try:
                install_requirements(selected_tool["bat"])
                os.system(f"{sys.executable} {selected_tool['script']} --export_path={EXPORT_DIR}")
                messagebox.showinfo("Success", f"{selected_tool['name']} has been executed.\nFiles exported to: {EXPORT_DIR}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        root = tk.Tk()
        root.title("PyTools GUI")

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

        mode = input("Enter mode (cli/gui): ").strip().lower()
        if mode == "cli":
            cli_mode()
        elif mode == "gui":
            gui_mode()
        else:
            print("Invalid mode. Exiting...")
    except Exception as e:
        print(f"Failed to start application: {e}")