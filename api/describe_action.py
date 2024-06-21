
import subprocess

from render import render_audio_and_score
from utils import get_absolute_path_from_relative_to_source


def describe_action(melody, assets_path):
    result = get_melody_description(melody)
    melody = generate_from_description_sentence(result)
    print(f"Generated melody: {melody}")
    uuid = render_audio_and_score(melody, assets_path)
    return [melody, uuid]

def get_melody_description(melody, prompt = None):
    working_directory = "../clamp"
    cwd = get_absolute_path_from_relative_to_source(working_directory)

    music_query_path = f"{cwd}/inference/music_query.abc"
    with open(music_query_path, 'w') as file:
        file.write(melody)
    command = [
        "python", "clamp.py", 
        "-clamp_model_name", "sander-wood/clamp-small-1024", 
        "-query_modal", "music", 
        "-key_modal", "text",
        "-top_n", "5"
    ]    
    result = subprocess.run(command, capture_output=True, text=True, cwd=cwd)
    text = result.stdout
    descriptions = unique_descriptions(text)
    print (f"Descriptions: {descriptions}")
    properties = extract_abc_properties(melody)
    result = convert_to_sentence(descriptions, prompt, properties)
    return result


def generate_from_description_sentence(sentence):
    command = [
        "python", 
        "run_inference.py", 
        "-num_tunes", "1",
        "-max_length", "256",
        "-top_p", "0.9", 
        "-temperature", "1.0",
        "-seed", "0"
    ]
    working_directory = "../text-to-music"
    cwd = get_absolute_path_from_relative_to_source(working_directory)
    print(f"Generate from: {sentence}")
    input_text_path = f"{cwd}/input_text.txt"
    with open(input_text_path, 'w') as file:
        file.write(sentence)

    print(f"Running command: {command}")
    result = subprocess.run(command, capture_output=True, text=True, cwd=cwd)
    print(f"ERROR: {result.stderr}")
    music = result.stdout

    return music


def unique_descriptions(input_string):
    lines = input_string.strip().split('\n')
    unique_lines = set()
    result = []
    
    for line in lines:
        if line.startswith('Prob:'):
            # The next line is the one we need to process
            next_line = lines[lines.index(line) + 1].strip()
            if next_line not in unique_lines:
                unique_lines.add(next_line)
                result.append(next_line)
    
    return result

def extract_abc_properties(abc_string):
    lines = abc_string.strip().split('\n')
    result = []

    for line in lines:
        if line.startswith('L:'):
            note_length = line.split(':')[1].strip()
            result.append(f'Note Length-{note_length}')
        elif line.startswith('M:'):
            meter = line.split(':')[1].strip()
            result.append(f'Meter-{meter}')
        elif line.startswith('K:'):
            key = line.split(':')[1].strip()
            result.append(f'Key-{key}')
    
    return result

def convert_to_sentence(descriptions, prompt, properties):
    # Join the lines with ' and ' and form the final sentence
    sentence = " and ".join(descriptions)
    if prompt is not None:
        sentence = f"{sentence} and {prompt}"

    props = "\n".join(properties)
    return f"Write a song that is a {sentence}\n{props}"
