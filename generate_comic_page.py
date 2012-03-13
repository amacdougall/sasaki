import os

import json

data = json.load(open("comic_website_generator.json"))

header = data["header"]

for page in data["pages"]:


    template = open("comic_template.html")

    output_file = open(page["filename"], "w")


    for line in template:

        line = line.replace("${header}", header)
        line = line.replace("${page_title}", page["page_title"])
        line = line.replace("${page_content}", page["page_content"])
	line = line.replace("${next_page}", page["next_page"])
	line = line.replace("${previous_page}", page["previous_page"])

        output_file.write(line)
    

    template.close()

    output_file.close()
