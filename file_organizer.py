import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FileOrganizerApp:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))
        style.configure('TLabel', font=('Helvetica', 18))

        self.frame = ttk.Frame(root, padding="20")
        self.frame.pack(expand=True)

        ttk.Label(self.frame, text="Select a directory to organize files by type:").pack(pady=20)
        ttk.Button(self.frame, text="Select Directory", command=self.select_directory).pack(pady=20)
        ttk.Button(self.frame, text="Back", command=self.back).pack(pady=20)

    def organize_files_by_type(self, directory):
        file_types = {
            'Videos': ['.mp4', '.avi', '.mkv', '.wmv', '.mov', '.flv'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
            'Documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
            'Programming': ['.py', '.java', '.cpp', '.c', '.html', '.css', '.js', '.php', '.xml'],
            'Apps': ['.exe', '.msi', '.app', '.dmg'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Etc': []
        }

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                file_ext = os.path.splitext(filename)[1].lower()
                for category, extensions in file_types.items():
                    if file_ext in extensions:
                        if category == 'Programming':
                            # Create a subdirectory for each programming file type
                            subcategory = file_ext.lstrip('.').upper()
                            dest_dir = os.path.join(directory, category, subcategory)
                        else:
                            dest_dir = os.path.join(directory, category)

                        if not os.path.exists(dest_dir):
                            os.makedirs(dest_dir)
                        shutil.move(filepath, dest_dir)
                        break
                else:
                    dest_dir = os.path.join(directory, 'Etc')
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    shutil.move(filepath, dest_dir)

        messagebox.showinfo("Success", "Files organized by type successfully.")
    def select_directory(self):
        directory = filedialog.askdirectory()
        if not directory:
            return

        self.organize_files_by_type(directory)

    def back(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.back_callback()