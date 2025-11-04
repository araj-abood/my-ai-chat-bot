
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from config import SYSTEM_PROMPT, MAX_ITERS
from call_functions import avaliable_functions
from functions.call_function import call_function

def main():
    load_dotenv()
  

    arguments = sys.argv

    # check if arg has verbose
    is_verbose = "--verbose" in arguments

    # build prompt array
    prompt_list = []
    for  arg in arguments:
        if not arg.startswith("--"):
            prompt_list.append(arg)

    print(prompt_list)
    # convert prompt list to string
    user_prompt = " ".join(prompt_list[1:])

    if not user_prompt:
        print("No prompt provided")        
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        exit(1)

    if is_verbose:
        print(f"User prompt: {user_prompt}")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    iters = 0
    
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Max iterations of ${MAX_ITERS}. Reached")
            sys.exit(1)
   
        try:
            final_response = generate_content(client, messages, is_verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")
            
    



    
  
def generate_content(client, messages, is_verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=[avaliable_functions])
    )
    
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)
            
    
    if is_verbose:
        meta_data = response.usage_metadata
        print(f"Prompt tokens: {meta_data.prompt_token_count}")
        print(f"Response tokens: {meta_data.candidates_token_count}")

    if not response.function_calls:
        return response.text

    function_response = []
    for function_call_part in response.function_calls:
        function_call_output = call_function(function_call_part, is_verbose)
        if not function_call_output.parts[0].function_response.response or not function_call_output.parts:
            raise Exception("empty function call result")
        if is_verbose:
            print(f"-> {function_call_output.parts[0].function_response.response}")
        
        function_response.append(function_call_output.parts[0])

    if not function_response:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="user", parts=function_response))


if __name__ == "__main__":
    main()
