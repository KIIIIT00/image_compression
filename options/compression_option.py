import argparse

class CompressionOption:
    
    def __init__(self):
        """Initialize the Option class."""
        self.parser = argparse.ArgumentParser(description="Command-line options for image compression.")
        self.initialize()
    
    def initialize(self):
        """Define command-line options."""
        parser = argparse.ArgumentParser(description="Options for image compression.")
        
        # Input and output folders
        parser.add_argument('--input_folder', type=str, 
                            required=True, 
                            help='Path to the input folder containing images.')
        parser.add_argument('--output_folder', type=str, 
                            required=True, 
                            help='Path to the output folder for processed images.')
        
        # Compression settings
        parser.add_argument('--compression_ratio', type=int, 
                            default=50, 
                            help='compression ratio for images[0-95] (default: 50).')
        parser.add_argument('--convert_png_to_jpeg', 
                            action='store_true', 
                            default=True, 
                            help='If specified, convert PNG images to JPEG format (default: True).')

        self.parser = parser
        self.initialized = True
    
    def parse(self):
        """Parse the command-line arguments."""
        if not self.initialized:
            self.initialize()

        options = self.parser.parse_args()
        return options
    
    def print_options(self, options):
        """Print the options in a structured format."""
        print("----------------- Options ---------------")
        print(f"               input_folder: {options.input_folder}")
        print(f"               output_folder: {options.output_folder}")
        print(f"               compression_ratio: {options.compression_ratio}")
        print(f"               convert_png_to_jpeg: {options.convert_png_to_jpeg}")
        print("----------------- End -------------------")