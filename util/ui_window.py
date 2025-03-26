import tkinter as tk
from tkinter import filedialog, ttk, Canvas
from PIL import Image, ImageTk
import threading

import time
class UI_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("画像圧縮アプリ")
        
        # File selection button
        self.file_button = self.create_button(root = self.root, 
                                              text="画像ファイルを選択",
                                              command=self.select_files
                                              )

        # Folder selection button
        self.folder_button = self.create_button(root = self.root, 
                                                text="フォルダを選択",
                                                command=self.select_folder
                                                )
        
        # Label to display selected files
        self.file_label = self.create_label(root=self.root, 
                                            text="選択されたファイルはありません"
                                            )
        # Label to display selected folder
        self.folder_label = self.create_label(root=self.root, 
                                              text="選択されたフォルダはありません"
                                              )
        
        # Create dropdown list
        values = ["強めの圧縮", "普通の圧縮", "弱めの圧縮"]
        self.combo = ttk.Combobox(self.root, values=values, state="readonly")
        self.combo.set("普通の圧縮") # Set initial value
        self.combo.pack(pady=10)
        # Bind selection event
        self.combo.bind("<<ComboboxSelected>>", self.on_selects)
        
        # Compress button
        self.compress_button = self.create_button(root=self.root, 
                                                  text="圧縮する",
                                                  command=self.compress_images
                                                  )
        
        
        # Frame for image list (for better positioning)
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(fill="both", expand=True, pady=10)
        
        # Label for selected images (Initially hidden)
        self.image_list_label = tk.Label(self.image_frame, text="選択された画像一覧", font=("Arial", 12, "bold"))
        self.image_list_label.pack(side="top", pady=5)
        self.image_list_label.pack_forget()  # Hide initially
        
        self.image_list_label = self.create_label(root=self.image_frame,
                                                  text="選択された画像一覧",
                                                  wraplength=400,
                                                  font=("Arial", 12, "bold"),
                                                  is_hidden=True
                                                  )
        
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
    
    def create_button(self, root, text, command, bg="SystemButtonFace", fg="black", width=15, height=2):
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
        button = tk.Button(root,
                            text=text,
                            command=command,
                            bg=bg,
                            fg=fg,
                            width=width,
                            height=height
                            )
        button.pack(pady=5)
        return button
    
    def create_label(self, root, text, wraplength=400, font=("TkDefaultFont", 9, "normal"), justify="left", is_hidden=False):
        """
        Create a tkinter label with customizable options.

        Args:
            text (str): The label text.
            wraplength (int, optional): Max width before text wraps. Default is 400.
            font (tuple, optional): Font style. Default is ("TkDefaultFont", 9, "normal").
            justify (str, optional): Text alignment. Default is "left".
            is_hidden (bool, optional): If True, the label will be created but hidden using pack_forget().

        Returns:
            tk.Label: The created label.
        """
        label = tk.Label(root, text=text, wraplength=wraplength, font=font, justify=justify)
        label.pack(pady=5)
        if is_hidden:
            label.pack_forget() # Hide initially
        return label
    
    def on_selects(self, event):
        """
        Update label when selection changes
        """
        selected_value = self.combo.get()
    
    def compress_images(self):
        """
        Executes the image compression process and displays a progress bar in a separate window.
        """
        selected_option = self.combo.get()
        print(f"Selected Compression Level: {selected_option}")

        if not self.image_refs:
            print("No images to compress!")
            return

        # Create a separate window for the progress bar
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Compressing...")
        self.progress_window.geometry("400x100")  # Set window size

        # Create a progress bar in the separate window
        self.progress = ttk.Progressbar(self.progress_window, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)
        
        # Start the compression process in a separate thread
        threading.Thread(target=self.run_compression, daemon=True).start()

    def run_compression(self):
        """
        Runs the image compression process and updates the progress bar.
        This function is executed in a separate thread to prevent UI blocking.
        """
        num_images = len(self.image_refs)
        for i in range(num_images):
            time.sleep(0.5)  # Simulate compression process
            self.progress["value"] = ((i + 1) / num_images) * 100
            self.progress_window.update()  # Ensure the UI updates

        print("Compression completed!")
        time.sleep(0.5)
        self.progress_window.destroy()  # Close the window after compression is complete
        
        # Reset the selected files, folder, and displayed images
        self.reset_selection()
        
    def reset_selection(self):
        """
        Reset the selected files, folder, and display images after compression.
        """
        self.file_label.config(text="選択されたファイルはありません")
        self.folder_label.config(text="選択されたフォルダはありません")
        self.combo.set("普通の圧縮")  # Reset compression level
        self.image_refs.clear()  # Clear image references
        self.image_list_label.pack_forget()  # Hide image list label
        self.clear_image_display()  # Clear displayed images
    
    def clear_image_display(self):
        """
        Clear the displayed images from the scrollable frame.
        """
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
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