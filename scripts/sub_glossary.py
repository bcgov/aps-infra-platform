import os
import yaml
import re
import sys

def load_definitions(config_file):
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            return config.get("terms", {})
    except Exception as e:
        print("Error loading configuration file:", e)
        sys.exit(1)

def substitute_links(markdown_file, definitions):
    try:
        with open(markdown_file, 'r') as f:
            content = f.read()

        for term_id, term_data in definitions.items():
            pattern = r'\{\{ glossary_tooltip text="([^"]+)" term_id="' + term_id + r'" \}\}'
            matches = re.findall(pattern, content)

            for match in matches:
                # Create the link tag
                link_tag = f'<a href="{term_data["url"]}" title="{term_data["def"]}" style="text-decoration: none !important; color: inherit; border-bottom: 1px dotted;">{match}</a>'
                # Replace the placeholder with the link tag
                content = re.sub(pattern, link_tag, content, count=1)

        return content
    except Exception as e:
        print("Error substituting links in", markdown_file, ":", e)
        sys.exit(1)

def process_markdown_files(root_folder, definitions):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".md"):
                markdown_file = os.path.join(root, file)
                try:
                    modified_content = substitute_links(markdown_file, definitions)
                    with open(markdown_file, 'w') as f:
                        f.write(modified_content)
                    print("Links substituted successfully in", markdown_file)
                except Exception as e:
                    print("Error processing", markdown_file, ":", e)

def main():
    config_file = 'scripts/terms.yaml'
    definitions = load_definitions(config_file)

    documentation_folder = 'documentation'
    process_markdown_files(documentation_folder, definitions)

if __name__ == "__main__":
    main()
