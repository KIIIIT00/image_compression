import tkinter as tk
from tkinter import filedialog, ttk, Canvas, messagebox
from PIL import Image, ImageTk
import threading
import os
import time
import glob

class UI_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compression App")
        self.root.geometry("800x600")  # Set window size
        
        # Variable to store compression handler class (ImageCompression)
        self.compression_handler = None
        
        # Store selected files and folders
        self.selected_files = []
        self.selected_folder = ""
        self.output_folder = os.path.join(os.path.expanduser("~"), "compressed_images")
        
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left frame (for controls)
        control_frame = tk.Frame(main_frame, width=300)
        control_frame.pack(side="left", fill="y", padx=10)
        
        # File selection button
        self.file_button = self.create_button(root=control_frame, 
                                              text="Select Image Files",
                                              command=self.select_files
                                              )

        # Folder selection button
        self.folder_button = self.create_button(root=control_frame, 
                                                text="Select Folder",
                                                command=self.select_folder
                                                )

        # Output folder selection button
        self.output_folder_button = self.create_button(root=control_frame, 
                                                    text="Select Output Folder",
                                                    command=self.select_output_folder
                                                    )
        
        # Label to display selected files
        self.file_label = self.create_label(root=control_frame, 
                                            text="No files selected"
                                            )
        # Label to display selected folder
        self.folder_label = self.create_label(root=control_frame, 
                                              text="No folder selected"
                                              )
                                              
        # Label to display output folder
        self.output_folder_label = self.create_label(root=control_frame, 
                                                    text=f"Output folder: {self.output_folder}"
                                                    )
        
        # Create dropdown list
        tk.Label(control_frame, text="Compression Level:").pack(pady=(10, 0))
        values = ["Strong Compression", "Normal Compression", "Light Compression"]
        self.combo = ttk.Combobox(control_frame, values=values, state="readonly")
        self.combo.set("Normal Compression") # Set initial value
        self.combo.pack(pady=5)
        
        # PNG to JPEG Option
        self.convert_png_var = tk.BooleanVar(value=True)
        self.png_checkbox = tk.Checkbutton(control_frame, 
                                          text="Convert PNG to JPEG", 
                                          variable=self.convert_png_var)
        self.png_checkbox.pack(pady=5)
        
        # Compress button
        self.compress_button = self.create_button(root=control_frame, 
                                                  text="Compress",
                                                  command=self.compress_images,
                                                  bg="#4CAF50",  # Green
                                                  fg="white"
                                                  )
        
        # Right frame (for image preview)
        preview_frame = tk.Frame(main_frame)
        preview_frame.pack(side="right", fill="both", expand=True)
        
        # Label for selected images
        self.image_list_label = tk.Label(preview_frame, text="Selected Images", font=("Arial", 12, "bold"))
        self.image_list_label.pack(side="top", pady=5)
        
        # Create scrollable canvas
        self.canvas_frame = tk.Frame(preview_frame)
        self.canvas_frame.pack(fill="both", expand=True)
        
        self.canvas = Canvas(self.canvas_frame)
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        
        self.scroll_frame = ttk.Frame(self.canvas)
        self.scroll_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # List to store image references (to prevent garbage collection)
        self.image_refs = []
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.statusbar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set_compression_handler(self, handler_class):
        """Set the compression handler class"""
        self.compression_handler = handler_class
    
    def create_button(self, root, text, command, bg="SystemButtonFace", fg="black", width=15, height=2):
        """
        Create a tkinter button with customizable options.
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
    
    def create_label(self, root, text, wraplength=300, font=("TkDefaultFont", 9, "normal"), justify="left", is_hidden=False):
        """
        Create a tkinter label with customizable options.
        """
        label = tk.Label(root, text=text, wraplength=wraplength, font=font, justify=justify)
        label.pack(pady=5)
        if is_hidden:
            label.pack_forget() # Hide initially
        return label
    
    def select_files(self):
        """
        Open file selection dialog
        """
        file_paths = filedialog.askopenfilenames(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.heic;*.heif;*.bmp;*.gif;*.tiff;*.webp")]
        )

        if file_paths:
            self.selected_files = file_paths
            self.file_label.config(text=f"Selected files: {len(file_paths)} images")
            self.selected_folder = ""
            self.folder_label.config(text="No folder selected")
            self.display_images(file_paths)
            self.status_var.set(f"{len(file_paths)} files selected")
        else:
            self.status_var.set("File selection cancelled")
            
    def select_folder(self):
        """
        Open folder selection dialog
        """
        folder_path = filedialog.askdirectory()

        if folder_path:
            self.selected_folder = folder_path
            self.folder_label.config(text="Selected folder: " + folder_path)
            self.selected_files = []
            self.file_label.config(text="No files selected")
            
            # Get image files in the folder
            image_files = []
            for ext in ['*.png', '*.jpg', '*.jpeg', '*.heic', '*.heif', '*.bmp', '*.gif', '*.tiff', '*.webp']:
                image_files.extend(glob.glob(os.path.join(folder_path, ext)))
                image_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
            
            if image_files:
                self.display_images(image_files[:20])  # Display only first 20 images
                self.status_var.set(f"Found {len(image_files)} images in folder")
            else:
                self.clear_image_display()
                self.status_var.set("No images found in folder")
        else:
            self.status_var.set("Folder selection cancelled")
    
    def select_output_folder(self):
        """
        Open output folder selection dialog
        """
        folder_path = filedialog.askdirectory()

        if folder_path:
            self.output_folder = folder_path
            self.output_folder_label.config(text="Output folder: " + folder_path)
            self.status_var.set(f"Output folder set: {folder_path}")
    
    def compress_images(self):
        """
        Execute image compression process
        """
        # Input validation
        if not self.selected_files and not self.selected_folder:
            messagebox.showwarning("Warning", "Please select files or a folder.")
            return
            
        if not self.compression_handler:
            messagebox.showerror("Error", "Compression handler not set.")
            return
            
        # Get compression level
        compression_level = self.combo.get()
        convert_png = self.convert_png_var.get()
        
        # Create progress window
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Compressing...")
        progress_window.geometry("400x150")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Create progress bar
        progress_label = tk.Label(progress_window, text="Compressing images...", font=("Arial", 12))
        progress_label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=350, mode="indeterminate")
        progress_bar.pack(pady=10)
        progress_bar.start(10)
        
        status_label = tk.Label(progress_window, text="Starting process...")
        status_label.pack(pady=10)
        
        # Run compression in separate thread
        def compression_thread():
            try:
                # Create ImageCompression instance
                input_source = self.selected_folder if self.selected_folder else self.selected_files[0]
                
                compressor = self.compression_handler(
                    input_folder=input_source,
                    output_folder=self.output_folder,
                    quality_ratio=self.map_compression_level(compression_level),
                    convert_png_to_jpeg=convert_png
                )
                
                # Ensure folder exists
                self.compression_handler.create_folder_if_not_exists(self.output_folder)
                
                # Execute compression
                processed_count = 0
                total_files = 0
                
                if self.selected_folder:
                    # Compress entire folder
                    status_label.config(text=f"Processing folder '{os.path.basename(self.selected_folder)}'...")
                    processed_count = compressor.compress_folder()
                    
                else:
                    # Compress selected files
                    total_files = len(self.selected_files)
                    for i, file_path in enumerate(self.selected_files):
                        status_label.config(text=f"Processing... ({i+1}/{total_files})")
                        compressor.compress_image(file_path)
                        processed_count += 1
                
                # Update UI in main thread after completion
                self.root.after(0, lambda: self.compression_complete(progress_window, processed_count))
                
            except Exception as e:
                # Handle errors
                error_msg = str(e)
                self.root.after(0, lambda: self.compression_error(progress_window, error_msg))
        
        # Start thread
        threading.Thread(target=compression_thread, daemon=True).start()
        
    def compression_complete(self, progress_window, processed_count):
        """Process after compression completes"""
        progress_window.destroy()
        messagebox.showinfo("Complete", f"Compression completed. Processed {processed_count} files.")
        self.status_var.set(f"Compression complete: {processed_count} files processed")
        
        # Ask to open output folder
        if messagebox.askyesno("Confirm", "Open output folder?"):
            self.open_output_folder()
    
    def compression_error(self, progress_window, error_msg):
        """Handle compression errors"""
        progress_window.destroy()
        messagebox.showerror("Error", f"Error during compression: {error_msg}")
        self.status_var.set("Error occurred")
    
    def map_compression_level(self, level_text):
        """Convert compression level text to quality ratio"""
        if level_text == "Strong Compression":
            return 30
        elif level_text == "Normal Compression":
            return 60
        elif level_text == "Light Compression":
            return 85
        else:
            return 60  # Default to normal compression
    
    def open_output_folder(self):
        """Open output folder in file explorer"""
        try:
            import subprocess
            if os.name == 'nt':  # Windows
                os.startfile(self.output_folder)
            elif os.name == 'posix':  # Mac/Linux
                if os.path.exists('/usr/bin/open'):  # Mac
                    subprocess.call(['open', self.output_folder])
                else:  # Linux
                    subprocess.call(['xdg-open', self.output_folder])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")
    
    def display_images(self, file_paths):
        """
        Display selected images in the scrollable frame
        """
        # Clear previous images
        self.clear_image_display()
        
        # Limit the number of displayed images
        max_images = min(len(file_paths), 20)
        display_paths = file_paths[:max_images]
        
        num_columns = 3  # Number of images per row
        row, col = 0, 0  # Initialize row and column

        for file_path in display_paths:
            try:
                img = Image.open(file_path)
                img.thumbnail((120, 120))  # Resize thumbnail
                img_ref = ImageTk.PhotoImage(img)
                self.image_refs.append(img_ref)  # Keep reference
                
                # Create frame for image (containing image and filename)
                img_frame = ttk.Frame(self.scroll_frame)
                img_frame.grid(row=row, column=col, padx=10, pady=10)
                
                # Display image
                img_label = tk.Label(img_frame, image=img_ref)
                img_label.pack()
                
                # Display filename (shortened)
                file_name = os.path.basename(file_path)
                if len(file_name) > 15:
                    file_name = file_name[:12] + "..."
                name_label = tk.Label(img_frame, text=file_name, wraplength=120)
                name_label.pack()
                
                # Move to next position
                col += 1
                if col >= num_columns:
                    col = 0
                    row += 1
                    
            except Exception as e:
                print(f"Error loading image: {e}")
        
        # Update display message
        if len(file_paths) > max_images:
            self.status_var.set(f"Displaying {max_images} of {len(file_paths)} images")
            
    def clear_image_display(self):
        """Clear image display"""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.image_refs.clear()