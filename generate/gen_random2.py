import random

PROB_REST = 0.2  # Probability of generating a rest
MIN_BARS = 8     # Minimum number of bars in a melody
MAX_BARS = 32    # Maximum number of bars in a melody
BEATS_PER_BAR = 4  # Beats per bar, assuming 4/4 time signature
GENERATIONS = 1000  # Number of melodies to generate

def generate_random_abc(iter):
    # Define musical elements
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    durations = ['1', '2', '4']  # Note durations (quarter, half, whole)
    octaves = [",", "", "'", "''"]  # Octave indicators (lower, middle, higher)
    accidentals = ['=', '^', '_']  # Accidentals (natural, sharp, flat)

    # Randomly choose time signature
    time_signatures = ["4/4", "3/4", "2/4", "6/8", "9/8", "12/8"]
    time_signature = random.choice(time_signatures)

    # Randomly choose key signature
    keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
    key_signature = random.choice(keys)

    # Generate a random number of bars for the melody
    num_bars = random.randint(MIN_BARS, MAX_BARS)
    total_beats = num_bars * BEATS_PER_BAR

    abc_notes = []
    current_beat = 0

    while current_beat < total_beats:
        if random.random() < PROB_REST:
            duration = random.choice(durations)
            abc_notes.append(f"z/{duration}")  # Rest notation
            current_beat += int(duration)
        else:
            note = random.choice(notes)
            accidental = random.choice(accidentals)
            octave = random.choice(octaves)
            duration = random.choice(durations)
            abc_notes.append(f"{accidental}{note}{octave}/{duration}")  # Note notation
            current_beat += int(duration)

    abc_string = " ".join(abc_notes)

    # Construct ABC notation with headers
    abc_header = (
        f"X:{iter + 1}\n"  # Index for each generation
        f"T:Random-{iter + 1}\n"  # Title
        f"M:{time_signature}\n"  # Time signature
        f"L:1/4\n"  # Note length
        f"K:{key_signature}\n"  # Key signature
    )

    abc_content = abc_header + abc_string

    # Write ABC notation to file
    with open(f"output/random-{iter + 1}.abc", "w") as file:
        file.write(abc_content)

if __name__ == "__main__":
    # Generate multiple melodies
    for i in range(GENERATIONS):
        generate_random_abc(i)
