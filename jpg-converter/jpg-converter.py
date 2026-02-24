import os
import argparse
from PIL import Image

# Optional HEIC support
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    print("HEIC support enabled.")
except ImportError:
    print("pillow-heif not installed. HEIC files may not work.")

# -----------------------------
# Argument parser
# -----------------------------
parser = argparse.ArgumentParser(
    description='Convert images to JPG format and optionally delete originals.'
)

parser.add_argument(
    'path',
    type=str,
    help='Path to the folder with images.'
)

parser.add_argument(
    '-d', '--delete',
    type=int,
    choices=[0, 1],
    default=0,
    help='Delete original files after conversion (1 = yes, 0 = no).'
)

parser.add_argument(
    '-q', '--quality',
    type=int,
    default=95,
    help='JPEG quality (1–100). Default is 95.'
)

args = parser.parse_args()

# -----------------------------
# Settings
# -----------------------------
folder_path = args.path
delete_original = args.delete
jpeg_quality = args.quality

formats_to_convert = (
    '.png', '.gif', '.bmp', '.tiff',
    '.jfif', '.webp', '.heic'
)

# -----------------------------
# Conversion function
# -----------------------------
def convert_to_jpg(root, filename):
    if filename.lower().endswith('.jpg'):
        return

    if filename.lower().endswith(formats_to_convert):
        original_file = os.path.join(root, filename)
        converted_file = os.path.join(
            root,
            os.path.splitext(filename)[0] + '.jpg'
        )

        try:
            with Image.open(original_file) as img:
                rgb_image = img.convert('RGB')
                rgb_image.save(
                    converted_file,
                    'JPEG',
                    quality=jpeg_quality,
                    optimize=True
                )

            print(f'Converted: {original_file}')

            if delete_original == 1:
                os.remove(original_file)
                print(f'Deleted: {original_file}')

        except Exception as e:
            print(f'Error converting {original_file}: {e}')

# -----------------------------
# Walk directory recursively
# -----------------------------
for root, dirs, files in os.walk(folder_path):
    for file in files:
        convert_to_jpg(root, file)

print("Conversion completed.")
