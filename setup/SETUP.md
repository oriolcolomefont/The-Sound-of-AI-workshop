# Setup python

This is Mac only.

1. Create conda from `setup/conda.yml`. I've called `soroll` ("noise" in Catalan)

```
conda env create -f setup/conda.yml
```

2. Check and install pip dependencies `setup/pip-requirements.txt`

3. You have to download this file: https://github.com/microsoft/muzic/blob/main/clamp/inference/music_keys/music_keys.zip and unzip inside `clamp/inference/music_keys`

## Recreate env

From root folder:

```
conda deactivate
conda env update --file setup/conda.yml --prune
```

4. Cross fingers 🤞

If I remember correctly, I've installed `transformers` and `unidecode` with conda instead of pip

## Useful? links

- Install pytorch with Apple GPU: https://developer.apple.com/metal/pytorch/
- Install pytorch with Apple GPU: https://chrisdare.medium.com/running-pytorch-on-apple-silicon-m1-gpus-a8bb6f680b02
- Check MPS (Apple GPU) is installed: https://pytorch.org/docs/stable/notes/mps.html

```

```
