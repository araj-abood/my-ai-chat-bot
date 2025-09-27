
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    clinet = genai.Client(api_key=api_key)

    arguments = sys.argv

    user_prompt = " ".join(arguments[1:])

    if "--verbose" in user_prompt:
        user_prompt = user_prompt.replace("--verbose", "")

    if not user_prompt:
        print("No prompt provided")        
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        exit(1)

    is_verbose = "--verbose" in arguments
    
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]


    response = clinet.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages
    
    )

    response_text = response.text
    if is_verbose:
        print(f"User prompt: {user_prompt}")
        meta_data = response.usage_metadata
        print(f"Prompt tokens: {meta_data.prompt_token_count}")
        print(f"Response tokens: {meta_data.candidates_token_count}")
    print("Response:")
    print(response_text)

if __name__ == "__main__":
    main()
