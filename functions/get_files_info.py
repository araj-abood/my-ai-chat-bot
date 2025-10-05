import os 

def get_files_info(working_directory, directory="."):
    try:
        working_directory_absolute_path = os.path.abspath(working_directory)
        directory_absolute_path = os.path.join(working_directory_absolute_path, directory)
        
        target_dir = os.path.abspath(directory_absolute_path)


        if not  target_dir.startswith(working_directory_absolute_path) :
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        is_directory = os.path.isdir(target_dir)

        if not is_directory:
            return f'Error: "{directory}" is not a directory'

        contents = os.listdir(target_dir)

        file_info_message = ''
        for item in contents:
            item_path = os.path.join(directory_absolute_path, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isfile(item_path)
            info = f"- {item}: file_size={size}, is_dir={is_dir}\n"
            file_info_message += info

        return (file_info_message)
    except Exception as e:
        return f"Error {e}"
