import os
import json
import argparse

EXCLUDE_DIRS = ['.git', 'venv', 'node_modules', '__pycache__']
EXCLUDE_FILES = ['.DS_Store', 'Thumbs.db']
MAX_PREVIEW_LINES = 10

def should_include(path):
    return not any(excl in path for excl in EXCLUDE_DIRS)

def build_json_structure(root_path):
    repo = {
        "path": root_path,
        "folders": []
    }

    for foldername, subfolders, filenames in os.walk(root_path):
        subfolders[:] = [d for d in subfolders if should_include(os.path.join(foldername, d))]

        rel_folder = os.path.relpath(foldername, root_path)
        folder = {
            "name": rel_folder if rel_folder != '.' else "/",
            "files": []
        }

        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            rel_path = os.path.relpath(file_path, root_path)

            if not should_include(file_path) or filename in EXCLUDE_FILES:
                continue

            file_info = {
                "name": filename,
                "size_bytes": os.path.getsize(file_path)
            }

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    preview = "".join([line for _, line in zip(range(MAX_PREVIEW_LINES), f)])
                    file_info["preview"] = preview
            except Exception as e:
                file_info["error"] = str(e)

            folder["files"].append(file_info)

        repo["folders"].append(folder)

    return repo

def save_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON snapshot saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a JSON representation of your local repo")
    parser.add_argument("repo_path", help="Path to your repo")
    parser.add_argument("-o", "--output", default="repo_snapshot.json", help="Output JSON filename")
    args = parser.parse_args()

    if not os.path.isdir(args.repo_path):
        print("❌ Error: Not a valid directory.")
    else:
        json_data = build_json_structure(args.repo_path)

        # ⬇️ this line is the important change:
        output_path = os.path.join(args.repo_path, args.output)

        save_json(json_data, output_path)

