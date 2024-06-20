
import subprocess

from clean_action import remove_chords
from render import render_audio_and_score
from utils import create_uuid, get_absolute_path_from_relative_to_source


def generate_score_action(prompt, assets_path):
    lib_path = '../tunesformer'
    cwd = get_absolute_path_from_relative_to_source(lib_path)
    prompt_path = f"{cwd}/prompt.txt"

    # with open(prompt_path, 'w') as file:
    #     file.write("Generate a new tune.")

    command = [
        "python", "generate.py",
        "-num_tunes", "1", 
        "-max_patch", "128",
        "-top_p", "0.8", 
        "-top_k", "8",
        "-temperature", "1.2", 
        "-seed", "0", 
        "-show_control_code", "False"
    ]
    result = subprocess.run(command, capture_output=True, text=True, cwd=cwd)
    song= extract_abc_song(result.stdout)
    melody = remove_chords(song)
    print(f"Generated MELODY: {melody}")
    uuid = render_audio_and_score(melody, assets_path)
    uuid = create_uuid(melody)
    return [melody, uuid]

def extract_abc_song(output):
    lines = output.split('\n')
    result_lines = []
    found_x1 = False
    
    for line in lines:
        if not found_x1:
            if line.startswith("X:1"):
                found_x1 = True
                result_lines.append(line)
        elif line.startswith("X:2"):
            break
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)