import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    try:
        full_file_path = os.path.join(working_directory, file_path)

        # Resolve absolute paths
        abs_working_directory = os.path.abspath(working_directory)
        if abs_working_directory[-1] != os.path.sep:
            abs_working_directory += os.path.sep

        abs_file_path = os.path.abspath(full_file_path)

        # Check is a file
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        # Check is Python file
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Check containment
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Run!
        try:
            subprocess_args = [ "python", abs_file_path ]
            subprocess_args.extend(args)

            completed_process = subprocess.run(
                args=subprocess_args,
                timeout=30,
                capture_output=True,
                cwd=working_directory
            )

            results = []
            if completed_process.stderr or completed_process.stdout:
                if completed_process.stdout:
                    results.append(f"STDOUT: {completed_process.stdout.decode('utf-8')}")
                if completed_process.stderr:
                    results.append(f"STDERR: {completed_process.stderr.decode('utf-8')}")
            else:
                results.append('No output produced.')
            if completed_process.returncode != 0:
                results.append(f"Process exited with code {completed_process.returncode}")

            return "\n".join(results)
        except Exception as e:
            return f"Error: executing Python file: {e}"
    except Exception as e:
        return f"Error: {str(e)}"