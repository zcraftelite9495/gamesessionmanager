import os
import base64
import fnmatch

# List of file patterns to exclude from encoding
excluded_files = ['*.py', '*.md', '*.sublime*', '.gitattributes']  # Add filenames or patterns here
# List of directory patterns to exclude from encoding
excluded_dirs = ['.git']  # Add directory names or patterns here

def encode_file(file_path):
    """Encodes a file to base64."""
    with open(file_path, 'rb') as file:
        file_data = file.read()
        encoded_data = base64.b64encode(file_data).decode('utf-8')
    return encoded_data

def should_exclude_file(file_name):
    """Check if the file name matches any of the exclusion patterns."""
    for pattern in excluded_files:
        if fnmatch.fnmatch(file_name, pattern):
            return True
    return False

def should_exclude_dir(dir_name):
    """Check if the directory name matches any of the exclusion patterns."""
    for pattern in excluded_dirs:
        if fnmatch.fnmatch(dir_name, pattern):
            return True
    return False

def create_package(output_file):
    """Creates a Python file that contains the base64 encoded files."""
    with open(output_file, 'w') as pkg_file:
        pkg_file.write("# This is an auto-generated package file\n")
        pkg_file.write("import base64\n")
        pkg_file.write("import os\n\n")
        pkg_file.write("def decode_files():\n")
        pkg_file.write("    files = {\n")
        
        for root, dirs, files in os.walk('.'):
            # Exclude directories that match the exclusion patterns
            dirs[:] = [d for d in dirs if not should_exclude_dir(d)]
            
            for file in files:
                if file != os.path.basename(output_file) and not should_exclude_file(file):
                    file_path = os.path.join(root, file)
                    encoded_data = encode_file(file_path)
                    relative_path = os.path.relpath(file_path).replace('\\', '/')
                    pkg_file.write(f"        '{relative_path}': '{encoded_data}',\n")
        
        pkg_file.write("    }\n\n")
        pkg_file.write("    for rel_path, data in files.items():\n")
        pkg_file.write("        # Create directories if they don't exist\n")
        pkg_file.write("        os.makedirs(os.path.dirname(rel_path), exist_ok=True)\n")
        pkg_file.write("        with open(rel_path, 'wb') as file:\n")
        pkg_file.write("            file.write(base64.b64decode(data))\n")
        pkg_file.write("decode_files()\n")
        
        # Append the content of gamesessionmanager.py
        try:
            with open('gamesessionmanager.py', 'r') as game_file:
                game_code = game_file.read()
                pkg_file.write("\n" + game_code + "\n")
        except FileNotFoundError:
            print("Warning: 'gamesessionmanager.py' not found. Skipping inclusion.")

if __name__ == "__main__":
    output_file_name = "../GameSessionManagerPackage/GSMFull.py"
    create_package(output_file_name)
    print(f"Package created: {output_file_name}")
