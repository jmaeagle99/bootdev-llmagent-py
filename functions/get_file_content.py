import os


def get_file_content(working_directory, file_path):
    try:
        full_file_path = os.path.join(working_directory, file_path)

        # Resolve absolute paths
        abs_working_directory = os.path.abspath(working_directory)
        if abs_working_directory[-1] != os.path.sep:
            abs_working_directory += os.path.sep

        abs_file_path = os.path.abspath(full_file_path)

        # Check is a file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Check containment
        if not abs_file_path.startswith(abs_working_directory):
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Read file content
        MAX_CHARS = 10000
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(abs_file_path) > MAX_CHARS:
                file_content_string += "[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"
            return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"
