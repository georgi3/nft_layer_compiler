from PIL import Image
import os
from background import generate_background
import random

mamai = os.listdir('./cossack_mamai')
print(mamai)


def compose_png(*args):
    n = lambda: random.randint(0, 256)
    white = (256, 256, 256)
    rand = (n(), n(), n())
    background = generate_background(dimension=2048, color=white)
    for img in args:
        background = Image.alpha_composite(background, img)
    return background


n = lambda: random.randint(0, 256)
im0 = generate_background(dimension=2048, color=(n(), n(), n()))
im1 = Image.open('./cossack_mamai/body.png').convert('RGBA')
im2 = Image.open('./cossack_mamai/shirt.png').convert('RGBA')
im3 = Image.open('./cossack_mamai/pants.png').convert('RGBA')

im4 = Image.open('./cossack_mamai/boots.png').convert('RGBA')
im5 = Image.open('./cossack_mamai/head.png').convert('RGBA')
im6 = Image.open('./cossack_mamai/ears.png').convert('RGBA')

im7 = Image.open('./cossack_mamai/eyes.png').convert('RGBA')
im8 = Image.open('./cossack_mamai/brows.png').convert('RGBA')
im9 = Image.open('./cossack_mamai/nose.png').convert('RGBA')

im10 = Image.open('./cossack_mamai/lips.png').convert('RGBA')
im11 = Image.open('./cossack_mamai/cross.png').convert('RGBA')
im12 = Image.open('./cossack_mamai/belt.png').convert('RGBA')
im13 = Image.open('./cossack_mamai/stache.png').convert('RGBA')

l = [im1, im2, im3, im4, im5, im6, im7, im8, im9, im10, im12]

# l = [im1, im1]
cos = compose_png(*l)
cos.show('')
