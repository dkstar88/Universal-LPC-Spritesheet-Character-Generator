import glob
import json
import os
from PIL import Image, ImageOps, ImageColor


BODY_TYPES = ['male', 'female', 'muscular', 'pregnant', 'child']
IMAGE_FOLDER = '../spritesheets'

PROCESSED_PATH = []

def center_image(img, width, height):
    (iw, ih) = img.size
    left = (width-iw)//2
    top = (height-ih)//2
    result = Image.new("RGBA", size=(width, height), color="#00000000")
    result.paste(img, (left, top))
    return result

def generate_thumb(source):
    global PROCESSED_PATH
    with open(source) as f:
        d = json.load(f)
        for body in BODY_TYPES:
            if not body in d['layer_1']:
                continue
            imagepath = d['layer_1'][body]
            variants = d['variants']

            for variant in variants:
                variant = variant.replace(' ', '_')
                imagefile = os.path.join(IMAGE_FOLDER, imagepath, variant + '.png')
                if imagefile in PROCESSED_PATH:
                    continue
                PROCESSED_PATH.append(imagefile)

                if os.path.exists(imagefile):

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
                    region = region.crop(region.getbbox())
                    (width, height) = region.size
                    if width * 3 < 48 and height * 3 < 48:
                        region = ImageOps.contain(region, (width*3, height*3))
                    
                    
                    if width > 64 or height > 64:
                        #print("%s - fit - %d, %d" % (thumbfile, width, height))
                        region = ImageOps.contain(region, (64, 64))

                    (width, height) = region.size
                    if width != 64 or height != 64:
                        region = center_image(region, 64, 64)

                    region.save(thumbfile)

                
    
for filepath in glob.iglob('../sheet_definitions/*.json'):
    #print(filepath)
    generate_thumb(filepath)

# generate_thumb("../sheet_definitions/shield.json")