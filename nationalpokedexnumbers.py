#!/usr/local/bin/python3


import os
startdir = "images/full_sprites/opaque/kanto/"

n = 1
fns = os.listdir(startdir)
fns.sort()

for fn in fns:
  os.rename(startdir+fn, startdir+str(n).zfill(3)+".png")
  n += 1
