#! /usr/bin/env python

"""
Generates a cache of images for picframe; we do things this way so that we don't occupy the graphics card whilst the
slideshow is actually happening (because I want to use it in jupyter :-) ), and also because loads are really slow..
"""

import torch
import yaml
import os.path
import typing
import random
import click
import time

SELF_DIR = os.path.split(__file__)[0]

class Description:
    def __init__(self):
        with open(os.path.join(SELF_DIR, "control.yaml"), 'r') as f:
            self.desc = yaml.safe_load(f.read())

    def make_description(self, gen) -> str:
        elems = self.desc["compose"]
        result = []
        for elem in elems:
            if not elem:
                break
            one_of = elem.get('one_of')
            if one_of is not None:
                which = one_of[gen.randrange(len(one_of))]
                result.append(which)
            some_of = elem.get('some_of')
            if some_of is not None:
                for s in some_of:
                    if gen.randrange(2) != 0:
                        result.append(s)
            fixed = elem.get('fixed')
            if fixed is not None:
                result.extend([f for f in fixed])
        return " ".join(result)

class ImagePipeline:
    def __init__(self):
        # Dynamic import so we don't do the GPU initialisation until we have to.
        diffusers = __import__("diffusers")
        #from diffusers import AutoPipelineForText2Image
        self.pipe = diffusers.AutoPipelineForText2Image.from_pretrained("stabilityai/sd-turbo", torch_dtype=torch.float16, variant="fp16")
        # Beware - if you want this on your CPU, you'll need to not use fp16
        self.pipe.to("cuda")

    def generate_image(self, prompt):
        image = self.pipe(prompt = prompt, num_inference_steps = 3, guidance_scale = 0.0)
        return image.images[0]


class GiveUp(Exception):
    pass

@click.command()
@click.option("--seed", default=None)
@click.option("--batch-size", default=4)
@click.option("--image-dir", default = None)
def go(seed, batch_size, image_dir):
    desc = Description()
    if seed is None:
        seed = time.time()
    if image_dir is None:
        raise GiveUp("You must specify an image directory with --image-dir")
    rand = random.Random(seed)
    pipe = ImagePipeline()
    for i in range(batch_size):
        d = desc.make_description(rand)
        print(f" - {d}")
        img = pipe.generate_image(d)
        stem = os.path.join(image_dir, f"{seed}_{i}")
        with open(f"{stem}.txt", 'w') as f:
            meta = { "prompt" : d, "seed" : seed, "index": i }
            yaml.dump(meta, f)
        img.save(f"{stem}.jpg", format='JPEG')

if __name__ == "__main__":
    go()
    
