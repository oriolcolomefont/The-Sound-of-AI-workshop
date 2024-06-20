import os
import random

input_folder = './no-headers-no-lyrics'
output_folder = './temp'

number_of_items_to_remove = 4


files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

for file_name in files:
       print(f'Processing {file_name}')
       with open(f'{input_folder}/{file_name}', 'r') as file: 
            text = file.read()
            items = text.split()

            number_of_items = len(items)

            for i in range(number_of_items_to_remove):
                remove_index = random.randint(0, number_of_items - 1)
                items.pop(remove_index)
                number_of_items -= 1
            
            new_text = ' '.join(items)
            with open(f'{output_folder}/{file_name}', 'w') as output_file:
                output_file.write(new_text)




