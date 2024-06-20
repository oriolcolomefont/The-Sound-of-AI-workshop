import os
import re

input_folder = './original-abc'
output_folder = './clean1'

files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]



for file_name in files:
    with open(f'{input_folder}/{file_name}', 'r') as file:
        lines = file.readlines()
        selected = []
        for line in lines:
            if re.match(r'^[A-Z]:', line): 
                continue
            if re.match(r'^\s*$', line):
                continue 
            if re.match(r'^w:', line):
                continue
            if re.match(r'^%%', line):
                continue
            selected.append(line)

        with open(f'{output_folder}/{file_name}', 'w') as output_file:
            output_file.writelines(selected)
        print(f'Cleaned {file_name}')

