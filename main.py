import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import pandas as pd
from openpyxl import load_workbook
from script import fetch_contributions

# Main window setup
root = tk.Tk()
root.title("Political Campaign Contributions Reporter")

# Initialize global variables after creating the root window
api_key = "your_initial_api_key"  # Replace with your default or saved API key
group_by_var = tk.BooleanVar(value=False)

# Function to parse input
def parse_input():
    content = text_area.get("1.0", "end-1c")
    lines = content.split("\n")
    contributors = [tuple(line.split(",")) for line in lines if line]
    return contributors

# Function to auto-adjust column width in Excel
def auto_adjust_column_width(filepath):
    workbook = load_workbook(filepath)
    worksheet = workbook.active
    for column_cells in worksheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells) + 2
        worksheet.column_dimensions[column_cells[0].column_letter].width = length
    workbook.save(filepath)

# Function to start report generation in a thread
def start_report_generation():
    if api_key == "your_initial_api_key":
        messagebox.showwarning("API Key Required", "Please set the API key in the Settings tab.")
        return
    progress_bar.start(10)
    threading.Thread(target=generate_report).start()

# Function to generate report
def generate_report():
    contributors = parse_input()
    min_amount = min_amount_entry.get()
    max_amount = max_amount_entry.get()
    year = year_entry.get()

    min_amount = float(min_amount) if min_amount else None
    max_amount = float(max_amount) if max_amount else None
    year = int(year) if year else 2024

    contributions_df = fetch_contributions(api_key, contributors, min_amount, max_amount, year, group_by_var.get())

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        contributions_df.to_excel(file_path, index=False)
        auto_adjust_column_width(file_path)

    # Stop and reset the progress bar
    progress_bar.stop()
    progress_bar['mode'] = 'determinate'
    progress_bar['value'] = 0
    progress_bar['mode'] = 'indeterminate'

# Function to save settings
def save_settings():
    global api_key
    api_key = api_key_entry.get()
    api_key_message_label.pack_forget()  # Hide the API key message
    messagebox.showinfo("Settings Saved", "Your settings have been successfully saved.")

# Notebook (tab control)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Main tab
main_frame = ttk.Frame(notebook)
notebook.add(main_frame, text='Main')

# Settings tab
settings_frame = ttk.Frame(notebook)
notebook.add(settings_frame, text='Settings')

# Main tab contents
api_key_message_label = tk.Label(main_frame, text="Please set the API key in the Settings tab.", fg="red")
if api_key == "your_initial_api_key":
    api_key_message_label.pack(pady=10)

text_area = tk.Text(main_frame, height=20, width=50)
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

control_frame = tk.Frame(main_frame)
control_frame.pack(side=tk.RIGHT, fill=tk.Y)

min_amount_label = tk.Label(control_frame, text="Minimum Amount:")
min_amount_label.pack()
min_amount_entry = tk.Entry(control_frame)
min_amount_entry.pack()

max_amount_label = tk.Label(control_frame, text="Maximum Amount:")
max_amount_label.pack()
max_amount_entry = tk.Entry(control_frame)
max_amount_entry.pack()

year_label = tk.Label(control_frame, text="Transaction Year:")
year_label.pack()
year_entry = tk.Entry(control_frame)
year_entry.pack()

generate_button = tk.Button(control_frame, text="Generate Report", command=start_report_generation)
generate_button.pack(pady=10)

progress_bar = ttk.Progressbar(control_frame, orient="horizontal", length=200, mode="indeterminate")
progress_bar.pack(pady=10)

# Settings tab contents
api_key_label = tk.Label(settings_frame, text="API Key:")
api_key_label.pack()
api_key_entry = tk.Entry(settings_frame)
api_key_entry.pack()
api_key_entry.insert(0, api_key)

group_by_checkbox = tk.Checkbutton(settings_frame, text="Enable Grouping", variable=group_by_var)
group_by_checkbox.pack()

save_settings_button = tk.Button(settings_frame, text="Save Settings", command=save_settings)
save_settings_button.pack()

# Start the GUI loop
root.mainloop()
