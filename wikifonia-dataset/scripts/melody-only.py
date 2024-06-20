import os
import re

input_folder = './no-headers-no-lyrics'
output_folder = './temp-melody-only'


files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

for file_name in files:
       print(f'Processing {file_name}')
       with open(f'{input_folder}/{file_name}', 'r') as file: 
            text = file.read()        
            text = re.sub(r'"[^"]*"', '', text)
        
            with open(f'{output_folder}/{file_name}', 'w') as output_file:
                output_file.write(text)
