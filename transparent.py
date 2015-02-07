#!/usr/local/bin/python3

# This work is licensed under the Creative Commons Attribution 3.0 United 
# States License. To view a copy of this license, visit 
# http://creativecommons.org/licenses/by/3.0/us/ or send a letter to Creative
# Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.

# from http://oranlooney.com/make-css-sprites-python-image-library/ 
# Orignial Author Oran Looney <olooney@gmail.com>

#mods by Josh Gourneau <josh@gourneau.com> to make one big horizontal sprite JPG with no spaces between images
import os
from PIL import Image
import glob

start_dir = "images/full_sprites/opaque/kanto/"
end_dir = "images/full_sprites/transparent/kanto/"

#get your images using glob
iconmap = os.listdir(start_dir)
#iconMap = sorted(iconMap)

print(len(iconmap))

for filename in iconmap:
  image = Image.open(start_dir+filename) 
  image_width, image_height = image.size

  print( "the image will by %d by %d" % (image_width, image_height))
  print( "creating image...")
  master = Image.new(
      mode='RGBA',
      size=(image_width, image_height),
      color=(0,0,0,0))  # fully transparent
  master.paste(image,(0,0))

  data = master.getdata()

  newdata = []
  for item in data:
    if item[0] == 255 and item[1] == 255 and item[2] == 255:
      newdata.append((255,255,255,0))
    else:
      newdata.append(item)

  master.putdata(newdata)

  print( "saving master.jpg...")
  master.save(end_dir+filename)
  print( "saved!")

