import os
from google.genai import types
def write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))

    if not file_path_abs.startswith(working_directory_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
 
    with open(file_path_abs, "w") as f:
        f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



schema_write_file = types.FunctionDeclaration(
    name="write_file",
        description=(
            "Writes text content to a file."
            "Use ONLY when the user explicitly requests to 'save', 'create', or 'update' a file."
            "NEVER use this to list, explore,get , or inspect directories — use 'get_files_info' instead."
        ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base folder where the file is located."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative or absolute path of the file to be written."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the target file."
            ),
        }
    )
)
