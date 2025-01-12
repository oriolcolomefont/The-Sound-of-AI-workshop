# Symbolic Music Information Retrieval and Generation

## Overview
A comprehensive Music Information Retrieval (MIR) system that combines state-of-the-art AI models for symbolic music generation, analysis, and similarity search. This project showcases various aspects of MIR including:
- Symbolic music generation using transformer-based models
- Music similarity search using CLAMP embeddings
- Text-to-music generation
- Format conversion (MusicXML to ABC)
- Audio synthesis from symbolic representations

## Features
- **AI-Powered Music Generation**: Multiple approaches including Tunesformer and text-to-music models
- **Music Similarity Search**: Using Microsoft's CLAMP model for finding similar melodies
- **Format Conversion**: Tools for converting between different music notation formats
- **Audio Synthesis**: ABC to MIDI to audio conversion pipeline
- **Web Interface**: Modern Next.js frontend for interactive music generation and analysis

## Architecture
```
├── api/              # FastAPI backend server
├── client/           # Next.js frontend application
├── clamp/            # Music similarity search implementation
├── text-to-music/    # Text-to-music generation module
├── tunesformer/      # Transformer-based music generation
├── abc-utils/        # ABC notation utilities
├── generate/         # Music generation scripts
└── setup/           # Environment setup instructions
```

## Workshop Plan

**Monday**:
- Setup Python environment

**Tuesday**:
- Complete Python setup
- Generate random ABC melodies
- Identify similar melodies within the generated set

## Setup

Follow the instructions in `setup/SETUP.md` to get the environment ready.

## Application Structure

### Client (web, using [Next.js](https://nextjs.org/docs/getting-started/installation)):

```bash
cd client
# Install dependencies (run only once)
npm install
# Start the client
npm run dev
```

API (server using [FastAPI](https://fastapi.tiangolo.com/))

```bash
cd api
# Install dependencies only once
pip install fastapi
# Start the server
fastapi dev main.py
```

## Usage
To activate the environment:

```bash
conda activate soroll
```

##Melodies Generation & Similarity Search
We utilize several AI tools for melody generation, similarity matching, and sonification.

###Clamp
Find similar melodies using Microsoft's Clamp model:

https://github.com/microsoft/muzic/tree/main/clamp

```bash
cd clamp
# First
python clamp.py -clamp_model_name sander-wood/clamp-small-512 -query_modal music -key_modal text -top_n 100

# Find similar melodies (specified inside music_keys) of a given melody (specified in music_query.abc)
python clamp.py -clamp_model_name sander-wood/clamp-small-512 -query_modal music -key_modal music -top_n 3
```

### Text-to-music
Generate melodies from textual descriptions:

https://github.com/sander-wood/text-to-music

```bash

# optional: edit input_text.txt
cd text-to-music

python run_inference.py -num_tunes 3 -max_length 1024 -top_p 0.9 -temperature 1.0 -seed 0
```

### mxl to ABC
Convert MusicXML files to ABC format:

```bash
python inference/xml2abc.py -m 2 -c 8 -x input.mxl > inference/music_query.abc
```

### Sonify-abc
Sonify ABC files into audio:

```bash

# optional: edit input_text.txt
cd generate

python sonifyabc.py {input_folder} {output_folder} {midi_folder} {soundfont_file}
```

### Tunesformer
Generate music using the Tunesformer model:

https://github.com/sander-wood/tunesformer

```bash
python generate.py -num_tunes 3 -max_patch 128 -top_p 0.8 -top_k 8 -temperature 1.2 -seed 0 -show_control_code True
```

## Technical Details

### Models Used
- **CLAMP**: Microsoft's cross-modal language-music pre-training model
- **Tunesformer**: Transformer-based symbolic music generation
- **Text-to-Music**: Natural language to symbolic music conversion

### Data Processing Pipeline
1. Text/Music Input Processing
2. Model-specific encoding
3. Generation/Analysis
4. Format conversion
5. Audio synthesis

## Research and Implementation Details

### Music Similarity Search
The system uses CLAMP embeddings to create a high-dimensional representation of musical pieces, enabling:
- Cross-modal similarity search (text-to-music, music-to-music)
- Style-based retrieval
- Melodic pattern recognition

### Music Generation
Multiple approaches are implemented:
- Unconditional generation using Tunesformer
- Text-conditioned generation
- Style transfer capabilities

## Future Enhancements
- Integration of additional MIR models
- Enhanced audio analysis capabilities
- Real-time generation features
- Expanded dataset support

## Citation
If you use this project in your research, please cite:
```
@misc{symbolic-soroll,
  author = {Your Name},
  title = {Symbolic Soroll: Advanced Music Information Retrieval System},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/yourusername/symbolic-soroll}
}
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
