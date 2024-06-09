import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import Label, Button, Radiobutton, IntVar, filedialog, messagebox
from datetime import datetime

class FileSorterApp:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))
        style.configure('TLabel', font=('Helvetica', 18))
        style.configure('TRadiobutton', font=('Helvetica', 16))

        self.frame = ttk.Frame(root, padding="20")
        self.frame.pack(expand=True)

        ttk.Label(self.frame, text="Choose sorting option:").pack(pady=20)

        self.sort_option_var = IntVar()
        self.sort_option_var.set(1)

        ttk.Radiobutton(self.frame, text="Sort by Month", variable=self.sort_option_var, value=1).pack(pady=10)
        ttk.Radiobutton(self.frame, text="Sort by Size", variable=self.sort_option_var, value=2).pack(pady=10)

        ttk.Button(self.frame, text="Select Directory and Sort", command=self.select_directory).pack(pady=20)
        ttk.Button(self.frame, text="Back", command=self.back).pack(pady=20)

    def sort_files_by_month(self, directory):
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                month = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%B')
                month_dir = os.path.join(directory, month)
                if not os.path.exists(month_dir):
                    os.makedirs(month_dir)
                shutil.move(filepath, month_dir)

    def sort_files_by_size(self, directory):
        size_ranges = {
            'Tiny (0-1MB)': (0, 1 * 1024 * 1024),
            'Small (1-10MB)': (1 * 1024 * 1024, 10 * 1024 * 1024),
            'Medium (10-100MB)': (10 * 1024 * 1024, 100 * 1024 * 1024),
            'Large (100MB-1GB)': (100 * 1024 * 1024, 1 * 1024 * 1024 * 1024),
            'Huge (1GB+)': (1 * 1024 * 1024 * 1024, float('inf'))
        }

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                for category, (min_size, max_size) in size_ranges.items():
                    if min_size <= size < max_size:
                        size_dir = os.path.join(directory, category)
                        if not os.path.exists(size_dir):
                            os.makedirs(size_dir)
                        shutil.move(filepath, size_dir)
                        break

    def select_directory(self):
        directory = filedialog.askdirectory()
        if not directory:
            return

        sort_option = self.sort_option_var.get()
        if sort_option == 1:
            self.sort_files_by_month(directory)
        elif sort_option == 2:
            self.sort_files_by_size(directory)

        messagebox.showinfo("Success", "Files sorted successfully.")

    def back(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.back_callback()
