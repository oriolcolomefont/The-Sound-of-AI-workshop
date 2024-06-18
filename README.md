# Symbolic Soroll

## Setup

1. Install conda
2. Create a conda environment (I called it `soroll`, "noise" in Catalan)
3. Install dependencies (more or less the same as clamp/requirements.txt)
4. Good luck!

## Usage

```bash
conda activate soroll
```

### Clamp

```bash
python clamp/clamp.py -clamp_model_name sander-wood/clamp-small-512 -query_modal text -key_modal music -top_n 100
```
