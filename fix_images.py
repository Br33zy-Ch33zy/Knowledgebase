import os
import re

vault_path = "."

# Regex pattern to match all image link styles in your Markdown files
pattern = re.compile(r'!\[\]\((?:[^)]*?/)?(Pasted(?:%20|\s)image(?:%20|\s)[^)]+\.png)\)')

for root, dirs, files in os.walk(vault_path):
    if '.git' in root:
        continue
        
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            def replace_link(match):
                img_name = match.group(1)
                # Formats to absolute repository root path
                abs_path = f"/00-Meta/Objects/Pictures/{img_name}"
                return f"![]({abs_path})"

            new_content = pattern.sub(replace_link, content)
            
            if content != new_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Set absolute path in: {file_path}")

print("Done! All image links now use absolute repository paths.")
