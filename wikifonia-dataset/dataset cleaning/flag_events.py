import os
import json
from music21 import converter, note


def flag_score(score):
    flag_array = []  # Initialize an empty list to store boolean values
    
    for part in score.parts:
        for measure in part.getElementsByClass('Measure'):
            for note_or_rest in measure.notesAndRests:
                if isinstance(note_or_rest, note.Note):
                    if note_or_rest.beat % 1.0 == 0 or note_or_rest.tie is not None:
                        flag_array.append(True)  # Flag as True if note meets condition
                    else:
                        flag_array.append(False)  # Flag as False if note does not meet condition
                elif isinstance(note_or_rest, note.Rest):
                    flag_array.append(True)  # Flag rests as True (they are kept)
    
    return flag_array

# Function to process ABC files in a folder and save results to JSON
def process_abc_folder(folder_path, output_file):
    results = {}

    # Iterate through files in the folder
    for filename in os.listdir(folder_path)[0:10]:
        if filename.endswith(".abc"):
            file_path = os.path.join(folder_path, filename)
            try:
                # Parse the ABC file
                score = converter.parse(file_path)
                
                # Flag elements in the score
                flag_array = flag_score(score)
                
                # Store results in dictionary
                results[filename] = flag_array
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    # Save results to JSON file
    with open(output_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)
    
    print(f"Processed {len(results)} ABC files. Results saved to {output_file}")

# Example usage:
if __name__ == "__main__":
    abc_folder = '../original-abc'  # Replace with the path to your folder containing ABC files
    output_json = '../flagged-events/flagged-events.json'  # Name of the output JSON file
    
    process_abc_folder(abc_folder, output_json)