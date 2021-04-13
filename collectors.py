import json
import pandas as pd
import os
import random

from network.genius_interface import GeniusInterface

class GeniusCollector():
    def __init__(self, id_file = './info/collection/genius_ids.csv', configuration_file = './info/services.json', interface = GeniusInterface()):
        with open(configuration_file) as json_file:
            genius_collection_data = json.load(json_file)['genius']['collection']

        self.id_file = id_file

        self.indices = {}
        self.interface = interface
        self.min_index = genius_collection_data['min-id']
        self.max_index = genius_collection_data['max-id']

        if os.path.exists(id_file):
            self.indices = list(pd.read_csv(id_file)['indices'].values)
        else:
            self.indices = [i for i in range(self.min_index, self.max_index)]
            random.shuffle(self.indices)
            pd.DataFrame({'indices' : self.indices}).to_csv(self.id_file, index = False)

    async def get_next_song(self):
        if len(self.indices) > 0:
            next_song = None
            while next_song is None:
                next_song = await self.get_song(self.indices.pop(0))
            return next_song
        else:
            raise StopIteration

    async def get_song(self, index):
        await self.interface.get_song(index)

    async def __next__(self):
        return await self.get_next_song()
    
    def has_next(self):
        return len(self.indices) > 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback):
        pd.DataFrame({'indices' : self.indices}).to_csv(self.id_file, index = False)
        await self.interface.close()