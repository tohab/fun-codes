import xml.etree.ElementTree as ET
import os
from datetime import datetime
import re

def strip_html_tags(text):
    # Regular expression to remove HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def xml_to_markdown(xml_file, output_dir):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        os.makedirs(output_dir, exist_ok=True)

        for entry in root.findall('.//entry'):
            title = entry.find('title').text
            content = entry.find('content').text
            published = entry.find('published').text
            date = datetime.strptime(published, '%Y-%m-%dT%H:%M:%S')

            # Remove HTML tags from content
            if content:
                content = strip_html_tags(content)

            # Convert to markdown
            md_content = f"# {title}\n\n{date.strftime('%Y-%m-%d')}\n\n{content}"

            # Write to file
            file_name = f"{date.strftime('%Y-%m-%d')}-{title}.md"
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(md_content)

            print(f"Converted '{title}' to Markdown.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    xml_file = 'C:/Users/malat/Desktop/fun codes/blog-separator/blog-03-15-2024.xml'
    output_dir = 'C:/Users/malat/Desktop/fun codes/blog-separator/posts'
    xml_to_markdown(xml_file, output_dir)
