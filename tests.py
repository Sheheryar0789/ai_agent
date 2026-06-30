# from functions.get_files_info import get_files_info
# from functions.get_files_content import get_files_content

# from functions.write_content import write_file


from functions.run_python_files import run_python_file


def main():
    working_directory = "calculator"
    print(run_python_file(working_directory, "main.py", ["5 + 3"]))

main()