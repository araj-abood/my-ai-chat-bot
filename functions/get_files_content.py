import os
from config import MAX_CHARS
def get_file_content(working_directory, file_path):
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        file_path_abs_path = os.path.abspath(os.path.join(working_directory_abs_path, file_path))


        if not file_path_abs_path.startswith(working_directory_abs_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_path_abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            file_content_full = f.read()
            is_trunc = len(file_content_full) > len(file_content_string)
            return file_content_string +  f"{"[...File \"{file_path}\" truncated at 10000 characters]" if is_trunc else ""}" 

    except Exception as e:
        return f'Error: File not found or is not a regular file: "{file_path}"'

