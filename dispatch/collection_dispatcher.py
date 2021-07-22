import pandas as pd
import random
import json
import os

class CollectionDispatcher():
    def __init__(self, id_file = './info/collection/genius_ids.csv', configuration_file = './info/services.json'):
        with open(configuration_file) as json_file:
            genius_collection_data = json.load(json_file)['genius']['collection']

        self.id_file = id_file

        self.indices = []
        self.min_index = genius_collection_data['min-id']
        self.max_index = genius_collection_data['max-id']

        if os.path.exists(id_file):
            self.indices = list(pd.read_csv(id_file)['indices'].values)
        else:
            self.indices = [i for i in range(self.min_index, self.max_index)]
            random.shuffle(self.indices)
            self.save()

    async def get_next_song(self):
        if len(self.indices) > 0:
            selected_index = self.indices.pop()
            try:
                return await self.interface.get_song(selected_index)
            except GeniusRetrievalFailure as e:
                if str(e.status)[0] == '5':
                    self.indices.append(selected_index)
                    return
                elif e.status == 403 or e.status == 404:
                    return
                else:
                    raise e
            except:
                self.indices.append(selected_index)
                raise e
        else:
            raise StopIteration

    def save(self):
        pd.DataFrame({'indices' : self.indices}).to_csv(self.id_file, index = False)

    async def __next__(self):
        return await self.get_next_song()
    
    def has_next(self):
        return len(self.indices) > 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback):
        self.save()
        await self.interface.close()