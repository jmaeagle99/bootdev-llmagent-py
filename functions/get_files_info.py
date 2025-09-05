import os

def get_files_info(working_directory, directory="."):
    try:
        files_directory = os.path.join(working_directory, directory)
        
        # Resolve absolute paths
        abs_working_directory = os.path.abspath(working_directory)
        if abs_working_directory[-1] != os.path.sep:
            abs_working_directory += os.path.sep

        abs_files_directory = os.path.abspath(files_directory)
        if abs_files_directory[-1] != os.path.sep:
            abs_files_directory += os.path.sep

        # Check is a directory
        if not os.path.isdir(abs_files_directory):
            return f'Error: "{directory}" is not a directory'

        # Check containment
        if not abs_files_directory.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Build file and directory list
        info_list = []
        for file_name in os.listdir(abs_files_directory):
            full_path = os.path.join(abs_files_directory, file_name)
            info_list.append(f"- {file_name}, file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}")
        return "\n".join(info_list)
    except Exception as e:
        return f"Error: {str(e)}"