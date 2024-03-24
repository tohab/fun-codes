import os
import re
from dateutil.parser import parse
import shutil

def copy_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                match = re.search(r'\[\[?(.*?)\]?\]\(.*?\)', content)
                date = re.search(r'(\w+ \d+ \w+ \d{4})', content)

                if match and date:
                    title = match.group(1)
                    date = parse(date.group(1), fuzzy=True).strftime("%Y-%m-%d")
                    new_filename = f"{date}-{title}"
                    new_filename = re.sub(r'\W+', '-', new_filename)  # replace non-alphanumeric characters with '-'
                    new_filename += ".md"
                    shutil.copy(os.path.join(directory, filename), os.path.join(directory, new_filename))

# Call the function with the directory path
copy_files('output')
