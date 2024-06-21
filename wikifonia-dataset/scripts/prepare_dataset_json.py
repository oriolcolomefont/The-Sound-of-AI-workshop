import json
import os

input_folder = './temp-melody-only'
token_list = "token_list.json"
dataset_json = "dataset.json"

MAX_LEN = 100

all_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
files = []

tokens = set()

min_melody_length = float('inf')
max_melody_length = 0

for file_name in all_files:
    with open(f'{input_folder}/{file_name}', 'r') as file:
        text = file.read()
        items = text.split()
        if len(items) > MAX_LEN:
            continue
        files.append(file_name)
        max_melody_length = max(max_melody_length, len(items))
        min_melody_length = min(min_melody_length, len(items))
        tokens.update(items)

with open(dataset_json, 'w') as file:
    file.write(json.dumps({
        "token_list": "token_list.json",
        "max_melody_length": MAX_LEN,
        "dataset_folder": input_folder.replace("./", ""),
        "number_of_melodies": len(files),
        "number_of_tokens": len(tokens),
        "min_melody_length": min_melody_length, 
        "max_melody_length": max_melody_length,
        "file_list": list(files),
    }))

with open(token_list, 'w') as file:
    file.write(json.dumps(list(tokens)))

