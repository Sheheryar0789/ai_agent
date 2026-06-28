import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # print(sys.argv)
    if len(sys.argv) < 2:   
        print("Please provide a prompt.")
        return
    verbose_mode = False
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        verbose_mode = True
    prompt = sys.argv[1]


    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )

    print(response.text)
    if response is None or response.usage_metadata is None:
        print("Response or usage metadata is None")
        return
        
    if verbose_mode:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()
