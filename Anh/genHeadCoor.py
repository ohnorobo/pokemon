import os
from PIL import Image

start_dir = "../images/croppedPokeParts/head"
f = open("headcoor.txt",'w')

listdir = os.listdir(start_dir)
data = []

for xdir in listdir:
    image = Image.open(start_dir+'/'+xdir)
    width, length = image.size
    num = ''.join(i for i in xdir if i in '1234567890')
    data.append((int(num),width/2,length/2))
    #print >> f, num, (width/2), length/2

data = sorted(data, key = lambda x: x[0])
for item in data:
    print >> f, item
