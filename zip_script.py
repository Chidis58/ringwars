import zipfile
import os

files_to_zip = ['GEMINI.md', 'todo.txt', 'response.txt']
for root, dirs, filenames in os.walk('sim'):
    for filename in filenames:
        files_to_zip.append(os.path.join(root, filename))

with zipfile.ZipFile('ringwars_sim.zip', 'w') as zipf:
    for file in files_to_zip:
        if os.path.exists(file):
            zipf.write(file)
            print(f"Added: {file}")
