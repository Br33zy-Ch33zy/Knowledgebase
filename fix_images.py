import os
import re

# Path to your Vault root (current directory)
vault_path = "."

# Regular expression to handle both %20 and actual spaces in pasted images
pattern = re.compile(r'!\[\]\((Pasted(?:%20|\s)image(?:%20|\s)[^)]+\.png)\)')

for root, dirs, files in os.walk(vault_path):
    # Ignore Git folders if present
    if '.git' in root:
        continue

    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Replace the links with the absolute repo path (standardizing to %20 or keeping original)
            # This replaces the link target while ensuring clean formatting
            new_content = pattern.sub(r'![](/00-Meta/Objects/Pictures/\1)', content)

            if content != new_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated: {file_path}")

print("Done! All image links have been updated.")
