import os
import base64
import fnmatch
import tempfile
import subprocess

# List of file patterns to exclude from encoding
excluded_files = ['*.md', 'packager.py', '*.sublime*', 'commit.py', 'changelog.md', '.gitattributes']  # Add filenames or patterns here
# List of directory patterns to exclude from encoding
excluded_dirs = ['.git', 'config', '__pycache__']  # Add directory names or patterns here

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

def remove_tree(path):
    """Recursively removes a directory and all its contents."""
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

def create_package(output_file):
    """Creates a Python file that contains the encoded files."""
    with open(output_file, 'w') as pkg_file:
        pkg_file.write("# -------------------------------------\n# Packaged File\n# -------------------------------------\n")
        pkg_file.write("import base64\n")
        pkg_file.write("import tempfile\n")
        pkg_file.write("import subprocess\n")
        pkg_file.write("import os\n\n")

        pkg_file.write("def remove_tree(path):\n")
        pkg_file.write("    # Recursively removes a directory and all its contents.\n")
        pkg_file.write("    for root, dirs, files in os.walk(path, topdown=False):\n")
        pkg_file.write("        for name in files:\n")
        pkg_file.write("            os.remove(os.path.join(root, name))\n")
        pkg_file.write("        for name in dirs:\n")
        pkg_file.write("            os.rmdir(os.path.join(root, name))\n")
        pkg_file.write("    os.rmdir(path)\n\n")
        
        pkg_file.write("def get_encoded_files():\n")
        pkg_file.write("    return {\n")
        
        for root, dirs, files in os.walk('.'):
            # Exclude directories that match the exclusion patterns
            dirs[:] = [d for d in dirs if not should_exclude_dir(d)]
            
            for file in files:
                if file != os.path.basename(output_file) and not should_exclude_file(file):
                    file_path = os.path.join(root, file)
                    encoded_data = encode_file(file_path)
                    relative_path = os.path.relpath(file_path).replace('\\', '/')
                    pkg_file.write(f"        '{relative_path}': '''{encoded_data}''',\n")
        
        pkg_file.write("    }\n\n")
        
        pkg_file.write("\nif __name__ == '__main__':\n")
        pkg_file.write("    encoded_files = get_encoded_files()\n")
        pkg_file.write("    temp_dir = tempfile.mkdtemp()\n")
        pkg_file.write("    print('Decoding files...')\n")
        pkg_file.write("    for rel_path, encoded_content in encoded_files.items():\n")
        pkg_file.write("        decoded_file_path = os.path.join(temp_dir, rel_path)\n")
        pkg_file.write("        os.makedirs(os.path.dirname(decoded_file_path), exist_ok=True)\n")
        pkg_file.write("        with open(decoded_file_path, 'wb') as file:\n")
        pkg_file.write("            file.write(base64.b64decode(encoded_content))\n")
        pkg_file.write("    print('Executing gamesessionmanager.py...')\n")
        pkg_file.write("    subprocess.run(['python', os.path.join(temp_dir, 'gamesessionmanager.py')])\n")
        pkg_file.write("    print('Cleaning up...')\n")
        pkg_file.write("    print(temp_dir)\n")
        pkg_file.write("    remove_tree(temp_dir)\n")

if __name__ == "__main__":
    output_file_name = "../GameSessionManagerPackage/GSMFull.py"
    create_package(output_file_name)
    print(f"Package created: {output_file_name}")
