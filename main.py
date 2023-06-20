import os
import datetime
import stat


def rename_file(file_path, new_name):
    try:
        new_file_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_file_path)
        print(f"File '{file_path}' renamed to '{new_file_path}'.")
    except OSError as e:
        print(f"Error renaming file '{file_path}': {e}")


def recursive_rename(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Extract the existing name and extension
            name, ext = os.path.splitext(file_name)

            # Check if the file already follows the desired naming format
            if len(name) >= 8 and name[4] == '_' and name[7] == '_':
                try:
                    # Parse the existing date in the filename
                    existing_date = datetime.datetime.strptime(name[:7], "%Y_%m")

                    # Get the creation time and format the date
                    creation_time = os.stat(file_path).st_birthtime
                    creation_date = datetime.datetime.fromtimestamp(creation_time)

                    # Replace the existing date with the actual creation date
                    new_date_str = creation_date.strftime("%Y_%m")
                    new_name = new_date_str + name[7:] + ext

                    rename_file(file_path, new_name)
                except ValueError:
                    print(f"Skipping file '{file_path}' due to invalid date format.")
                continue

            # Get the creation time and format the date
            creation_time = os.stat(file_path).st_birthtime
            creation_date = datetime.datetime.fromtimestamp(creation_time)
            creation_date_str = creation_date.strftime("%Y_%m")

            # Generate the new filename
            new_file_name = f"{creation_date_str}_{name}{ext}"
            rename_file(file_path, new_file_name)


# Provide the folder path
folder_path = "/Users/zakzangrandocardoso/Library/Mobile Documents/com~apple~Pages/Documents"

recursive_rename(folder_path)
