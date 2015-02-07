import Image
import numpy as np
import colorsys
import glob
import os

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

start_dir = "../images/full_sprites/opaque/kanto/"
end_dir = "imagedata"

#get your images using glob
iconmap = os.listdir(start_dir)
#iconMap = sorted(iconMap)

print(len(iconmap))

#for filename in iconmap:

def shift_hue(arr, hout):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = rgb_to_hsv(r, g, b)
    h = (h+hout)%360
    r, g, b = hsv_to_rgb(h, s, v)
    arr = np.dstack((r, g, b, a))
    return arr


def changeHue(filename, offset):
    image = Image.open(start_dir+filename)
    image = image.convert('RGBA')
    arr = np.array(np.asarray(image).astype('float'))
    new_img = Image.fromarray(shift_hue(arr, offset/360.).astype('uint8'), 'RGBA')
    new_img.save(end_dir+filename)

changeHue("0-0.png",70)
