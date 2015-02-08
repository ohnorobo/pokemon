#!/usr/local/bin/python3

import json
import random
from PIL import Image
from pprint import pprint

file_loc = "../images/croppedPokeParts/"

def get_metadata():
  f = open("../metadata/body.json", 'r')
  bodies = json.loads(f.read())

  f = open("../metadata/head.json", 'r')
  heads = json.loads(f.read())

  return bodies, heads


# paste of the paste coords of the first image
# pinhole_a is the pinhold for the first image
# pinhole_b is the pinhold for the second image
# returns the coords to paste b to match pinholes
def get_pinhole_match(paste, pinhole_a, pinhole_b, imagea, imageb):
  x = paste[0] + pinhole_a[0] - pinhole_b[0]
  y = paste[1] + (imagea.size[1] - pinhole_a[1]) - pinhole_b[1]
  return (x, y)


def crop(img):
    data = img.load()
    l,w = img.size
    print l,w
    a = (l,w)
    b = (l,0)
    c = (0,w)
    d = (0,0)

    print((a, b, c, d))

    for x in range(0,l-1):
        for y in range(0,w-1):
            if data[x,y][3] != 0:
                a = (min(a[0],x),min(a[1],y))
                b = (min(b[0],x),max(b[1],y))
                c = (max(c[0],x),min(c[1],y))
                d = (max(d[0],x),max(d[1],y))

    print((a, b, c, d))

    a = (a[0] -1, a[1]-1)
    d = (d[0] +1,d[1]+1)

    return img.crop(a+d)

def generate_image():

  bodies, heads = get_metadata()
  body = random.choice(bodies)
  head = random.choice(heads)

  pprint(body)
  pprint(head)


  body_image = Image.open(file_loc+body["filename"])
  head_image = Image.open(file_loc+head["filename"])

  master = Image.new(
      mode='RGBA',
      size=(300, 300),
      color=(0,0,0,0))

  body_pinhole = body["needs"][0]["pinhole"]
  head_pinhole = head["pinhole"]


  master.paste(body_image,(50, 50))
  coords = get_pinhole_match((50, 50),
                              body_pinhole, head_pinhole,
                              body_image, head_image)
  master.paste(head_image, coords, head_image)
  master=crop(master)
  master.save("../site/static/imgs/horror.png")






