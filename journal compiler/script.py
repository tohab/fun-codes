# Take all .odt and .docx files and use markdown pandoc to output them into markdown files in this folder of the same name
# "G:\My Drive\creative\digital journals"
# I'm on windows vscodes

import os
import pypandoc

# Directory containing the .odt and .docx files
directory = r"G:\My Drive\creative\digital journals"

# Function to convert files to markdown
def convert_to_markdown(file_path):
    try:
        output_file = os.path.splitext(file_path)[0] + ".md"
        pypandoc.convert_file(file_path, 'md', outputfile=output_file)
        print(f"Converted {file_path} to Markdown successfully.")
    except Exception as e:
        print(f"Error converting {file_path}:", e)

# Iterate through files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".odt") or filename.endswith(".docx"):
        file_path = os.path.join(directory, filename)
        convert_to_markdown(file_path)
