import glob
import json
import os
from PIL import Image


BODY_TYPES = ['male', 'female', 'muscular', 'pregnant', 'child']
IMAGE_FOLDER = '../spritesheets'

PROCESSED_PATH = []

def generate_thumb(source):
    global PROCESSED_PATH
    with open(source) as f:
        d = json.load(f)
        for body in BODY_TYPES:
            try:
                imagepath = d['layer_1'][body]
                variants = d['variants']

                for variant in variants:
                    variant = variant.replace(' ', '_')
                    imagefile = os.path.join(IMAGE_FOLDER, imagepath, variant + '.png')
                    if imagefile in PROCESSED_PATH:
                        continue
                    PROCESSED_PATH.append(imagefile)
                    thumbfile = os.path.join(IMAGE_FOLDER, imagepath, variant + '-thumb.png')
                    im=Image.open(imagefile)
                    y = 0
                    size = 64
                    if 'oversize' in imagefile:
                        y = 2*192
                        size = 192
                    elif 'preview_row' in d:
                        y = d['preview_row'] * size
                    else:
                        y = 10 * size
                    region = im.crop((0, y, size, y+size))
                    if size > 64:
                        region = region.resize((64, 64))
                    region.save(thumbfile)

            except Exception as err:
                pass
    
for filepath in glob.iglob('../sheet_definitions/*.json'):
    print(filepath)
    generate_thumb(filepath)