# Code to run an AI-driven picture frame

There are three components here (or will be, when I've finished!)

 - gen: does all the funky AI stuff to generate images.
 - serve: serves them to the inky
 - render: displays them on the inky

## gen

This is the script that generates (and links) content and stashes it in a directory.

We're going to exploit the observation that SD-Turbo will not only run on my graphics card (:-)), but responds pretty well to GROAN-type input.

So, we write a simple text generator and feed that output through SD-Turbo to generate images which can be fetched by the frame.

To use this we'll need a venv

```sh
mkdir ~/env
python -m venv env
source env/bin/activate
pip install diffusers transformers accelerate --upgrade
```

And make sure you have plenty of space in `~/.cache` - it's about to get hit with a few GiB of weights. Now:

```sh
./gen.py --image-dir=/somewhere/to/cache/things --batch-size=20
```

Feel free to set `--guidance-scale` and `--inference-steps`. `gen.py`
does a centre-cut to the right resolution for an Inky 7.3, because one
day we'd like to make stable diffusion do this for us.

## Serve

This serves the data from port 14582:

```sh
export IMG_DIR=/somewhere/to/cache/things
cd serve
./serve
```

## Set your wifi parameters

Write a `secrets.py` on your Pico (via `thonny`)

```python
WIFI_SSID="MYSSID"
WIFI_PASSWORD="MYPASSWORD"
# Or whatever it is.
SERVER_NAME="192.168.1.1"
```

Now copy `render/thirdparty/*` and `render/main.py` to your inky and run `main.py`.

It takes some time to decode the JPEG (need to work out why - it probably shouldn't).
