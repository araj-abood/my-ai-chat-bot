import os 
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    command = ["python", abs_file_path] + args

    try:
        completed_process = subprocess.run(args=command, timeout=30, capture_output=True)

        if len(completed_process.stdout) > 0:
            output =  f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
            return output + f"\nProcess exited with code {completed_process.returncode}"
        else:
            return "No output produced."
        
    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes an existing Python script file located within the working directory. "
        "Use this ONLY when explicitly instructed to run a pre-existing Python file. "
        "Do NOT use this function to perform file system tasks like listing directories or reading files — "
        "those should be handled by dedicated tools such as 'get_files_info'."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base directory containing the Python file to execute."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative or absolute path to the Python file to run."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to pass to the Python script when executing.",
                items=types.Schema(type=types.Type.STRING),
                default=[]
            )
        }
    )
)

