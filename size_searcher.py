import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class SizeApp:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))
        style.configure('TLabel', font=('Helvetica', 18))

        self.frame = ttk.Frame(root, padding="20")
        self.frame.pack(expand=True)

        ttk.Label(self.frame, text="Select a directory:").pack(pady=0)
        ttk.Button(self.frame, text="Select", command=self.select_directory).pack(pady=20)
        ttk.Button(self.frame, text="Back", command=self.back).pack(pady=20)

        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(self.frame, yscrollcommand=self.scrollbar.set, width=100)
        self.listbox.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.listbox.yview)

    def get_files(self, directory):
        file_list = []
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                file_list.append((filepath, size))
        file_list.sort(key=lambda x: x[1], reverse=True)
        return file_list

    def delete_file(self, filepath):
        result = messagebox.askyesno("Delete File", f"Are you sure you want to delete {os.path.basename(filepath)}?")
        if result:
            try:
                os.remove(filepath)
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {str(e)}")
                return False
        return False

    def update_display(self):
        self.listbox.delete(0, tk.END)  # Clear the listbox

        for i, (filepath, size) in enumerate(self.file_list[:30], start=1):
            label_text = f"{i}. {os.path.basename(filepath)} - Size: {size} bytes"
            self.listbox.insert(tk.END, label_text)

        self.listbox.bind("<Double-Button-1>", self.on_double_click)
        self.listbox.bind("<Button-3>", self.on_right_click)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if not directory:
            return
        self.file_list = self.get_files(directory)
        self.update_display()

    def open_file(self, filepath):
        os.system(f'start "" "{filepath}"')

    def on_double_click(self, event):
        index = self.listbox.curselection()
        if index:
            filepath = self.file_list[index[0]][0]
            self.open_file(filepath)

    def on_right_click(self, event):
        index = self.listbox.curselection()
        if index:
            filepath = self.file_list[index[0]][0]
            self.delete_file(filepath)
            self.update_display()

    def back(self):
        self.frame.pack_forget()
        self.callback()

if __name__ == "__main__":
    root = tk.Tk()
    app = SizeApp(root, callback=root.quit)
    root.mainloop()
