import os

REPO_URL = "https://github.com/lSaturnl/b2c_api_pits_demo/blob/main"
EXCLUDED_DIRS = {'.git', '.venv', '__pycache__'}

def generate_markdown_links(base_path="."):
    lines = []

    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        depth = root.replace(base_path, "").count(os.sep)
        indent = "  " * depth
        rel_dir = os.path.relpath(root, base_path).replace("\\", "/")
        if rel_dir != ".":
            lines.append(f"{indent}📁 {rel_dir}/")

        for f in files:
            rel_path = os.path.join(root, f).replace("\\", "/").lstrip("./")
            if any(part in EXCLUDED_DIRS for part in rel_path.split("/")):
                continue
            url = f"{REPO_URL}/{rel_path}"
            lines.append(f"{indent}  📄 [{f}]({url})")

    return "\n".join(lines)

if __name__ == "__main__":
    print(generate_markdown_links("."))
