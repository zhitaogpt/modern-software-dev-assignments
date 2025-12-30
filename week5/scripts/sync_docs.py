import json
import sys
import os
from pathlib import Path

# Add the repository root to sys.path so we can import week5
repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root))

# Change directory to week5 so that relative paths in the app (like 'frontend') work
os.chdir(repo_root / "week5")
sys.path.append(os.getcwd())

try:
    from backend.app.main import app
except ImportError as e:
    print(f"Error importing app: {e}")
    sys.exit(1)

def generate_markdown(openapi_spec):
    md = "# API Documentation\n\n"
    md += f"**Title:** {openapi_spec.get('info', {}).get('title', 'API')}\n"
    md += f"**Version:** {openapi_spec.get('info', {}).get('version', '0.0.0')}\n\n"
    
    paths = openapi_spec.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            method_upper = method.upper()
            summary = details.get('summary', 'No summary')
            description = details.get('description', '')
            
            md += f"## {method_upper} `{path}`\n\n"
            md += f"**Summary:** {summary}\n\n"
            if description:
                md += f"{description}\n\n"
            
            # Parameters
            params = details.get('parameters', [])
            if params:
                md += "### Parameters\n\n"
                md += "| Name | In | Required | Description |\n"
                md += "| :--- | :--- | :--- | :--- |\n"
                for p in params:
                    name = p.get('name')
                    loc = p.get('in')
                    req = "Yes" if p.get('required') else "No"
                    desc = p.get('description', '-')
                    md += f"| {name} | {loc} | {req} | {desc} |\n"
                md += "\n"
            
            md += "---\n\n"
            
    return md

def main():
    print("Generating OpenAPI spec...")
    openapi_spec = app.openapi()
    
    print("Converting to Markdown...")
    md_content = generate_markdown(openapi_spec)
    
    output_path = repo_root / "week5" / "docs" / "API.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(md_content)
    
    print(f"Successfully wrote API documentation to {output_path}")

if __name__ == "__main__":
    main()
