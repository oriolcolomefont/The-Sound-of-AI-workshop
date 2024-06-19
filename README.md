# Symbolic Soroll

Repo: https://github.com/danigb/symbolic-soroll
Google doc: https://docs.google.com/document/d/12YW3WwS4il5bFIiHNfAnDf-tTJOX63ysJp1wR8yezyU/edit

https://michaeleskin.com/abctools/abctools.html

## Plan

Monday:

- Setup python

Tuesday:

- Finish python setup
- Generate abc random melodies
- Find similar melody inside the random melodies

## Setup

See `setup/SETUP.md`

## Application

Client (web using [next](https://nextjs.org/docs/getting-started/installation)):

```bash
cd client
# Install dependencies only once
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

```bash
conda activate soroll
```

### Clamp

https://github.com/microsoft/muzic/tree/main/clamp

```bash
cd clamp
# First
python clamp.py -clamp_model_name sander-wood/clamp-small-512 -query_modal music -key_modal text -top_n 100

# Find similar melodies (specified inside music_keys) of a given melody (specified in music_query.abc)
python clamp.py -clamp_model_name sander-wood/clamp-small-512 -query_modal music -key_modal music -top_n 3
```

### Text-to-music

```bash

# optional: edit input_text.txt
cd text-to-music

python run_inference.py -num_tunes 3 -max_length 1024 -top_p 0.9 -temperature 1.0 -seed 0
```

### mxl to abc

```bash
python inference/xml2abc.py -m 2 -c 8 -x input.mxl > inference/music_query.abc
```

### Sonify-abc

```bash

# optional: edit input_text.txt
cd generate

python sonifyabc.py {input_folder} {output_folder} {midi_folder} {soundfont_file}
```
