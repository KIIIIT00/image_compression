import os
from PIL import Image
import pillow_heif
import pathlib
import glob

class ImageCompression:
    
    def __init__(self, input_folder, output_folder, quality_ratio=50, convert_png_to_jpeg=True):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.quality_ratio = quality_ratio
        self.convert_png_to_jpeg = convert_png_to_jpeg
        
    def heic2jpg(self, heic_path, output_path=None):
        """
        Convert HEIC image to JPG format
        
        Parameters:
        heic_path : string
            Path to HEIC image file
        output_path : string, optional
            Path to save JPG image. If None, saves to same directory with .jpg extension
        """
        try:
            heic_file = pillow_heif.read_heif(heic_path)
            data = Image.frombytes(
                heic_file.mode,
                heic_file.size,
                heic_file.data,
                'raw',
                heic_file.mode,
                heic_file.stride
            )
            
            if output_path is None:
                # Default output path is same directory with .jpg extension
                output_path = os.path.splitext(heic_path)[0] + '.jpg'
                
            data.save(output_path, 'JPEG', quality=self.quality_ratio)
            return True
        except Exception as e:
            print(f"Error converting HEIC to JPG: {e}")
            return False
    
    @staticmethod
    def create_folder_if_not_exists(output_folder_path):
        """
        Create folder if it doesn't exist
        
        Parameters:
        output_folder_path : string
            compression images folder
        """
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
            print(f"Folder '{output_folder_path}' has been created.")
        else:
            print(f"Folder '{output_folder_path}' already exists.")
            
    def compress_image(self, image_path, output_path=None):
        """
        Compress individual image file
        
        Parameters:
        image_path : string
            Path to image file
        output_path : string, optional
            Path to save compressed image. If None, determines based on settings
        
        Returns:
        bool: True if successful, False otherwise
        """
        try:
            # Get file extension (lowercase)
            ext = os.path.splitext(image_path)[1].lower()
            
            # If it's a HEIC file, use heic2jpg conversion
            if ext in ['.heic', '.heif']:
                return self.heic2jpg(image_path, output_path)
            
            # Open the image
            img = Image.open(image_path)
            
            # If no output path specified, create one
            if output_path is None:
                base_name = os.path.basename(image_path)
                
                # If convert_png_to_jpeg is True and file is PNG, change extension to .jpg
                if self.convert_png_to_jpeg and ext == '.png':
                    base_name = os.path.splitext(base_name)[0] + '.jpg'
                    
                output_path = os.path.join(self.output_folder, base_name)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Convert to RGB if necessary (to avoid problems with transparency)
            if img.mode in ['RGBA', 'LA'] and (self.convert_png_to_jpeg or ext != '.png'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])  # paste using the alpha channel as mask
                img = background
            
            # Save with compression
            if ext == '.png' and not self.convert_png_to_jpeg:
                # PNG uses different compression (0-9)
                img.save(output_path, optimize=True, 
                         quality=min(95, max(0, self.quality_ratio)))  # Clamp between 0-95
            elif ext in ['.jpg', '.jpeg'] or (ext == '.png' and self.convert_png_to_jpeg):
                # JPEG compression (0-95, with 95 being highest quality)
                img.save(output_path, 'JPEG', 
                         quality=min(95, max(0, self.quality_ratio)),  # Clamp between 0-95
                         optimize=True)
            else:
                # For other formats, just save with default settings
                img.save(output_path)
                
            print(f"Compressed {image_path} -> {output_path}")
            return True
        
        except Exception as e:
            print(f"Error compressing {image_path}: {e}")
            return False
    
    def compress_folder(self):
        """
        Compress all images in the input folder and save to output folder
        """
        # Ensure output folder exists
        self.create_folder_if_not_exists(self.output_folder)
        
        # File extensions to look for
        extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.heic', '*.heif', '*.tiff', '*.webp']
        
        # Find all matching files
        all_files = []
        for ext in extensions:
            # If input_folder is file, get directory
            if os.path.isfile(self.input_folder):
                search_path = os.path.join(os.path.dirname(self.input_folder), ext)
            else:
                search_path = os.path.join(self.input_folder, ext)
                
            # Use glob to find matching files
            all_files.extend(glob.glob(search_path))
            
        # Also check for uppercase extensions
        for ext in extensions:
            if os.path.isfile(self.input_folder):
                search_path = os.path.join(os.path.dirname(self.input_folder), ext.upper())
            else:
                search_path = os.path.join(self.input_folder, ext.upper())
            all_files.extend(glob.glob(search_path))
            
        # Check if we have files to compress
        if not all_files and os.path.isfile(self.input_folder):
            # If input_folder is actually a file, add it directly
            all_files = [self.input_folder]
            
        # Process each file
        processed_count = 0
        for image_path in all_files:
            if self.compress_image(image_path):
                processed_count += 1
                
        print(f"Compressed {processed_count} of {len(all_files)} images")
        return processed_count
        
    def map_compression_level(self, level_text):
        """
        Map the compression level text to a quality ratio
        
        Parameters:
        level_text : string
            Text description of compression level
        
        Returns:
        int: Quality ratio (0-95)
        """
        if level_text == "強めの圧縮":  # Strong compression
            return 30
        elif level_text == "普通の圧縮":  # Normal compression
            return 60
        elif level_text == "弱めの圧縮":  # Weak compression
            return 85
        else:
            return 60  # Default to normal compression
    