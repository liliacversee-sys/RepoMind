import os

SUPPORTED_EXTENSIONS = [".py", ".js", ".ts"]

def scan_repository(repo_path):

    files = []

    for root, dirs, filenames in os.walk(repo_path):

        for file in filenames:

            for ext in SUPPORTED_EXTENSIONS:
                if file.endswith(ext):
                    files.append(os.path.join(root, file))

    return files