import os 
from google.genai import types

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
            is_dir = os.path.isdir(item_path)
            if is_dir:
                continue
            info = f"- '{item}'\n"
            file_info_message += info

        return (file_info_message)
    except Exception as e:
        return f"Error {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "DIRECTLY lists files and folders in a given directory. "
        "Use this function ANYTIME the user requests to 'list', 'show', or 'view' directory contents. "
        "This function accesses the file system directly — DO NOT generate or run Python code for this purpose."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The directory path to list, relative to the working directory. "
                    "If omitted, defaults to listing the working directory."
                ),
            ),
        },
    ),
)
