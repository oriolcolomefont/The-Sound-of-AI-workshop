from music21 import converter
from melodic_scheleton import filter_score


# Load the MusicXML file into a Score object
score = converter.parse(file_path, )

# Apply filtering or manipulation rules
filtered_score = filter_score(score)

# Save the modified score to a new MusicXML file
modified_file_path = f'modified_{file_path}'
score.write('musicxml', modified_file_path)