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

  f = open("./metadata/head.json", 'r')
  heads = json.loads(f.read())

  f = open("./metadata/tail.json", 'r')
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

def paste_in():
  pass


def generate_image():

  bodies, heads, tails = get_metadata()
  body = random.choice(bodies)
  head = random.choice(heads)
  tail = random.choice(tails)

  pprint(body)
  pprint(head)


  body_image = Image.open(file_loc+body["filename"])
  head_image = Image.open(file_loc+head["filename"])
  tail_image = Image.open(file_loc+tail["filename"])

  master = Image.new(
      mode='RGBA',
      size=(1000, 1000),
      color=(0,0,0,0))

  body_pinhole = body["needs"][0]["pinhole"]
  head_pinhole = head["pinhole"]
  tail_pinhole = tail["needs"][0]["pinhole"]

  master.paste(body_image,(500, 500))
  coords = get_pinhole_match((500, 500),
                              body_pinhole, head_pinhole,
                              body_image, head_image)
  master.paste(head_image, coords, head_image)
  if len(body["needs"])>1:
    body_pinhole = body["needs"][1]["pinhole"]
    coords = get_pinhole_match((500,500),
                               body_pinhole,tail_pinhole,
                               body_image, tail_image)
    master.paste(tail_image, coords, tail_image)
  master.save("../site/static/imgs/horror.png") 
  
 # for i in body_pinhole["needs"]:
 #   body_pinhole = i["pinhole"]
