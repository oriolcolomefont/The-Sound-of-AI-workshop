from music21 import converter, metadata, note, stream

VALID_DURATIONS = [4.0, 2.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]

def clean_abc(text):
    return text

def score_to_notes_and_rests(score):
    notes_and_rests = [elem for elem in score if isinstance(elem, (note.Note, note.Rest))]
    return notes_and_rests


def convert_notes_and_rests_to_events(notes_and_rests):
    notes_and_durations = []

    for elem in notes_and_rests:
        duration = float(elem.duration.quarterLength)
        if duration not in VALID_DURATIONS:
            duration = min(VALID_DURATIONS, key=lambda x: abs(x - duration))

        if isinstance(elem, note.Note):
            notes_and_durations.append((elem.pitch.nameWithOctave, duration))
        elif isinstance(elem, note.Rest):
            notes_and_durations.append(("R", duration))

    return notes_and_durations


def convert_melody_to_abc(iter_num, notes_and_durations):
    abc_header = (
        f"X:{iter_num + 1}\n"  # Index for each generation
        f"M:4/4\n"  # Time signature
        f"L:1/4\n"  # Note length
        f"K:C\n"  # Key signature
    )    

    VALID_DURATIONS_TO_ABC = {
        4.0: "4",
        2.0: "2",
        1.0: "",
        0.5: "/2",
        0.25: "/4",
        0.125: "/8",
        0.0625: "/16",
        0.03125: "/32",
    }

    abc_notes = []
    for note, abs_duration in notes_and_durations:
        duration = VALID_DURATIONS_TO_ABC[abs_duration]
        if note == "R":
            abc_notes.append(f"z{duration}")
        else:
            note_without_octave = note[:-1]
            letter = note[0] 
            accidental = note_without_octave[1] if len(note_without_octave) > 1 else ""
            accidental = accidental.replace("#", "^")
            abc_note = f"{accidental}{letter}{duration}"
            abc_notes.append(abc_note)

    abc_score = abc_header + " ".join(abc_notes)
    return abc_score



def main(file_name):
    with open(file_name, "r") as file:
        text = file.read()
    score = converter.parse(text, format="abc")
    notes_and_rests = score_to_notes_and_rests(score.flatten())
    events = convert_notes_and_rests_to_events(notes_and_rests)
    abc = convert_melody_to_abc(0, events)
    print(abc)


if __name__ == "__main__":
    file_name = "input.abc"
    main(file_name)