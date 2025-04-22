import os
import html
import xml.etree.ElementTree as ET
import argparse

EXCLUDE_DIRS = ['.git', 'venv', 'node_modules', '__pycache__']
EXCLUDE_FILES = ['.DS_Store', 'Thumbs.db']
MAX_PREVIEW_LINES = 10

def should_include(path):
    return not any(excl in path for excl in EXCLUDE_DIRS)

def build_xml_tree(root_path):
    repo_elem = ET.Element("repository", path=root_path)

    for foldername, subfolders, filenames in os.walk(root_path):
        subfolders[:] = [d for d in subfolders if should_include(os.path.join(foldername, d))]
        
        rel_folder = os.path.relpath(foldername, root_path)
        folder_elem = ET.SubElement(repo_elem, "folder", name=rel_folder if rel_folder != '.' else "/")

        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            if not should_include(file_path) or filename in EXCLUDE_FILES:
                continue

            file_elem = ET.SubElement(folder_elem, "file", name=filename)
            file_size = os.path.getsize(file_path)
            file_elem.set("size_bytes", str(file_size))

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    preview_lines = []
                    for _ in range(MAX_PREVIEW_LINES):
                        line = f.readline()
                        if not line:
                            break
                        preview_lines.append(line)
                    preview = ''.join(preview_lines)
                    
                    preview_elem = ET.SubElement(file_elem, "preview")
                    preview_elem.text = html.escape(preview)
            except Exception as e:
                ET.SubElement(file_elem, "error").text = html.escape(str(e))

    return ET.ElementTree(repo_elem)

def save_xml(tree, output_path):
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"✅ XML snapshot saved as {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an XML representation of your local Git repo")
    parser.add_argument("repo_path", help="Path to your repo")
    parser.add_argument("-n", "--name", default="repo_snapshot.xml", help="Output XML filename (name only)")
    args = parser.parse_args()

    if not os.path.isdir(args.repo_path):
        print("❌ Error: Not a valid directory.")
    else:
        output_file_path = os.path.join(args.repo_path, args.name)
        xml_tree = build_xml_tree(args.repo_path)
        save_xml(xml_tree, output_file_path)
