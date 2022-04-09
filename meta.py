import json
from config import *


class Meta:
    def __init__(self, data):
        self.data = data

    def gen_json(self):
        print(type(self.data))
        for key, value in self.data.items():
            token = {
                'image': IMAGES_BASE_URL + str(key) + '.png',
                'tokenID': key,
                'name': PROJECT_NAME + ' ' + str(key),
                'attributes': [value]
            }
            #
            token_fname = './metadata/' + str(key) + '.json'
            with open(token_fname, 'w') as f:
                json.dump(token, f, indent=4)
