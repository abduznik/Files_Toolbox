import tkinter as tk
from tkinter import ttk
from file_sorter import FileSorterApp
from size_searcher import SizeApp  # Renamed from SizeSearcherApp
from file_organizer import FileOrganizerApp

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")
        self.root.geometry("800x400")

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))
        style.configure('TLabel', font=('Helvetica', 18))
        style.configure('TRadiobutton', font=('Helvetica', 16))

        self.frame = ttk.Frame(root, padding="20")
        self.frame.pack(expand=True)

        ttk.Label(self.frame, text="Select an application:").pack(pady=20)

        self.file_sorter_button = ttk.Button(self.frame, text="File Sorter", command=self.open_file_sorter)
        self.file_sorter_button.pack(side="left", padx=20)

        self.size_searcher_button = ttk.Button(self.frame, text="Size Searcher", command=self.open_size_searcher)
        self.size_searcher_button.pack(side="left", padx=20)

        self.file_organizer_button = ttk.Button(self.frame, text="File Organizer", command=self.open_file_organizer)
        self.file_organizer_button.pack(side="right", padx=20)


    def open_file_sorter(self):
        self.frame.pack_forget()
        FileSorterApp(self.root, self.back_to_main)

    def open_size_searcher(self):
        self.frame.pack_forget()
        SizeApp(self.root, self.back_to_main)  # Changed from SizeSearcherApp

    def open_file_organizer(self):
        self.frame.pack_forget()
        FileOrganizerApp(self.root, self.back_to_main)

    def back_to_main(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application terminated by user.")
