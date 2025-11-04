from functions import write_file, get_files_content,get_files_info, run_python_file
from google.genai import types

function_strings_to_actual_functions = {
    "get_file_content": get_files_content.get_file_content,
    "get_files_info": get_files_info.get_files_info,
    "run_python_file": run_python_file.run_python_file,
    "write_file": write_file.write_file
}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")



    function_name = function_call_part.name
    function_to_call = function_strings_to_actual_functions[function_name]

    if not function_to_call:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    function_result = function_to_call("./calculator",**function_call_part.args)
    
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)

