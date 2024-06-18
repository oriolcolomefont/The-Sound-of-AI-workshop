import random

PROB_REST = 0.2
GENERATIONS = 10

def generate_random_abc(iter, number_of_items):
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    durations = ['1', '2', '4', '8', '16']
    accidentals = ['=', '^', '_']
    octaves = [",", "", "", "", "'"]

    abc_notes = []
    for _ in range(number_of_items):
        if random.random() < PROB_REST:
            duration = random.choice(durations)
            abc_notes.append(f"z/{duration}")
            continue
        note = random.choice(notes)
        accidental = random.choice(accidentals)
        octave = random.choice(octaves)
        duration = random.choice(durations)
        abc_notes.append(f"{accidental}{note}{octave}/{duration}")

    abc_string = " ".join(abc_notes)
    
    abc_header = (
        "X:1\n"
        f"T:Random-{iter}\n"
        "M:4/4\n"
        "L:1/4\n"
        "K:C\n"
    )
    
    abc_content = abc_header + abc_string
    
    with open(f"output/random-{iter}.abc", "w") as file:
        file.write(abc_content)

if __name__ == "__main__":
    for i in range(GENERATIONS):
        generate_random_abc(i, 10)
