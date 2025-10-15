import re
import os

from convert import markdown_to_html_node

def extract_title(text):
    pattern = "^#([^#].*?)$"
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else None

def generate_page(from_path, template_path, dest_path, basepath):
    print("Generating page from", from_path, "to", dest_path, "using", template_path)
    
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)

    template = template.replace('href="/', f'href="/{basepath}/')
    template = template.replace('src="/', f'src="/{basepath}/')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if not file.endswith(".md"):
                continue
            from_path = os.path.join(root, file)
            dest_path = os.path.join(dest_dir_path, os.path.relpath(from_path, dir_path_content)).replace(".md", ".html")
            generate_page(from_path, template_path, dest_path, basepath)