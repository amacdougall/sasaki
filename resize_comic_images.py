import sys
import os
import re
import subprocess
from clint import args

usage = """
python resize_comic_images.py [optional flags] -i input_dir -o output_dir

Reads all files from input_dir and generates identically named images in
output_dir, resized to a maximum of 960 pixels wide, or the value specified.

Flags (may occur in any order):

-i input_dir Directory from which to read files.
-o output_dir Directory to which to write files.
-w width [optional] Maximum width of generated images, in pixels. Default 960.
-n pattern [optional] Only convert files matching the supplied regex pattern.
    Pattern should not be surrounded by slashes.

Example:
python resize_comic_images.py -w 500 -i static/comic_raw -o static/comic_images
"""

def show_usage():
    "Print the usage message and exit the script."
    print usage
    sys.exit()

if args.get(0) is "--help":
    show_usage()
else:
    groups = dict(args.grouped)

    # verify and parse arguments
    if not (groups.has_key("-i") and groups.has_key("-o")):
        show_usage()
    else:
        width = groups["-w"][0] if groups.has_key("-w") else "960"
        pattern = groups["-n"][0] if groups.has_key("-n") else None
        input_dir = groups["-i"][0]
        output_dir = groups["-o"][0]

    # build command
    command = "convert {0} -resize {1}x -quality 80 {2}"

    # verify directories, creating output dir if needed
    if not os.path.exists(input_dir):
        message = "The supplied input directory did not exist: {0}"
        print message.format(input_dir)
        sys.exit()
    elif not os.path.isdir(input_dir):
        message = "The supplied input directory was not a directory: {0}"
        print message.format(input_dir)
        sys.exit()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    elif not os.path.isdir(output_dir):
        message = "The supplied output directory existed, but was not a directory: {0}"
        print message.format(output_dir)
        sys.exit()

    target_files = [filename for filename in os.listdir(input_dir)
                        if pattern is None or re.search(pattern, filename)]

    input_files = [os.path.join(input_dir, filename) for filename in target_files]
    output_files = [os.path.join(output_dir, filename) for filename in target_files]

    for input_file, output_file in zip(input_files, output_files):
        print command.format(input_file, width, output_file)
        subprocess.call(command.format(input_file, width, output_file),
                        shell=True)
