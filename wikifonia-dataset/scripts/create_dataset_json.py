import json
import os

input_folder = './temp'
token_list = "token_list.json"
dataset_json = "dataset.json"

files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

tokens = set()

min_melody_length = float('inf')
max_melody_length = 0

for file_name in files:
    with open(f'{input_folder}/{file_name}', 'r') as file:
        text = file.read()
        items = text.split()
        max_melody_length = max(max_melody_length, len(items))
        min_melody_length = min(min_melody_length, len(items))
        tokens.update(items)

with open(dataset_json, 'w') as file:
    file.write(json.dumps({
        "token_list": "token_list.json",
        "dataset_folder": "temp",
        "number_of_melodies": len(files),
        "number_of_tokens": len(tokens),
        "min_melody_length": min_melody_length, 
        "max_melody_length": max_melody_length,
        "file_list": list(files),
    }))

with open(token_list, 'w') as file:
    file.write(json.dumps(list(tokens)))

