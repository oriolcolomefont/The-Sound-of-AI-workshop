# Text-to-Music Generation Documentation

## Overview
The text-to-music generation component converts natural language descriptions into musical pieces using advanced language models and music generation techniques. It enables users to create music by describing their desired musical characteristics in plain text.

## Features
- Natural language to ABC notation conversion
- Style-aware music generation
- Controllable generation parameters
- Multi-modal conditioning

## Architecture

### Model Architecture
- Base: GPT-style transformer
- Context window: 1024 tokens
- Vocabulary: Combined text and music tokens
- Training: Large-scale text-music pair dataset

### Generation Pipeline
1. Text Processing
   - Natural language parsing
   - Musical term extraction
   - Style identification

2. Music Generation
   - Token generation
   - Structure enforcement
   - Musical coherence checking

3. Post-processing
   - ABC notation formatting
   - Validation
   - Optional MIDI conversion

## Usage

### Basic Generation
```bash
python run_inference.py \
    -num_tunes 3 \
    -max_length 1024 \
    -top_p 0.9 \
    -temperature 1.0 \
    -seed 0
```

### Input Format
```text
# Example input_text.txt
A happy Irish jig in D major with a lively rhythm
and traditional ornaments. The melody should feature
eighth note runs and occasional triplets.
```

## Configuration

### Generation Parameters
```python
{
    "max_length": 1024,      # Maximum sequence length
    "temperature": 1.0,      # Sampling temperature
    "top_p": 0.9,           # Nucleus sampling parameter
    "top_k": 50,            # Top-k sampling parameter
    "num_return_sequences": 3 # Number of variations
}
```

### Model Settings
```python
{
    "model_path": "path/to/checkpoint",
    "device": "cuda",        # or "cpu"
    "batch_size": 1,
    "use_cache": true
}
```

## Musical Controls

### Supported Attributes
- Key signatures
- Time signatures
- Tempo markings
- Musical styles
- Rhythmic patterns
- Melodic contours

### Style Keywords
```python
STYLES = {
    "classical": ["sonata", "minuet", "baroque"],
    "folk": ["jig", "reel", "ballad"],
    "jazz": ["swing", "bebop", "blues"],
    # ... more styles
}
```

## Output Formats

### ABC Notation
```abc
X:1
T:Generated Melody
M:6/8
L:1/8
K:D
|: "D"d2e f2g | "A"a2f "D"d2f :|
```

### Additional Formats
- MIDI export
- MusicXML conversion
- Audio rendering

## Integration

### Python API
```python
from text2music import TextToMusicGenerator

generator = TextToMusicGenerator()
abc_notation = generator.generate(
    prompt="A peaceful melody in C major",
    num_variations=3
)
```

### Web API
```python
@app.post("/generate")
async def generate_endpoint(
    prompt: str,
    num_variations: int = 1
) -> List[str]:
    # Implementation
    pass
```

## Error Handling

### Common Issues
1. Invalid musical descriptions
2. Generation failures
3. Format conversion errors

### Solutions
- Robust input validation
- Fallback generation strategies
- Error recovery mechanisms

## Performance Tips
- Batch processing for multiple generations
- GPU acceleration when available
- Caching frequent patterns
- Memory management for long sequences

## Examples

### Sample Prompts
1. "A gentle waltz in 3/4 time"
2. "An energetic Scottish reel"
3. "A romantic piano piece in minor key"

### Advanced Usage
```python
# Style transfer
generator.generate_with_style(
    prompt="A melody",
    style="irish_folk",
    strength=0.8
)

# Structure control
generator.generate_with_form(
    prompt="A melody",
    form="AABA",
    length_bars=32
)
``` 