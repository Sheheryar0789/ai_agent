import os
from config import MAX_CHAR
from google.genai import types

def get_files_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not in the working directory."
    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file."

    file_string_content = ""
    try:
        with open(abs_file_path, 'r') as f:
            file_string_content = f.read(MAX_CHAR)
            if len(file_string_content) >= MAX_CHAR:
                file_string_content += f"\n[...{file_path}] Content truncated due to size limit]"
            return file_string_content
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"
    
schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Gets the content of the given file as a string, constrained to a maximum number of characters defined by MAX_CHAR. If the file is larger than MAX_CHAR, the content will be truncated and a message will be appended indicating that the content has been truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, from the working directory.",
            ),
        },
    ),
)