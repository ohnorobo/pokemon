#!/usr/local/bin/python3

from PIL import Image
import colorsys
import glob
import os
from collections import Counter

#rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
#hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

'''
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
'''


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
  difference = min((maxh-minh) ((minh+1)-maxh))

  return difference



def get_color_histogram(image):
  color_counts = Counter()
  color_list = []

  for pix in image.getdata():
    color_counts[pix] += 1

  for color, num in sorted(colors.items(), key=lambda x: x[1], reverse=True):
    color_list.append(color)

  return color_list



#The basic idea behind the colors is that each sprite will have at most 3 different colors, with at most 5 shades of each color. The 3rd shade of each color is set to be the primary color, with the 2 shades on either side defining highlights and shadows.
# http://www.alexonsager.net/2013/06/behind-the-scenes-pokemon-fusion/
# breaks the colors into three lists 
# (and a secret 4th list for grayscale)
def get_primary_secondary_tertiary(color_list):
  # pick the smallest # of clusters such that 
  # the distance between 2 hues in a cluster is never more than 30 (?) degrees
  # primary colors have to be matched between pokemon merges
  # secondary and tertiary colors don't (and they may be empty lists)

  primary = []
  secondary = []
  tertiary = []
  grayscale = []

  primary.append(color_list[0])
  color_list = color_list[1:]

  for color in color_list:
    if is_grayscale(color):
      grayscale.append(color)
    elif is_close_in_list(primary, color):
      primary.append(color)
    elif is_close_in_list(secondary, color):
      secondary.append(color)
    elif is_close_in_list(tertiary, color):
      tertiary.append(color)
    else:
      pprint(("NON CLOSE COLOR", color))

  return (primary, secondary, tertiary, grayscale)


def is_greyscale(color):
  r, g, b, a = color
  return r == g == b


def is_close_in_list(color_list, color):
  # checks if a color is within 30 degrees of all others in a list

  for c in color_list:
    closeness = closeness(color, c):
      if (closeness * 360) > 30:
        return False
  return True








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



def rgb_to_hsv(color):
  r, g, b, a = color
  maxcolor = max(r, g, b)
  mincolor = min(r, g, b)
  v = maxcolor

  if maxcolor == 0:
    s = 0
  else:
    s = (maxcolor - mincolor)/maxcolor

  if s == 0:
    h = 0
  else:
    if r == maxcolor:
      h = (g-b)/(maxcolor-mincolor)
    elif g == maxcolor:
      h = 2 + (b-r)/(maxcolor-mincolor)
    elif b == maxcolor:
      h = 4 + (r-g)/(maxcolor-mincolor)
    else:
      print("AAAAAHHHHH")

    if (h<0):
      h = 0

  return (h*255, s*255, v*255)

# http://lodev.org/cgtutor/color.html
def hsv_to_rgb(color):
  h, s, v = color

  h /= 255
  s /= 255
  v /= 255

  if s == 0:
    r = v
    g = v
    b = v

  else:
    h *= 6
    i = floor(h)
    f = h-i
    p = v * (1 - s)
    q = v * (1 - (s*f))
    t = v * (1 - (s*(l-f)))

    if i == 0:
      r=v
      g=t
      b=p
    if i == 1:
      r=q
      g=v
      b=p
    if i == 2:
      r=p
      g=v
      b=t
    if i == 3:
      r=p
      g=q
      b=v
    if i == 4:
      r=t
      g=p
      b=v
    if i == 5:
      r=v
      g=p
      b=q

  return (floor(r*255), floor(g*255), floor(b*255))






