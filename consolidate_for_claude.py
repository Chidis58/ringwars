import os

output_file = 'sim_source_for_claude.txt'
base_dir = '.'
files_to_include = ['README.md', 'GEMINI.md', 'todo.txt', 'response.txt']

# Get all .py files in sim directory
for root, dirs, files in os.walk('sim'):
    for file in files:
        if file.endswith('.py'):
            files_to_include.append(os.path.join(root, file))

with open(output_file, 'w') as out:
    out.write("--- RINGWARS PROJECT CONSOLIDATED SOURCE ---\n")
    out.write("--- DIRECTORY TREE ---\n")
    
    # Simple tree visualization
    for root, dirs, files in os.walk('sim'):
        level = root.replace('sim', '').count(os.sep)
        indent = ' ' * 4 * (level)
        out.write(f"{indent}{os.path.basename(root)}/\n")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f.endswith('.py'):
                out.write(f"{subindent}{f}\n")
    
    out.write("\n\n")

    for file_path in files_to_include:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            out.write(f"--- FILE: {file_path} ---\n")
            with open(file_path, 'r') as f:
                out.write(f.read())
            out.write(f"\n--- END OF {file_path} ---\n\n")

print(f"Consolidated file created: {output_file}")
