
import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.splitlines()

    for line in lines:
        if line.startswith("# ") and not line.startswith("##"):
            return line[2:].strip()

    raise Exception("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} "
        f"using {template_path}"
    )

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(
    dir_path_content,
    template_path,
    dest_dir_path
):
    for entry in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(content_path):
            if entry.endswith(".md"):
                dest_path = dest_path.removesuffix(".md") + ".html"

                generate_page(
                    content_path,
                    template_path,
                    dest_path
                )

        elif os.path.isdir(content_path):
            os.makedirs(dest_path, exist_ok=True)

            generate_pages_recursive(
                content_path,
                template_path,
                dest_path
            )
