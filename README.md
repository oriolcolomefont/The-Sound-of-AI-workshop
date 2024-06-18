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
python clamp.py -clamp_model_name sander-wood/clamp-small-512 -query_modal text -key_modal music -top_n 100
```
