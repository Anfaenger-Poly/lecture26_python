import shutil
import os

def copy_image_file(image_file):
    base, ext = os.path.splitext(image_file)
    new_name = f'{base}_copy{ext}'
    shutil.copy(image_file, new_name)

copy_image_file('photo.jpg')