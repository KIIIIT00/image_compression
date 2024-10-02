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
        input_path = os.path.join(input_folder, "/*.HEIC")
        image_dir = pathlib.Path(input_path)
        heic_path = list(image_dir.glob())
        for image in heic_path:
            heic_file = pillow_heif.read_heif(image)
            data = Image.frombytes(
                heic_file.mode,
                heic_file.size,
                heic_file.data,
                'raw',
                heic_file.mode,
                heic_file.stride
            )
            jpg_file_name = image.stem + '.jpg'
            save_path = os.path.join(input_folder, jpg_file_name)
            data.save(save_path, 'JPEG')
    
    def create_folder_if_not_exists(output_folder_path):
        """
        output_folder_path : string
            compression images folder
        """
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
            print(f"Folder '{output_folder_path}' has been created.")
        else:
            print(f"Folder '{output_folder_path}' already exists.")
    
    