import os
import yaml
import re
import sys

DOCS_URL = os.getenv('DOCS_URL', 'https://developer.gov.bc.ca/docs/default/component/aps-infra-platform-docs')

def load_definitions(config_file):
    try:
        with open(config_file, 'r') as f:
            config = f.read()
            config = config.replace('{DOCS_URL}', DOCS_URL)
            config = yaml.safe_load(config)
            return config.get("terms", {})
    except Exception as e:
        print("Error loading configuration file:", e)
        sys.exit(1)

def substitute_links(markdown_file, definitions):
    try:
        with open(markdown_file, 'r') as f:
            content = f.read()

        for term_id, term_data in definitions.items():
            pattern = r'\{\{ glossary_tooltip term_id="' + term_id + r'"\s*(?:text="([^"]+)")?\s*\}\}'            
            matches = re.findall(pattern, content)

            for match in matches:
                 # Use name if text is not provided
                term_text = match if match else term_data["name"]

                if term_data["url"]:
                    link_tag = f'<a href="{term_data["url"]}" title="{term_data["def"]}" target="_blank" style="text-decoration: none !important; color: inherit; border-bottom: 1px dotted;">{term_text}</a>'
                else:
                    # If no url, just create tooltip
                    link_tag = f'<span title="{term_data["def"]}" style="border-bottom: 1px dotted;">{term_text}</span>'
                
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

def yaml_to_md_glossary(yaml_file):
    with open(yaml_file, 'r') as f:
        data = f.read()
        data = data.replace('{DOCS_URL}', DOCS_URL)
        data = yaml.safe_load(data)
    
    markdown_table = "---\ntitle: Glossary\n---\n\n|Term|Definition|\n|:----|:----|\n"
    
    for term, details in data['terms'].items():
        markdown_table += f"|{details['name']}|{details['def']}|\n"
    
    return markdown_table

def save_to_file(markdown_table, output_file):
    with open(output_file, 'w') as f:
        f.write(markdown_table)
    print("Glossary created at:", output_file)

def main():
    reference_file = 'scripts/glossary_reference.yaml'
    definitions = load_definitions(reference_file)
    
    # produce glossary
    markdown_table = yaml_to_md_glossary(reference_file)
    output_file = 'documentation/reference/glossary.md'
    save_to_file(markdown_table, output_file)

    # substitute docs
    documentation_folder = 'documentation'
    process_markdown_files(documentation_folder, definitions)

if __name__ == "__main__":
    main()
