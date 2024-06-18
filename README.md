# Symbolic Soroll

Repo: https://github.com/danigb/symbolic-soroll

## Setup

See `setup/SETUP.md`

## Usage

```bash
conda activate soroll
```

### Clamp

```bash
cd clamp
# First
python clamp.py -clamp_model_name sander-wood/clamp-small-512 -query_modal music -key_modal text -top_n 100
# Second
python clamp.py -clamp_model_name sander-wood/clamp-small-512 -query_modal text -key_modal music -top_n 100
```

#### Text-to-music

```bash

# optional: edit input_text.txt
cd text-to-music

python run_inference.py -num_tunes 3 -max_length 1024 -top_p 0.9 -temperature 1.0 -seed 0
```
