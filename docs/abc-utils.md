# ABC Utilities Documentation

## Overview
The ABC utilities component provides a comprehensive set of tools for working with ABC notation, including parsing, manipulation, conversion, and validation of ABC musical scores.

## Features
- ABC notation parsing and validation
- Format conversion (ABC ↔ MIDI ↔ MusicXML)
- Score manipulation and transformation
- Audio synthesis from ABC notation

## Core Utilities

### ABC Parser
```python
from abc_utils.parser import ABCParser

parser = ABCParser()
score = parser.parse("X:1\\nT:Example\\nK:C\\nCDEF|")
```

### Format Conversion
```python
from abc_utils.converter import ABCConverter

converter = ABCConverter()

# ABC to MIDI
midi_data = converter.to_midi("X:1\\nK:C\\nCDEF|")

# MIDI to ABC
abc_notation = converter.from_midi("input.mid")

# ABC to MusicXML
xml_data = converter.to_musicxml("X:1\\nK:C\\nCDEF|")
```

## ABC Notation Reference

### Header Fields
```abc
X: <reference number>
T: <title>
C: <composer>
M: <meter>
L: <default note length>
Q: <tempo>
K: <key>
```

### Musical Elements
```abc
# Notes and durations
C    # quarter note C
C2   # half note C
C/2  # eighth note C
^C   # C sharp
_C   # C flat

# Bars and repeats
|    # bar line
:|   # end repeat
|:   # start repeat
||   # double bar line

# Chords and ornaments
[CEG]   # C major chord
+trill+ # trill ornament
~       # general ornament
```

## Validation

### Score Validation
```python
from abc_utils.validator import ABCValidator

validator = ABCValidator()
is_valid = validator.validate_score(abc_string)
errors = validator.get_validation_errors(abc_string)
```

### Common Validation Rules
1. Required header fields
2. Valid key signatures
3. Bar length consistency
4. Note duration validity
5. Repeat structure integrity

## Transformation Tools

### Transposition
```python
from abc_utils.transform import ABCTransformer

transformer = ABCTransformer()
transposed = transformer.transpose(
    abc_string,
    semitones=2  # Up two semitones
)
```

### Other Transformations
```python
# Double tempo
doubled = transformer.scale_tempo(abc_string, factor=2.0)

# Change meter
new_meter = transformer.change_meter(abc_string, "6/8")

# Simplify notation
simplified = transformer.simplify_notation(abc_string)
```

## Audio Synthesis

### Basic Synthesis
```python
from abc_utils.synth import ABCSynthesizer

synth = ABCSynthesizer()
wav_data = synth.synthesize(
    abc_string,
    soundfont="path/to/soundfont.sf2"
)
```

### Advanced Synthesis Options
```python
# With specific instrument
wav_data = synth.synthesize(
    abc_string,
    instrument=0,  # Piano
    reverb=0.3,
    tempo_factor=1.2
)

# Multi-track synthesis
wav_data = synth.synthesize_multi(
    abc_string,
    instruments=[0, 48],  # Piano and String
    mix_levels=[1.0, 0.8]
)
```

## Integration Examples

### Web API Integration
```python
@app.post("/convert/abc-to-midi")
async def convert_endpoint(
    abc_notation: str,
    output_format: str = "midi"
) -> bytes:
    converter = ABCConverter()
    return converter.to_midi(abc_notation)
```

### Batch Processing
```python
def process_abc_files(input_dir: str, output_dir: str):
    converter = ABCConverter()
    for abc_file in Path(input_dir).glob("*.abc"):
        midi_data = converter.to_midi(abc_file.read_text())
        output_path = Path(output_dir) / f"{abc_file.stem}.mid"
        output_path.write_bytes(midi_data)
```

## Error Handling

### Common Issues
1. Invalid ABC syntax
2. Inconsistent bar lengths
3. Invalid key signatures
4. Synthesis errors

### Error Recovery
```python
try:
    score = parser.parse(abc_string)
except ABCSyntaxError as e:
    # Attempt to fix common syntax issues
    fixed_abc = parser.auto_fix(abc_string)
    score = parser.parse(fixed_abc)
```

## Performance Optimization
- Caching of parsed scores
- Batch processing for multiple files
- Memory-efficient streaming for large files
- Parallel processing support

## Best Practices
1. Always validate ABC input
2. Use appropriate error handling
3. Cache parsed results when possible
4. Handle encoding issues properly
5. Implement proper cleanup for temporary files 