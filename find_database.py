
import os

print("SEARCHING FOR DATABASE FILES...")
print("-" * 40)

for root, dirs, files in os.walk("."):
    # Skip virtual environments and Git folders
    dirs[:] = [
        d for d in dirs
        if d not in [".git", ".venv", "__pycache__"]
    ]

    for file in files:
        if file.lower().endswith((".db", ".sqlite", ".sqlite3")):
            print(os.path.join(root, file))

print("\nSEARCH COMPLETE!")
