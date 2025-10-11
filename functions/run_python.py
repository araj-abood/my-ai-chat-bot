import os 
import subprocess

def run_python(working_directory, file_path, args=[]):
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

