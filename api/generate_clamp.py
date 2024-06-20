
import random
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

NUMBER_OF_VARIATIONS = 100


def generate_clamp_action(melody, prompt, assets_path):
    print(">>> GENERATING VARIATIONS")
    generate_variations(melody, NUMBER_OF_VARIATIONS)

    header = extract_abc_header(melody)
    print(">>> GENERATING MELODY DESCRIPTION")
    description = get_melody_description(melody, prompt)
    print("PROMPT: ", description)



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

def generate_variations(melody, number_of_variations):
    header = extract_abc_header(melody)
    clamp_path = '../clamp'
    cwd = get_absolute_path_from_relative_to_source(clamp_path)
    music_keys_folder = f"{cwd}/inference/music_keys"
    command = ['rm', '-r', music_keys_folder]
    subprocess.run(command)
    # create the folder back
    command = ['mkdir', music_keys_folder]
    subprocess.run(command)
    # Read the score and process events
    score = converter.parse(melody, type='abc')
    notes_and_rests = score_to_notes_and_rests(score.flatten())
    events = convert_notes_and_rests_to_events(notes_and_rests)
    unique_events = list(set(events))
    number_of_events = len(events)
    # Create markov chain
    markov = MarkovChain(unique_events, 0.1)
    markov.train(events)
    markov.normalize_matrix()

    importance_array = get_importance_array(score)

    for i in range(number_of_variations):
        markov_melody = generate_melody(events, markov, importance_array)
        markov_abc_melody = convert_events_to_abc_melody(markov_melody)
        markov_abc_score = header + "\n" + " ".join(markov_abc_melody)
        markov_uuid = create_uuid(markov_abc_score)

        file_path = f"{music_keys_folder}/{markov_uuid}.abc"
        # create the file and write
        with open(file_path, 'w') as file:
            file.write(markov_abc_score)

def generate_melody(events, markov, importance_array):
    last_note = random.choice(events)
    melody = []
    for i in range(len(events)):
        current_note = events[i]
        if importance_array[i] == True:
            last_note = current_note
        else:
            last_note = markov.generate_single_note(last_note)
        melody.append(last_note)
    return melody


def get_importance_array(score):
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
L:1/4
M:4/4
K:C
|:"C" c3/2 G/ E2- | E2 (3c d c |"E7" B3/2 ^G/ E2- | E4 |"A7" A3/2 G/ E2- | E ^D (3E _B A | %6
w: All of me|* why not take|all of me?|_|Can't you see|_ I'm no good with-|
"Dm7" G2 F2- | F4 |"E7" E3/2 _E/ D2- | D2 (3E ^G B |"Am" d2 c2- | c4 |"D7" B3/2 _B/ A2- | %13
    """
    assets_path = "../client/public/assets"
    prompt = "make it more folk"
    generate_clamp_action(abc_melody, prompt, assets_path)