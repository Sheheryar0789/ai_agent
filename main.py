import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_ITERS
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_files_content
from functions.run_python_files import schema_run_python_file
from functions.write_content import schema_write_file
from call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read the content of a file
        - Write content to a file (create or update)
        - Run a Python file with optional command-line arguments

        When the user asks about the code project - they are referring to 
        the working directory. So, you should typically start by looking at the 
        project's files, and figuring out how to run the project and how
        to run its tests, you'll always want to test the tests and the actual project
        to verify that behavior is working.
        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """


    # print(sys.argv)
    if len(sys.argv) < 2:   
        print("Please provide a prompt.")
        return
    verbose_mode = False
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        verbose_mode = True
    prompt = sys.argv[1]


    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_files_content, 
        schema_run_python_file, 
        schema_write_file
        ],
    )
    
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt)

    for i in range(0, MAX_ITERS):

        response = client.models.generate_content(
            model='gemini-2.5-flash', contents=messages,
            config=config
        )

        if response is None or response.usage_metadata is None:
            print("Response or usage metadata is None")
            return
            
        if verbose_mode:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            for function_call in response.function_calls:
                result = call_function(function_call, verbose=verbose_mode)
                messages.append(result)

        else:
            print(response.text)
            return

main()
