import tkinter as tk
from tkinter import filedialog, ttk, Canvas
from PIL import Image, ImageTk

class UI_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("画像圧縮アプリ")
        
        # File selection button
        self.file_button = tk.Button(root, text="画像ファイルを選択", command=self.select_files)
        self.file_button.pack(pady=5)

        # Folder selection button
        self.folder_button = tk.Button(root, text="フォルダを選択", command=self.select_folder)
        self.folder_button.pack(pady=5)

        # Label to display selected files
        self.file_label = tk.Label(root, text="選択されたファイルはありません", wraplength=400, justify="left")
        self.file_label.pack(pady=5)

        # Label to display selected folder
        self.folder_label = tk.Label(root, text="選択されたフォルダはありません", wraplength=400, justify="left")
        self.folder_label.pack(pady=5)
        
        # Frame for image list (for better positioning)
        self.image_frame = tk.Frame(root)
        self.image_frame.pack(fill="both", expand=True, pady=10)
        
        # Label for selected images (Initially hidden)
        self.image_list_label = tk.Label(self.image_frame, text="選択された画像一覧", font=("Arial", 12, "bold"))
        self.image_list_label.pack(side="top", pady=5)
        self.image_list_label.pack_forget()  # Hide initially
        
        # Scrollable frame for images
        self.canvas = Canvas(root)
        self.scroll_y = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = ttk.Frame(self.canvas)

        self.scroll_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        # List to store image references
        self.image_refs = []

    def select_files(self):
        """Open file selection dialog"""
        file_paths = filedialog.askopenfilenames(
            filetypes=[("画像ファイル", "*.png;*.jpg;*.jpeg;*.heic;*.heif;*.bmp;*.gif;*.tiff;*.webp")]
        )

        # Update label with selected files
        if file_paths:
            self.file_label.config(text="選択されたファイル:\n" + "\n".join(file_paths))
            self.image_list_label.pack() # Show the labe;
            self.display_images(file_paths)  # Display all selected images
        else:
            self.file_label.config(text="選択されたファイルはありません")
            self.image_list_label.pack_forget()  # Hide if no image is selected
            
    def select_folder(self):
        """Open folder selection dialog"""
        folder_path = filedialog.askdirectory()

        # Update label with selected folder
        if folder_path:
            self.folder_label.config(text="選択されたフォルダ:\n" + folder_path)
            
        else:
            self.folder_label.config(text="選択されたフォルダはありません")

    def display_images(self, file_paths):
        """Display all selected images in the scrollable frame"""
        # Clear previous images
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.image_refs.clear()

        num_columns = 3  # Set number of columns
        row, col = 0, 0  # Initialize row and column index

        for file_path in file_paths:
            try:
                img = Image.open(file_path)
                img.thumbnail((100, 100))  # Resize image for display
                img_ref = ImageTk.PhotoImage(img)
                self.image_refs.append(img_ref)  # Keep a reference

                # Create a label for each image and place it in a grid
                img_label = tk.Label(self.scroll_frame, image=img_ref)
                img_label.grid(row=row, column=col, padx=10, pady=5)

                # Update row and column for next image
                col += 1
                if col >= num_columns:
                    col = 0
                    row += 1
            except Exception as e:
                print(f"Error loading image: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = UI_Window(root)
    root.mainloop()