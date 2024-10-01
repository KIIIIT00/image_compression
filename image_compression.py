from util.module_checker import ModuleChecker
import os
from PIL import Image
from options.compression_option import CompressionOption

# module_checker
module_checker = ModuleChecker()
module_checker.check_and_import('PIL.Image')
module_checker.check_and_import('os')

compression_options = CompressionOption()
args = compression_options.parse()


