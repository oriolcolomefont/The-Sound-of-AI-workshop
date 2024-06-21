import os

input_folder = './temp-melody-only'
output_folder = './temp-melody-divided'

DIVIDE_THRESHOLD = 100

files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

def divide_string(s):
    parts = []
    while len(s) > 100:
        # Find the last space character within the first 100 characters
        break_point = s.rfind(' ', 0, 100)
        if break_point == -1:
            # If no space is found, split at 100th character to avoid infinite loop
            break_point = 100
        parts.append(s[:break_point])
        s = s[break_point:].lstrip()  # Remove leading spaces from the remaining string
    parts.append(s)  # Add the last part
    return parts

for file_name in files:
    with open(f'{input_folder}/{file_name}', 'r') as file:
        text = file.read()
        if len(text) < DIVIDE_THRESHOLD:
            print(f'Not needed: {file_name} {len(text)}')
            with open(f'{output_folder}/{file_name}', 'w') as output_file:
                output_file.write(text)
            continue

        print(f'Processing {file_name} {len(text)}')
        parts = divide_string(text)
        for i in range(len(parts)):
            with open(f'{output_folder}/{file_name}_{i}', 'w') as output_file:
                output_file.write(parts[i])


