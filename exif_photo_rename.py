import os
import piexif

def rename_photo_files(directory):
    """Renames photos in a directory based on their EXIF create date and camera model.

    Args:
        directory: The directory containing the photos.
    """

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.cr2')):
            name_original = filename[:-4].lower()
            extension     = filename[-3:].lower()

            try:
                exif_data = piexif.load(os.path.join(directory, filename))
            except (piexif.InvalidImageDataError, KeyError):
                print(f"Error loading EXIF data for {filename}")
                continue

            name_new = get_new_name(exif_data)

            # rename raw photo files
            rename_file(directory, name_original, name_new, extension)

            # check if xmp file exists, rename if it does
            rename_file(directory, name_original, name_new, 'xmp')

            # check if photo has been exported to jpg or tiff, rename if it has
            rename_file(directory, name_original, name_new, 'jpg')
            rename_file(directory, name_original, name_new, 'tiff')

def get_new_name(exif_data):
    exif_datetime = str(exif_data['Exif'][36867])[2:-1]
    exif_datetime = exif_datetime.replace(" ", "_").replace(":","")
    # print(exif_datetime)

    exif_model = str(exif_data['0th'][272])[2:-1]
    if exif_model.lower() == 'Canon EOS REBEL T2i'.lower():
        exif_model = 'canont2i'
    elif exif_model.lower() == 'Canon EOS R6'.lower():
        exif_model = 'canonr6'
    elif exif_model.lower() == 'Galaxy S23'.lower():
        exif_model = 'galaxys23'
    else:
        exif_model = exif_model.lower().replace(" ", "")
    # print(exif_model)

    new_file_name = f"{exif_datetime}_{exif_model}"

    return new_file_name

def rename_file(directory, name_original, name_new, extension):
    file_original = f"{name_original}.{extension}"
    path_original = os.path.join(directory, file_original)

    if os.path.exists(path_original):
        file_new = f"{name_new}.{extension}"
        path_new = os.path.join(directory, file_new)

        if os.path.exists(path_new):
            print(f"New {extension} file for {file_original} already exists: {file_new}")
            return

        os.rename(path_original, path_new)
        log_filename_change(directory, file_original, file_new)
        print(f"Renamed {file_original} to {file_new}")

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
