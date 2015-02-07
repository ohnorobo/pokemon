import Image
import colorsys
import glob
import os

start_dir = "../images/pokemonParts/"
end_dir = "../images/croppedPokeParts/"
file = open("data.txt",'w')

def findCrop(xdir):
    if not os.path.exists(xdir):
        xdir = start_dir+xdir
    ydir = end_dir+xdir
    try: 
        os.makedirs(os.path.split(ydir)[0])
    except OSError:
        if not os.path.isdir(os.path.split(ydir)[0]):
            raise
    filename = os.path.split(xdir)[1]
    img = Image.open(xdir)
    data = img.load()
    l,w = img.size
    print l,w
    a = (l,w)
    b = (l,0)
    c = (0,w)
    d = (0,0)
    for x in range(0,l-1):
        for y in range(0,w-1):
            if data[x,y] != (255,255,255,0):
                a = (min(a[0],x),min(a[1],y))
                b = (min(b[0],x),max(b[1],y))
                c = (max(c[0],x),min(c[1],y))
                d = (max(d[0],x),max(d[1],y))
    
    new_img = img.crop(a+d)

    new_img.save(ydir)

def fitIn(xdir,ydir):
    ximg = Image.open(end_dir+xdir)
    yimg = Image.open(end_dir+ydir)
    new_img = yimg.copy()
    new_img.paste(ximg,(0,0))
    new_img.save(end_dir+"testproduct.png")
