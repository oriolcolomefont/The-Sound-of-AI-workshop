# Symbolic Soroll

This repository represents our work during the **"Sound Of AI Music Workshop"**, where we explored symbolic music generation using AI tools.

- **Repo**: https://github.com/danigb/symbolic-soroll
- **Google Doc** (project notes): [Symbolic Soroll Documentation](https://docs.google.com/document/d/12YW3WwS4il5bFIiHNfAnDf-tTJOX63ysJp1wR8yezyU/edit)
- **Render ABC**: [ABC Tools](https://michaeleskin.com/abctools/abctools.html)

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
