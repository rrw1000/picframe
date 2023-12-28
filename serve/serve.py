#! /usr/bin/env python

from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
import os
import time
import re

app = FastAPI()

CONFIG_DIR = os.environ["IMG_DIR"]
SAFE_ID=re.compile("^[A-Za-z0-9_.]+$")

@app.get("/list")
async def read_list():
    files = [f for f in os.listdir(CONFIG_DIR) if f.endswith(".jpg") or f.endswith(".jpeg") ]
    return files

@app.get("/current_image.jpg")
async def image_now():
    # For now ..
    stamp = int(time.time())
    files = [f for f in os.listdir(CONFIG_DIR) if f.endswith(".jpg") or f.endswith(".jpeg") ]
    which_file = files[stamp % len(files)]
    file_name = os.path.join(CONFIG_DIR, which_file)
    return FileResponse(file_name)
    

@app.get("/img/{img_id}")
async def read_image(img_id: str):
    if SAFE_ID.fullmatch(img_id) is None:
        return JSONResponse(status_code = 401, content = { "bad_filename" : f"{img_id}" })
    id_name = os.path.join(CONFIG_DIR, f"{img_id}")
    print(id_name)
    if not os.path.exists(id_name):
        return JSONResponse(status_code = 404, content = { "error" : f"{id_name} does not exist" })
    return FileResponse(id_name)

@app.get("/")
async def root():
    return { "message": "Hello FastAPI!" }
