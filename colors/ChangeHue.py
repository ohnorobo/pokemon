#!/usr/local/bin/python3

from PIL import Image
import colorsys
import glob
import os
from collections import Counter
from pprint import pprint



# color, a rgb tuple
# amount a number from 0 to 255
def shift(color, amount):
  r, g, b, a = color

  print(("rgb", r, g, b, a))

  h, l, s = colorsys.rgb_to_hls(r, g, b)
  print(("hls", h, l, s))
  h *= 360
  h += int(amount)
  h %= 360
  h /= 360.0
  print(("hls", h, l, s))

  r, g, b = colorsys.hls_to_rgb(h, l, s)

  print(("rgb", int(r), int(g), int(b), a))

  return (int(r), int(g), int(b), a)



def closeness(color_a, color_b):
  ra, ga, ba, aa = color_a
  rb, gb, bb, ab = color_b

  ha, la, sa = colorsys.rgb_to_hls(ra, ga, ba)
  hb, lb, sb = colorsys.rgb_to_hls(rb, gb, bb)

  maxh = max(ha, hb)
  minh = min(ha, hb)
  difference = min(maxh-minh, (minh+1)-maxh)

  return difference



def get_color_histogram(image):
  color_counts = Counter()
  color_list = []

  for pix in image.getdata():
    if pix[3] != 0:
      color_counts[pix] += 1

  for color, num in sorted(color_counts.items(), key=lambda x: x[1], reverse=True):
    color_list.append(color)

  return color_list



def is_grayscale(color):
  r, g, b, a = color
  #print((r, g, b, a))
  diff = abs(r-g) + abs(g-b) + abs(b-r)
  #s = r+g+b
  return diff < 20 #or s > 700 or s < 150


def is_close_in_list(color_list, color, degree):
  # checks if a color is within 30 degrees of all others in a list

  for c in color_list:
    close = closeness(color, c)
    if (close * 360) > degree:
      return False
  return True






#The basic idea behind the colors is that each sprite will have at most 3 different colors, with at most 5 shades of each color. The 3rd shade of each color is set to be the primary color, with the 2 shades on either side defining highlights and shadows.
# http://www.alexonsager.net/2013/06/behind-the-scenes-pokemon-fusion/
# breaks the colors into three lists 
# (and a secret 4th list for grayscale)
def get_primary_secondary_tertiary(color_list, degree):
  # pick the smallest # of clusters such that 
  # the distance between 2 hues in a cluster is never more than 30 (?) degrees
  # primary colors have to be matched between pokemon merges
  # secondary and tertiary colors don't (and they may be empty lists)

  primary = []
  secondary = []
  tertiary = []
  grayscale = []
  aux = []

  while(len(primary) == 0 and len(color_list) != 0):
    if is_grayscale(color_list[0]):
      grayscale.append(color_list[0])
    else:
      primary.append(color_list[0])
    color_list = color_list[1:]

  for color in color_list:
    if is_grayscale(color):
      grayscale.append(color)
    elif is_close_in_list(primary, color, degree):
      primary.append(color)
    elif is_close_in_list(secondary, color, degree):
      secondary.append(color)
    elif is_close_in_list(tertiary, color, degree):
      tertiary.append(color)
    else:
      aux.append(color)

  return (primary, secondary, tertiary, grayscale, aux)




'''
def change_image(filename):
  image = Image.open(filename)

  newdata = []
  for pix in image.getdata():
    if pix[3] == 0:
      newdata.append(pix)
    else:
      newdata.append(shift(pix, 127))
  image.putdata(newdata)
  image.save(filename)

change_image("images/full_sprites/transparent/kanto/002.png")
'''


def print15pix(colors, data):
  for color in colors:
    data.append(color)

  for i in range(15 - len(colors)):
    data.append((255,255,255,0))



master = Image.new(
  mode='RGBA',  
  size=(75, 151), #40 px for color rows, 151 pokemon
  color=(0,0,0,0))  # fully transparent

start_dir = "images/full_sprites/transparent/kanto/"
#start_dir = "images/test/"
newdata = []
listdata = []
iconmap = os.listdir(start_dir)

pokenumber = 0
for filename in iconmap:
  pokenumber += 1
  listdata.append((pokenumber, [])) # add (2, []) to the list
  image = Image.open(start_dir+filename)

  histo = get_color_histogram(image)
  p, s, t, g, a= get_primary_secondary_tertiary(histo, 35)
  if len(t) == 0:
    p, s, t, g, a = get_primary_secondary_tertiary(histo, 20)

  print15pix(p, newdata)
  print15pix(s, newdata)
  print15pix(t, newdata)
  print15pix(g, newdata)
  print15pix(a, newdata)

  #pprint(("pokenumber",pokenumber))

#print(json.dumps(listdata, indent=2))
master.putdata(newdata)
master.save("./colors/colormap_split.png")

