import os
import json

data_path = os.path.join("input_dir", "comic_data.json")
data = json.load(open(data_path))

header = data["header"]

for page in data["pages"]:
    template_path = os.path.join("input_dir", "comic_template.html")
    template = open(template_path)

    output_path = os.path.join("output_dir", page["filename"])
    output_file = open(output_path,"w")

    for line in template:
        line = line.replace("${header}", header)
        line = line.replace("${page_title}", page["page_title"])
        line = line.replace("${page_content}", page["page_content"])
        line = line.replace("${next_page}", page["next_page"])
        line = line.replace("${previous_page}", page["previous_page"])
        output_file.write(line)

    template.close()
    output_file.close()
