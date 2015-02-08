from PIL import Image

def same_size(img):
    w, h = img.size

    master = Image.new(
                mode='RGBA',
                size=(300, 280),
                color=(0,0,0,0))

    master.paste(img, (150-w/2, 280-h-2))
    return master


img = Image.open("site/static/imgs/generated/missingno.png")
master = same_size(img)
master.save("site/static/imgs/generated/missingno.png")
