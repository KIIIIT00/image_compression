import os
import tkinter as tk
import sys
from PIL import Image
from options.compression_option import CompressionOption
from util.ui_window import UI_Window
from util.image_compression import ImageCompression
from util.module_checker import ModuleChecker

def main():
    # Process command line arguments
    compression_options = CompressionOption()
    
    # Add GUI display flag (displays GUI when --gui option is specified)
    compression_options.parser.add_argument('--gui', action='store_true', 
                                  help='Launch the GUI version of the application')
    
    # Set default values to the parser to disable required flags
    compression_options.parser._option_string_actions['--input_folder'].required = False
    compression_options.parser._option_string_actions['--output_folder'].required = False
    
    # Parse arguments
    args = compression_options.parser.parse_args()
    
    # Initialize module checker
    checker = ModuleChecker()
    checker.check_and_import('PIL')
    checker.check_and_import('pillow_heif')
    
    # If in GUI mode, or if input/output folders are not specified
    if args.gui or (not args.input_folder and not args.output_folder):
        print("Starting in GUI mode...")
        root = tk.Tk()
        app = UI_Window(root)
        
        # Link the ImageCompression handler to the UI instance
        app.set_compression_handler(ImageCompression)
        
        root.mainloop()
    else:
        # Display command line arguments
        compression_options.print_options(args)
        
        # Create output folder
        ImageCompression.create_folder_if_not_exists(args.output_folder)
        
        # Execute compression process
        compressor = ImageCompression(
            input_folder=args.input_folder,
            output_folder=args.output_folder,
            quality_ratio=args.compression_ratio,
            convert_png_to_jpeg=args.convert_png_to_jpeg
        )
        
        # Start compression process
        processed_count = compressor.compress_folder()
        print(f"Compression complete. Processed {processed_count} files.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        if 'tkinter' in sys.modules:
            # Display error in GUI if tkinter is loaded
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"An application error occurred: {e}")
        sys.exit(1)