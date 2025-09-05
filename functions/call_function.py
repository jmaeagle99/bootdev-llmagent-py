from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.functions import (
    get_file_content_name,
    get_files_info_name,
    run_python_file_name,
    write_file_name,
)
from google.genai import types

def __create_result(function_name, result):
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )

def __create_error(function_name, error_message):
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": error_message},
            )
        ],
    )

def __create_error_unkown_function(function_name):
    return __create_error(function_name, f"Unknown function: {function_name}")

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name == get_file_content_name:
        return __create_result(
            get_file_content_name,
            get_file_content("./calculator", **function_call_part.args)
        )
    elif function_call_part.name == get_files_info_name:
        return __create_result(
            get_files_info_name,
            get_files_info("./calculator", **function_call_part.args)
        )
    elif function_call_part.name == run_python_file_name:
        return __create_result(
            run_python_file_name,
            run_python_file("./calculator", **function_call_part.args)
        )
    elif function_call_part.name == write_file_name:
        return __create_result(
            write_file_name,
            write_file("./calculator", **function_call_part.args)
        )
    else:
        return __create_error_unkown_function(function_call_part.name)