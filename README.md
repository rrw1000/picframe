# Code to run an AI-driven picture frame

We're going to exploit the observation that SD-Turbo will not only run on my graphics card (:-)), but responds pretty well to GROAN-type input.

So, we write a simple text generator and feed that output through SD-Turbo to generate images which can be fetched by the frame.

To use this we'll need a venv

```sh
mkdir ~/env
python -m venv env
source env/bin/activate
pip install diffusers transformers accelerate --upgrade
```

And make sure you have plenty of space in `~/.cache` - it's about to get hit with a few GiB of weights.


