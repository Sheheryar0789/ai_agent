import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not in the working directory."
    
    parent_dir = os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"Could'nt create parent directory: {parent_dir}. Error: {str(e)}"
    
    try:
        with open(abs_file_path, 'w') as f:
            f.write(content)
            return (
                f"Successfully wrote to {file_path}. Content length: {len(content)} characters."
            )
    except Exception as e:
        return f"Error writing to file {file_path}: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)