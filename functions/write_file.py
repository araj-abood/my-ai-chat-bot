import os
def write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))

    if not file_path_abs.startswith(working_directory_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
 
    with open(file_path_abs, "w") as f:
        f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
