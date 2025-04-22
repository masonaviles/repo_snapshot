
# Repo to JSON Snapshot Tool

This script generates a **JSON snapshot** of a local project or Git repository.  
It captures the folder structure, file names, file sizes, and a small preview of each file.

---

## Features

- Excludes system and unnecessary folders like:
  - `.git`, `node_modules`, `venv`, `__pycache__`
- Captures:
  - Folder and file hierarchy
  - File sizes in bytes
  - Preview of the first 10 lines of each file (configurable)
- Outputs a single `.json` file saved inside the project directory.

---

## Requirements

- Python 3.6 or higher

No external libraries are needed — only the Python Standard Library.

---

## Usage

Navigate to the folder where you saved the script and run:

```bash
python3 repo_to_json.py /path/to/your/project
```

**Example:**

```bash
python3 repo_to_json.py /mnt/c/Users/mason/Dev/CustomerApp
```

This will create a file called `repo_snapshot.json` **inside your project folder**.

If you want to name the output differently:

```bash
python3 repo_to_json.py /mnt/c/Users/mason/Dev/CustomerApp -o my_snapshot.json
```

---

## JSON Structure Example

```json
{
  "path": "/path/to/project",
  "folders": [
    {
      "name": "/",
      "files": [
        {
          "name": "app.py",
          "size_bytes": 1234,
          "preview": "import os\nimport sys\n..."
        }
      ]
    },
    {
      "name": "subfolder",
      "files": [
        {
          "name": "utils.py",
          "size_bytes": 567,
          "preview": "def helper():\n    pass\n..."
        }
      ]
    }
  ]
}
```

---

## Notes

- Only **text-readable** files are previewed. If the script encounters binary files or unreadable files, it records an error instead.
- Hidden files and system files like `.DS_Store` and `Thumbs.db` are skipped automatically.

---

## License

This tool is provided under the MIT License.  
Feel free to use, modify, and redistribute.
