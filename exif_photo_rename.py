import os
import piexif

def rename_photo_files(directory):
    """Renames photos in a directory based on their EXIF create date and camera model.

    Args:
        directory: The directory containing the photos.
    """

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.cr2')):
            filepath = os.path.join(directory, filename)

            print(f"\nProcessing file: {filename}")

            try:
                exif_data = piexif.load(filepath)
            except (piexif.InvalidImageDataError, KeyError):
                print(f"    Error loading EXIF data for {filename}")
                continue

            filename_new_base = get_new_name(exif_data)
            filename_new = filename_new_base + '.cr2'

            filepath_new = os.path.join(directory, filename_new)

            if os.path.exists(filepath_new):
                print(f"    File already exists: {filename_new}")
                continue

            os.rename(filepath, filepath_new)
            log_filename_change(directory, filename, filename_new)
            print(f"    Renamed {filename} to {filename_new}")

            # check if xmp file exists, rename if it does
            filename_xmp = filename.split('.')[0] + ".XMP"
            filepath_xmp = os.path.join(directory, filename_xmp)

            if os.path.exists(filepath_xmp):
                print(f"    XMP file found: {filename_xmp}")

                filename_xmp_new = f"{filename_new_base}.xmp"
                filepath_xmp_new = os.path.join(directory, filename_xmp_new)

                if os.path.exists(filepath_xmp_new):
                    print(f"    XMP file already exists: {filename_xmp_new}")
                    continue

                os.rename(filepath_xmp, filepath_xmp_new)
                log_filename_change(directory, filename_xmp, filename_xmp_new)
                print(f"    Renamed {filename_xmp} to {filename_xmp_new}")

            # check if photo has been exported to jpg or tiff, rename if it has
            filename_jpg = filename.split('.')[0] + ".JPG"
            filepath_jpg = os.path.join(directory, filename_jpg)

            if os.path.exists(filepath_jpg):
                print(f"    JPG file found: {filename_jpg}")

                filename_jpg_new = f"{filename_new_base}.jpg"
                filepath_jpg_new = os.path.join(directory, filename_jpg_new)

                if os.path.exists(filepath_jpg_new):
                    print(f"    JPG file already exists: {filename_jpg_new}")
                    continue

                os.rename(filepath_jpg, filepath_jpg_new)
                log_filename_change(directory, filename_jpg, filename_jpg_new)
                print(f"    Renamed {filename_jpg} to {filename_jpg_new}")

def get_new_name(exif_data):
    exif_datetime = str(exif_data['Exif'][36867])[2:-1]
    exif_datetime = exif_datetime.replace(" ", "_").replace(":","")
    # print(exif_datetime)

    exif_model = str(exif_data['0th'][272])[2:-1]
    if exif_model.lower() == 'Canon EOS REBEL T2i'.lower():
        exif_model = 'canont2i'
    else:
        exif_model = exif_model.lower().replace(" ", "")
    # print(exif_model)

    new_file_name = f"{exif_datetime}_{exif_model}"

    return new_file_name

def log_filename_change(directory, original_name, new_name):
    change_log_filename = 'name_change.log'
    change_log_filepath = os.path.join(directory, change_log_filename)

    if not os.path.exists(change_log_filepath):
        change_log_output = open(change_log_filepath, 'w')
    else:
        change_log_output = open(change_log_filepath, 'a')

    change_log_output.write(original_name + '  >>>  ' + new_name + '\n')

    change_log_output.close()

if __name__ == "__main__":
    current_dir = os.getcwd()

    print(f"Processing files in {current_dir}")

    rename_photo_files(current_dir)
