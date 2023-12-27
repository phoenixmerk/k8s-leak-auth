import os
import re
import sys

RED_COLOR = '\033[91m'
RESET_COLOR = '\033[0m'

def scan_yaml_files(directory, pattern):
    matched_files = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".yaml") or file.endswith(".yml"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        if re.search(pattern, content):
                            matched_files.append(file_path)
    except Exception as e:
        print(f"Error: {e}")    
    return matched_files

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script.py /path/to/directory")
        sys.exit(1)

    directory = sys.argv[1]
    pattern = re.compile(r'(?i)(\.(dockerconfigjson|dockercfg):\s*\|*\s*(ey|ew)+)')
    matched_files = scan_yaml_files(directory, pattern)

    if matched_files:
        print("Matched files:")
        for file_path in matched_files:
            print(f"{RED_COLOR}{file_path}{RESET_COLOR}")
    else:
        print("No matching files found.")

if __name__ == "__main__":
    main()