#!/usr/local/bin/python3

import json
import random
from PIL import Image
from pprint import pprint

file_loc = "../images/croppedPokeParts/"

def get_metadatalist():
  pass

def get_metadata():
  f = open("../metadata/body.json", 'r')
  bodies = json.loads(f.read())

  f = open("../metadata/head.json", 'r')
  heads = json.loads(f.read())

  f = open("../metadata/tail.json", 'r')
  tails = json.loads(f.read())

  return bodies, heads, tails


# paste of the paste coords of the first image
# pinhole_a is the pinhold for the first image
# pinhole_b is the pinhold for the second image
# returns the coords to paste b to match pinholes
def get_pinhole_match(paste, pinhole_a, pinhole_b, imagea, imageb):
  x = paste[0] + pinhole_a[0] - pinhole_b[0]
  y = paste[1] + (imagea.size[1] - pinhole_a[1]) - pinhole_b[1]
  return (x, y)

def get_pinhole_match_beta(paste, pinhole_a, pinhole_b, imagea, imageb):
  x = paste[0] + pinhole_a[0] - pinhole_b[0]
  y = paste[1] + (imagea.size[1] - pinhole_a[1]) - (imageb.size[1] - pinhole_b[1])
  return (x, y)

def paste_in():
  pass


def crop(img):
    data = img.load()
    l,w = img.size
    a = (l,w)
    b = (l,0)
    c = (0,w)
    d = (0,0)


    for x in range(0,l-1):
        for y in range(0,w-1):
            if data[x,y][3] != 0:
                a = (min(a[0],x),min(a[1],y))
                b = (min(b[0],x),max(b[1],y))
                c = (max(c[0],x),min(c[1],y))
                d = (max(d[0],x),max(d[1],y))


    a = (a[0] -1, a[1]-1)
    d = (d[0] +1,d[1]+1)

    return img.crop(a+d)

def same_size(img):
  w, h = img.size

  master = Image.new(
      mode='RGBA',
      size=(300, 280),
      color=(0,0,0,0))

  master.paste(img, (150-w/2, 280-h-2), img)
  return master


FACTOR = 3
def embiggen(img):
  return img.resize((FACTOR*img.size[0], FACTOR*img.size[1]), 0)

def get_image_filename(ids):
    # print(("IDS",ids))
    return "-".join(str(v) for v in ids) + ".png"


def generate_image(seed=None):

  bodies, heads, tails = get_metadata()

  random.seed(seed)
  body_id = random.choice(range(len(bodies)))
  head_id = random.choice(range(len(heads)))
  tail_id = random.choice(range(len(tails)))

  body = bodies[body_id]
  head = heads[head_id]
  tail = tails[tail_id]

  body_image = Image.open(file_loc+body["filename"])
  head_image = Image.open(file_loc+head["filename"])
  tail_image = Image.open(file_loc+tail["filename"])

  master = Image.new(
      mode='RGBA',
      size=(300, 300),
      color=(0,0,0,0))

  head_pinhole = head["pinhole"]
  tail_pinhole = tail["needs"][0]["pinhole"]
  if len(body["needs"])>1:
    body_pinhole = body["needs"][1]["pinhole"]
    coords = get_pinhole_match_beta((150,150),
                               body_pinhole,tail_pinhole,
                               body_image, tail_image)
    master.paste(tail_image, coords, tail_image)
    ids = [body_id, head_id, tail_id]

  else: #no tail
    ids = [body_id, head_id, 'X']

  body_pinhole = body["needs"][0]["pinhole"]
  master.paste(body_image,(150, 150),body_image)
  coords = get_pinhole_match((150, 150),
                              body_pinhole, head_pinhole,
                              body_image, head_image)
  master.paste(head_image, coords, head_image)

  master = crop(master)
  master = embiggen(master)
  master = same_size(master)
  master.save("../site/static/imgs/generated/"+get_image_filename(ids))

  return ids + [seed]

 # for i in body_pinhole["needs"]:
 #   body_pinhole = i["pinhole"]
