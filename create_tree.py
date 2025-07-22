import os

REPO = "lSaturnl/b2c_api_pits_demo"
BRANCH = "refs/heads/main"
GITHUB_URL = f"https://github.com/{REPO}/blob/{BRANCH}"
RAW_URL = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"

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
            # Головне: одразу додаємо raw-лінк
            github_url = f"{GITHUB_URL}/{rel_path}"
            raw_url = f"{RAW_URL}/{rel_path}"
            lines.append(f"{indent}  📄 [{f}]({github_url}) ([raw]({raw_url}))")

    return "\n".join(lines)

if __name__ == "__main__":
    print(generate_markdown_links("."))
