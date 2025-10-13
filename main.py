
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from config import SYSTEM_PROMPT
from call_functions import avaliable_functions

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

    # convert prompt list to string
    user_prompt = " ".join(prompt_list)

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


    generate_content(client, messages, is_verbose)



    
  
def generate_content(client, messages, is_verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=[avaliable_functions])
    )
    if is_verbose:
        meta_data = response.usage_metadata
        print(f"Prompt tokens: {meta_data.prompt_token_count}")
        print(f"Response tokens: {meta_data.candidates_token_count}")
        
    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")


if __name__ == "__main__":
    main()
