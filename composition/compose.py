#!/usr/local/bin/python3

import yaml
import random
from PIL import Image
from pprint import pprint

file_loc = "./images/croppedPokeParts/"

def get_metadata():
  f = open("./metadata/body.yaml", 'r')
  bodies = yaml.load_all(f)

  f = open("./metadata/head.yaml", 'r')
  heads = yaml.load_all(f)

  return list(bodies), list(heads)


# paste of the paste coords of the first image
# pinhole_a is the pinhold for the first image
# pinhole_b is the pinhold for the second image
# returns the coords to paste b to match pinholes
def get_pinhole_match(paste, pinhole_a, pinhole_b):
  x = paste[0] + pinhole_a[0] - pinhole_b[0]
  y = paste[1] + pinhole_a[1] - pinhole_b[1]
  return (x, y)



bodies, heads = get_metadata()
body = random.choice(bodies[0])
head = random.choice(heads[0])

pprint(body)
pprint(head)


body_image = Image.open(file_loc+body["filename"])
head_image = Image.open(file_loc+head["filename"])

master = Image.new(
    mode='RGBA',
    size=(1000, 1000),
    color=(0,0,0,0))

body_pinhole = (body["pinhole-x"], body["pinhole-y"])
head_pinhole = (head["pinhole-x"], head["pinhole-y"])


master.paste(body_image,(500, 500))
coords = get_pinhole_match((500, 500), body_pinhole, head_pinhole)
master.paste(head_image, coords)
master.save("horror.png")






