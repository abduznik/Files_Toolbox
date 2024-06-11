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
        ttk.Button(self.frame, text="Organize Files", command=self.select_directory).pack(pady=20)
        ttk.Button(self.frame, text="De-organize Files", command=self.deorganize).pack(pady=20)
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

    def deorganize(self):
        directory = filedialog.askdirectory()
        if not directory:
            return

        file_names = {}
        for root_dir, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root_dir, file)
                if file in file_names:
                    new_file_name = f"{os.path.splitext(file)[0]}_{os.path.basename(file_names[file])}{os.path.splitext(file)[1]}"
                    dest_path = os.path.join(directory, new_file_name)
                    if os.path.exists(dest_path):
                        count = 1
                        while os.path.exists(
                                f"{os.path.splitext(dest_path)[0]}_{count}{os.path.splitext(dest_path)[1]}"):
                            count += 1
                        dest_path = f"{os.path.splitext(dest_path)[0]}_{count}{os.path.splitext(dest_path)[1]}"
                    shutil.move(file_path, dest_path)
                else:
                    file_names[file] = os.path.relpath(root_dir, directory)

        for root_dir, dirs, _ in os.walk(directory, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root_dir, dir)
                for root_subdir, subdirs, subdir_files in os.walk(dir_path):
                    for file in subdir_files:
                        shutil.move(os.path.join(root_subdir, file), directory)

        for root_dir, dirs, _ in os.walk(directory, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root_dir, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)

        messagebox.showinfo("Success", "Files and folders de-organized successfully.")

    def select_directory(self):
        directory = filedialog.askdirectory()
        if not directory:
            return

        self.organize_files_by_type(directory)

    def back(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.back_callback()

# Example usage
def main():
    root = tk.Tk()
    app = FileOrganizerApp(root, root.quit)
    root.mainloop()

if __name__ == "__main__":
    main()
