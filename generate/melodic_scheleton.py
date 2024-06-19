from music21 import converter, note, chord, stream

def filter_score(score):
    for part in score.parts:
        for measure in part.getElementsByClass('Measure'):
            for note_or_rest in measure.notesAndRests:
                if isinstance(note_or_rest, note.Note):
                    # Check if the note is on a strong beat (beat 1, 2, 3, or 4) or tied to the next note
                    if note_or_rest.beat % 1.0 == 0 or note_or_rest.tie is not None:
                        # Keep the note
                        pass
                    else:
                        # Replace with a rest of the same duration
                        new_rest = note.Rest()
                        new_rest.duration = note_or_rest.duration
                        measure.replace(note_or_rest, new_rest)
                elif isinstance(note_or_rest, note.Rest):
                    # Keep rests as they are
                    pass

def main():
    # Replace 'path_to_your_musicxml_file.xml' with your actual file path
    file_path = 'markov.mxl'
    
    # Load the MusicXML file into a Score object
    score = converter.parse(file_path)

    # Apply filtering or manipulation rules
    filter_score(score)

    # Save the modified score to a new MusicXML file
    modified_file_path = 'modified_musicxml_file.xml'
    score.write('musicxml', modified_file_path)

    # Show the modified score (display as sheet music)
    score.show()

if __name__ == '__main__':
    main()