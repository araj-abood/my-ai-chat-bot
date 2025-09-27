
import os
from dotenv import load_dotenv
from google import genai
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    clinet = genai.Client(api_key=api_key)

    arguments = sys.argv

    user_prompt = " ".join(arguments[1:])

    if not user_prompt:
        print("No prompt provided")
        exit(1)

    response = clinet.models.generate_content(model="gemini-2.0-flash-001", contents=user_prompt)

    response_text = response.text

    print(response_text)
    meta_data = response.usage_metadata
    print(f"Prompt tokens: {meta_data.prompt_token_count}")
    print(f"Response tokens: {meta_data.candidates_token_count}")

if __name__ == "__main__":
    main()
