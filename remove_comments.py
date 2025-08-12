import re

with open('main_v2.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

clean_lines = []
in_docstring = False
for line in lines:
    stripped = line.strip()
    
    if '"""' in stripped:
        if in_docstring:
            in_docstring = False
            continue
        else:
            in_docstring = True
            continue
    
    if in_docstring:
        continue
    
    if stripped.startswith('#'):
        continue
    
    clean_lines.append(line)

with open('main_v2.py', 'w', encoding='utf-8') as f:
    f.writelines(clean_lines)

print("Comentários removidos do main_v2.py")
