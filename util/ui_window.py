import tkinter as tk
from tkinter import filedialog, ttk, Canvas
from PIL import Image, ImageTk

class UI_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("画像圧縮アプリ")
        
        # File selection button
        self.file_button = self.create_button(text="画像ファイルを選択",
                                              command=self.select_files
                                              )

        # Folder selection button
        self.folder_button = self.create_button(text="フォルダを選択",
                                                command=self.select_folder
                                                )
        
        # Label to display selected files
        self.file_label = tk.Label(self.root, text="選択されたファイルはありません", wraplength=400, justify="left")
        self.file_label.pack(pady=5)

        # Label to display selected folder
        self.folder_label = tk.Label(self.root, text="選択されたフォルダはありません", wraplength=400, justify="left")
        self.folder_label.pack(pady=5)
        
        # Create dropdown list
        values = ["強めの圧縮", "普通の圧縮", "弱めの圧縮"]
        self.combo = ttk.Combobox(self.root, values=values, state="readonly")
        self.combo.set("普通の圧縮") # Set initial value
        self.combo.pack(pady=10)
        # Bind selection event
        self.combo.bind("<<ComboboxSelected>>", self.on_selects)
        
        # Compress button
        self.compress_button = self.create_button(text="圧縮する",
                                                  command=self.compress_images
                                                  )
        
        # Frame for image list (for better positioning)
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(fill="both", expand=True, pady=10)
        
        # Label for selected images (Initially hidden)
        self.image_list_label = tk.Label(self.image_frame, text="選択された画像一覧", font=("Arial", 12, "bold"))
        self.image_list_label.pack(side="top", pady=5)
        self.image_list_label.pack_forget()  # Hide initially
        
        # Scrollable frame for images
        self.canvas = Canvas(self.root)
        self.scroll_y = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
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
    
    def create_button(self, text, command, bg="SystemButtonFace", fg="black", width=15, height=2):
        """
        Create a tkinter button with customizable options.

        Args:
            text (str): The button text.
            command (function): The function to call when the button is clicked.
            bg (str, optional): Background color. Default is OS default.
            fg (str, optional): Foreground (text) color. Default is black.
            width (int, optional): Button width. Default is 15.
            height (int, optional): Button height. Default is 2.

        Returns:
            tk.Button: The created button.
        """
        button = tk.Button(self.root,
                            text=text,
                            command=command,
                            bg=bg,
                            fg=fg,
                            width=width,
                            height=height
                            )
        button.pack(pady=5)
        return button
    
    def on_selects(self, event):
        """
        Update label when selection changes
        """
        selected_value = self.combo.get()
    
    def compress_images(self):
        """
        Process when the compress button is clicked
        """
        selected_option = self.combo.get()
        print(f"選択された圧縮レベル: {selected_option}")
        
    def select_files(self):
        """
        Open file selection dialog
        """
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
        """
        Open folder selection dialog
        """
        folder_path = filedialog.askdirectory()

        # Update label with selected folder
        if folder_path:
            self.folder_label.config(text="選択されたフォルダ:\n" + folder_path)
            
        else:
            self.folder_label.config(text="選択されたフォルダはありません")

    def display_images(self, file_paths):
        """
        Display all selected images in the scrollable frame
        """
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