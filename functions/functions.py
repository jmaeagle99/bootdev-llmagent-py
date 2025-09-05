from google.genai import types

get_file_content_name = "get_file_content"
get_files_info_name = "get_files_info"
run_python_file_name = "run_python_file"
write_file_name = "write_file_content"

schema_get_file_content = types.FunctionDeclaration(
    name=get_file_content_name,
    description="Retrieves the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            )
        },
        required=["file_path"],
    ),
)

schema_get_files_info = types.FunctionDeclaration(
    name=get_files_info_name,
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name=run_python_file_name,
    description="Executes a specified Python file with optional arguments and returns its output, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory. The file must have a .py extension.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to pass to the Python file when executing it.",
            ),
        },
        required=["file_path"],
        property_ordering=["file_path", "args"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name=write_file_name,
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory. If the file does not exist, it will be created.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
        property_ordering=["file_path", "content"],
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)