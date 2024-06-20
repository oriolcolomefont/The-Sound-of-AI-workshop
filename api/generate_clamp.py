
import re
import subprocess

from describe_action import get_melody_description
from markov import MarkovChain
from music21 import converter, metadata, note, stream
from render import render_audio_and_score
from utils import create_uuid, get_absolute_path_from_relative_to_source
from variate_action import (convert_events_to_abc_melody,
                            convert_notes_and_rests_to_events,
                            extract_abc_header, score_to_notes_and_rests)


def generate_clamp_action(melody, prompt, assets_path):
    header = extract_abc_header(melody)
    print(">>> GENERATING MELODY DESCRIPTION")
    description = get_melody_description(melody, prompt)
    print("PROMPT: ", description)

    print(">>> GENERATING VARIATIONS")
    generale_variations(melody, 100)


    # inference_cache_folder = f"{cwd}/inference/cache"
    # command = ['rm', '-r', inference_cache_folder]


    print(">>> SEARCH VARIATIONS BY MUSIC SIMILARITY....")
    music_query_results = find_variation_by_music_query(melody)
    print(">>> MUSIC QUERY RESULTS: ", music_query_results)

    print(">>> SEARCH VARIATIONS BY TEXT QUERY....")
    text_query_results = find_variations_by_text_query(description)
    print(">>> TEXT QUERY RESULTS: ", music_query_results)

    # join both results
    results = music_query_results + text_query_results
    # sort by first pair (similarity)
    results = sorted(results, key=lambda x: x[0], reverse=False)

    # take first
    uuid = results[0][1]
    clamp_path = '../clamp'
    cwd = get_absolute_path_from_relative_to_source(clamp_path)
    variation_file = f"{cwd}/inference/music_keys/{uuid}.abc"
    with open(variation_file, 'r') as file:
        variation = file.read()

    variation_abc = header + "\n" + variation
    print(">>> SELECTED VARIATION: ", variation_abc)

    uuid = render_audio_and_score(variation_abc, assets_path)
    return [melody, uuid]

def generale_variations(melody, number_of_variations):
    clamp_path = '../clamp'
    cwd = get_absolute_path_from_relative_to_source(clamp_path)
    music_keys_folder = f"{cwd}/inference/music_keys"
    command = ['rm', '-r', music_keys_folder]
    subprocess.run(command)
    # create the folder back
    command = ['mkdir', music_keys_folder]
    subprocess.run(command)
    [markov, unique_events, number_of_events] = get_markov(melody)
    header = extract_abc_header(melody)

    for i in range(number_of_variations):
        markov_melody = markov.generate_melody(unique_events, number_of_events)
        markov_abc_melody = convert_events_to_abc_melody(markov_melody)
        markov_abc_score = header + "\n" + " ".join(markov_abc_melody)
        markov_uuid = create_uuid(markov_abc_score)

        file_path = f"{music_keys_folder}/{markov_uuid}.abc"
        # create the file and write
        with open(file_path, 'w') as file:
            file.write(markov_abc_score)



def get_markov(abc_melody):
    score = converter.parse(abc_melody, type='abc')
    notes_and_rests = score_to_notes_and_rests(score.flatten())
    events = convert_notes_and_rests_to_events(notes_and_rests)
    unique_events = list(set(events))
    markov = MarkovChain(unique_events, 0.1)

    markov.train(events)
    markov.normalize_matrix()
    return [markov, unique_events, len(events)]

def find_variation_by_music_query(melody):
    clamp_path = '../clamp'
    cwd = get_absolute_path_from_relative_to_source(clamp_path)    
    music_query_path = f"{cwd}/inference/music_query.abc"
    with open(music_query_path, 'w') as file:
        file.write(melody)
    command = [
        "python", "clamp.py", 
        "-clamp_model_name", "sander-wood/clamp-small-1024", 
        "-query_modal", "music", 
        "-key_modal", "music",
        "-top_n", "5"
    ]    
    result = subprocess.run(command, capture_output=True, text=True, cwd=cwd)
    return extract_similarity_uuid_pairs(result.stdout)

def find_variations_by_text_query(query_text):
    clamp_path = '../clamp'
    cwd = get_absolute_path_from_relative_to_source(clamp_path)    
    text_query_path = f"{cwd}/inference/text_query.txt"
    with open(text_query_path, 'w') as file:
        file.write(query_text)
    command = [
        "python", "clamp.py", 
        "-clamp_model_name", "sander-wood/clamp-small-1024", 
        "-query_modal", "text", 
        "-key_modal", "music",
        "-top_n", "5"
    ]    
    result = subprocess.run(command, capture_output=True, text=True, cwd=cwd)
    return extract_similarity_uuid_pairs(result.stdout)    

def extract_similarity_uuid_pairs(input_string):
    lines = input_string.strip().split('\n')
    pairs = []

    for line in lines:
        if line.startswith('Prob:'):
            # Extract the similarity score
            similarity_match = re.search(r'Sim: ([\d.]+)', line)
            if similarity_match:
                similarity = similarity_match.group(1)
                
                # Find the next line ending with .abc
                index = lines.index(line) + 1
                if index < len(lines) and lines[index].endswith('.abc'):
                    uuid_match = re.search(r'[^/]+\.abc$', lines[index])
                    if uuid_match:
                        uuid = uuid_match.group(0).replace('.abc', '')
                        pairs.append((similarity, uuid))

    return pairs

if __name__ == "__main__":
    abc_melody = """
X:1
L:1/8
Q:1/4=120
M:4/4
K:F
A, |"Eb7" (3B,_DF c4 BF |"Dm" ^G A3- A3 A, |"Eb7" (3B,_DF c4 BF |"Dm" A4 z2 z A, |  "Eb7" (3B,_DF c4 BF |"Dm" ^G A3- A4 |"Em7b5" ABAG"A7b5" _E2 ^CD- |"Dm" D4 z2 z A, |     
    """
    assets_path = "../client/public/assets"
    prompt = "make it more folk"
    generate_clamp_action(abc_melody, prompt, assets_path)