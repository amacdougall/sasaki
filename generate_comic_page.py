import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader
from datetime import date

def clear_directory(directory):
    """
    Deletes contents of the target directory, but not the directory itself.
    """
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

def generate_site(data):
    """
    Generates the entire site from the supplied data. Data format is exemplified
    by input_dir/comic_data.json.
    """

    jinja_env = Environment(loader=FileSystemLoader("input_dir/templates"))
    clear_directory("output_dir")

    first_page = data["pages"][0]
    last_page = data["pages"][-1]

    for page in data["pages"]:

        template = jinja_env.get_template("page.jinja2")

        output_path = os.path.join("output_dir", page["filename"])

        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        output_file = open(output_path,"w")
        output_file.write(template.render(comic_title=data["comic_title"],
                                          date=get_date(),
                                          page=page,
                                          first_page=first_page["filename"],
                                          last_page=last_page["filename"]))
        output_file.close()

    # copy static files such as stylesheets, javascript...
    for directory in os.listdir("input_dir/static"):
        shutil.copytree(os.path.join("input_dir/static", directory),
                        os.path.join("output_dir", directory))

def get_date():
    """
    Returns a string that represents today's date
    """
    today = date.today()
    return today.strftime("%A %B %d, %Y")

# generate the site
data_path = os.path.join("input_dir", "comic_data.json")
data = json.load(open(data_path))
generate_site(data)
print "Output complete. Generated %d output pages." % len(data["pages"])
