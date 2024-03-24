import os
import re

# Input file path
input_file = r"C:\Users\malat\Desktop\fun codes\blog-backup\all-posts.md"

# Output directory path
output_dir = r"C:\Users\malat\Desktop\fun codes\blog-backup\output"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open the input file with UTF-8 encoding
with open(input_file, 'r', encoding='utf-8') as f:
    # Read the content of the file
    content = f.readlines()

# Initialize variables
current_output_file = None
current_title = None

# Iterate through the lines
for line in content:
    # Check if the line starts with "## "
    match = re.match(r'##\s+(.+)', line)
    if match:
        # Close the current output file if it exists
        if current_output_file:
            current_output_file.close()

        # Extract the title
        title = match.group(1)
        title = title.replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
        # Create the output file path
        output_file = os.path.join(output_dir, f"{title}.md")
        # Open a new output file with UTF-8 encoding and write the header
        current_output_file = open(output_file, 'w', encoding='utf-8')
        current_output_file.write(line)
        current_title = title
    elif current_title:
        # Write the line to the current output file with UTF-8 encoding
        current_output_file.write(line)

# Close the last output file
if current_output_file:
    current_output_file.close()
