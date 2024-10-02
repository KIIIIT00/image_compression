import os
from PIL import Image
import pillow_heif
import pathlib

class ImageCompression:
    
    def __init__(self, input_folder, output_folder,quality_ratio, convert_png_to_jpeg):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.quality_ratio = quality_ratio
        self.convert_png_to_jpeg = convert_png_to_jpeg
        
    
    def heic2jpg(self, input_folder):
        """
        input_folder : string
            input image folder
        """
        image_dir = pathlib.Path(input_folder)
        heic_path = list(image_dir.glob())