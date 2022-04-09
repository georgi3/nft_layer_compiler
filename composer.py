import json
from pprint import pprint
from config import IMAGES_BASE_URL, PROJECT_NAME, folder_n
import random
from background import generate_background
from PIL import Image
import os
from collections import Counter, defaultdict
from meta import Meta
import time

from dudes import data
from traits import config


class ImageComposer:
    def __init__(self, config):
        self.config = config
        self.all_images = {}
        if not os.path.isdir('./metadata'):
            os.mkdir('./metadata')
        if not os.path.isdir('./images'):
            os.mkdir('./images/')

    def get_all_images(self):
        return self.all_images

    def store_metadata(self):
        metadata_fname = './metadata/all_traits.json'
        with open(metadata_fname, 'w') as f:
            json.dump(self.all_images, f, indent=4)

    @staticmethod
    def arbitrary_choices(seq, weights):
        """
        :param seq: passing a sequence that wo
        :param weights: weights for each element
        :return: returns an arbitrary number of elements from a sequence based on the passed weights
        """
        if len(seq) != len(weights):
            raise TypeError('arbitrary_choices() takes arguments of the same length')
        else:
            rand_num = lambda: random.random()
            return [item[0] for item in zip(seq, weights) if rand_num() < item[1]]

    def selecting_layer_img(self):
        """
        :return: returns a list with number ids of chosen layers for current image based on rarity of the layers
        """
        weights = [dic['rarity'] for dic in self.config if dic['rarity'] != 1]
        req_layers = [dic['id'] for dic in self.config if dic['rarity'] == 1]
        optional_layers = [dic['id'] for dic in self.config if dic['rarity'] != 1]
        chosen_opt_layers = self.arbitrary_choices(optional_layers, weights)
        return sorted(chosen_opt_layers + req_layers)

    def selecting_images(self):
        """
        :return: returns a unique dictionary with assigned img for each layer
        """
        new_img = {}
        for layer in self.config:
            if layer['id'] in self.selecting_layer_img():
                attrs_name = [attribute['file'] for attribute in layer['attributes']]
                attrs_weight = [attribute['rarity'] for attribute in layer['attributes']]
                new_img[layer['folder']] = random.choices(attrs_name, attrs_weight)[0]

        if new_img in self.all_images.values():
            return self.selecting_images()
        else:
            token_id = len(self.all_images)
            self.all_images[token_id] = new_img
            # token = {
            #     'image': IMAGES_BASE_URL + str(token_id) + '.png',
            #     'tokenID': token_id,
            #     'name': PROJECT_NAME + ' ' + str(token_id),
            #     'attributes': [new_img]
            # }
            #
            # token_fname = './metadata/' + str(token_id) + '.json'
            # with open(token_fname, 'w') as f:
            #     json.dump(token, f, indent=4)
            return new_img

    def count_rarity(self):
        """
        :return: dictionary with real rarity of each property in the current collection
        """
        count = defaultdict(int)
        for img in self.all_images.values():
            for value in img.values():
                count[value] += 1
        return {k: v / len(self.all_images) for k, v in sorted(count.items(), key=lambda item: item[1], reverse=True)}

    @staticmethod
    def compose_png(*args):
        """
        :param args: takes an ordered list of images to be composed together
        :return: returns a composed png with an added random background
        """
        n = lambda: random.randint(0, 256)
        background = generate_background(dimension=2048, color=(n(), n(), n()))
        for png in args:
            background = Image.alpha_composite(background, png)
        return background.convert('RGB')

    def generate_png(self):
        """
        :return: created and saves composed random png
        """
        img_dic = self.selecting_images()
        images_list = [Image.open(f'./{folder_n}/{key}/{value}').convert('RGBA') for key, value in img_dic.items()]
        composition = self.compose_png(*images_list)
        # rgb_im.show()
        file_name = str(list(self.all_images.values()).index(img_dic)) + ".png"
        composition.save("./images/" + file_name)
        self.store_metadata()
        time.sleep(2)


img = ImageComposer(config)
for _ in range(40):
    img.generate_png()

time.sleep(1)
all_meta = img.get_all_images()
met = Meta(all_meta)
met.gen_json()
