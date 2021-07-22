import pandas as pd
import random
import json
import os

from collectors import *

class CollectionDispatcher():
    def __init__(self, id_file = './info/collection/genius_ids.csv', configuration_file = './info/services.json'):
        with open(configuration_file) as json_file:
            genius_collection_data = json.load(json_file)['genius']['collection']

        self.id_file = id_file

        self.min_index = genius_collection_data['min-id']
        self.max_index = genius_collection_data['max-id']

        if os.path.exists(id_file):
            genius_stack = list(pd.read_csv(id_file)['indices'].values)
        else:
            genius_stack = [i for i in range(self.min_index, self.max_index)]
            random.shuffle(genius_stack)
            self.save()
        
        self.stack = {
        }

        self.collectors = {
            'genius' : GeniusCollector(),
            'spotify' : SpotifyCollector(),
            'youtube' : YoutubeCollector(),
            'soundcoud' : SoundcloudCollector()
        }

    async def update_from_service(self, service):
        if len(self.stacks[service]) > 0:
            item_to_update = self.stacks[service].pop()
            item_to_update = self.collectors.update_item(item_to_update)

    async def _index_of_next_for_service(self, service):


    def save(self):
        pd.DataFrame({'indices' : self.indices}).to_csv(self.id_file, index = False)