from PIL import Image, ImageDraw

# n = lambda: random.randint(0, 256)
# rand_color = (n(), n(), n())
nice_pinkish = (233, 125, 161)
nice_redish = (226, 87, 82)


def generate_background(dimension=560, color=(233, 125, 161), second_color=(255, 239, 0)):
    original_img = Image.new('RGBA', (dimension, dimension))
    draw = ImageDraw.Draw(original_img)
    border = (0, 0, dimension, dimension/2)
    draw.rectangle(border, color)
    bottom_border = (0, dimension/2, dimension, dimension)
    draw.rectangle(bottom_border, second_color)
    return original_img


# main(560, rand_color)

