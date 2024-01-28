import tkinter as tk
from tkinter import filedialog
import pandas as pd
from openpyxl import load_workbook
from script import fetch_contributions

def parse_input():
    content = text_area.get("1.0", "end-1c")
    lines = content.split("\n")
    contributors = [tuple(line.split(",")) for line in lines if line]
    return contributors

def auto_adjust_column_width(filepath):
    workbook = load_workbook(filepath)
    worksheet = workbook.active

    for column_cells in worksheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        worksheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    workbook.save(filepath)

def generate_report():
    contributors = parse_input()
    min_amount = min_amount_entry.get()
    max_amount = max_amount_entry.get()
    year = year_entry.get()

    min_amount = float(min_amount) if min_amount else None
    max_amount = float(max_amount) if max_amount else None
    year = int(year) if year else 2024

    apply_grouping = group_by_var.get()
    contributions_df = fetch_contributions(contributors, min_amount, max_amount, year, apply_grouping)

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        contributions_df.to_excel(file_path, index=False)
        auto_adjust_column_width(file_path)

root = tk.Tk()
root.title("Political Campaign Contributions Reporter")

left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

text_area = tk.Text(left_frame, height=20, width=50)
text_area.pack(expand=True, fill=tk.BOTH)

min_amount_label = tk.Label(right_frame, text="Minimum Amount:")
min_amount_label.pack()
min_amount_entry = tk.Entry(right_frame)
min_amount_entry.pack()

max_amount_label = tk.Label(right_frame, text="Maximum Amount:")
max_amount_label.pack()
max_amount_entry = tk.Entry(right_frame)
max_amount_entry.pack()

year_label = tk.Label(right_frame, text="Transaction Year:")
year_label.pack()
year_entry = tk.Entry(right_frame)
year_entry.pack()

group_by_var = tk.BooleanVar()
group_by_checkbox = tk.Checkbutton(right_frame, text="Enable Grouping", variable=group_by_var)
group_by_checkbox.pack()

generate_button = tk.Button(right_frame, text="Generate Report", command=lambda: generate_report())
generate_button.pack(pady=10)

root.mainloop()
