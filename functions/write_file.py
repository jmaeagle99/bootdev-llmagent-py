import os


def write_file(working_directory, file_path, content):
    try:
        full_file_path = os.path.join(working_directory, file_path)

        # Resolve absolute paths
        abs_working_directory = os.path.abspath(working_directory)
        if abs_working_directory[-1] != os.path.sep:
            abs_working_directory += os.path.sep

        abs_file_path = os.path.abspath(full_file_path)

        # Check containment
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Create directories
        abs_file_dir_path = os.path.dirname(abs_file_path)
        os.makedirs(abs_file_dir_path, exist_ok=True)

        # Write file content
        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"