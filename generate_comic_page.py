import os
import json
import shutil

def generate_site(data):
    """
    Generates the entire site from the supplied data. Data format is exemplified
    by input_dir/comic_data.json.
    """

    header = data["header"]

    path_exists = os.path.exists("output_dir")
    
    if path_exists:
        shutil.rmtree("output_dir")

    os.mkdir("output_dir")

    for page in data["pages"]:
        template_path = os.path.join("input_dir", "comic_template.html")
        template = open(template_path)

        output_path = os.path.join("output_dir", page["filename"])
        output_file = open(output_path,"w")

        for line in template:
            if "${nav}" in line:
                content = build_nav(page)
            elif "${" in line:
                content = replace_tokens(line, page, header)
            else:
                content = line

            output_file.write(content)

        template.close()
        output_file.close()

def replace_tokens(line, page, header):
    """
    Replaces standard tokens with page content, where found.
    """
    line = line.replace("${header}", header)
    line = line.replace("${title}", page["title"])
    line = line.replace("${content}", page["content"])
    return line

def build_nav(page):
    """
    Generates a navigation block for the supplied page.
    """
    if page.has_key("nav_template"):
        nav_template_filename = page["nav_template"]
    else:
        nav_template_filename = "nav_template.html"

    nav_template_path = os.path.join("input_dir", nav_template_filename)
    nav_template = open(nav_template_path)

    content_lines = []

    for line in nav_template:
        line = line.replace("${next_page}", page["next_page"])
        line = line.replace("${previous_page}", page["previous_page"])
        content_lines.append(line)

    nav_template.close()
    return "".join(content_lines)

# generate the site
data_path = os.path.join("input_dir", "comic_data.json")
data = json.load(open(data_path))
generate_site(data)
