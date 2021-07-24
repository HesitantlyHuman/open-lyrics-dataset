import asyncio
from re import I
import pandas as pd
import random
import json
import os

from collectors import *
from data_management import DataPartitioner
from errors import TooFastError

class CollectionDispatcher():
    def __init__(
        self,
        data_partitioner,
        rate = 10,
        max_stack = 4096,
        id_file = './info/collection/genius_ids.csv',
        configuration_file = './info/services.json',
        error_threshold = 3
    ):
        with open(configuration_file) as json_file:
            genius_collection_data = json.load(json_file)['genius']['collection']

        self.data_partitioner = data_partitioner

        self.error_threshold = error_threshold

        self.id_file = id_file

        self.rate = rate

        self.max_stack = max_stack

        self.min_index = genius_collection_data['min-id']
        self.max_index = genius_collection_data['max-id']

        if os.path.exists(id_file):
            self._indices = list(pd.read_csv(id_file)['indices'].values)
        else:
            self._indices = [i for i in range(self.min_index, self.max_index)]
            random.shuffle(self._indices)
            self.save()

        #A dictionary which holds the data currently being processed
        self._data_digest = {
        }

        #Dictionary which holds error numbers for each service
        self._error_record = {
        }

        #A dictionary which holds list of indices for each service
        self._service_stacks = {
            'spotify' : [],
            'youtube' : [],
            'soundcloud' : []
        }

        self._collectors = {
            'genius' : GeniusCollector(),
            'spotify' : SpotifyCollector(),
            'youtube' : YoutubeCollector(),
            'soundcloud' : SoundcloudCollector()
        }

    async def start_generating_items(self):
        while True:
            if len(self._data_digest < self.max_stack):
                self._generate_item(self._indices.pop())
            asyncio.sleep(1 / self.rate + 1)

    async def start_service(self, service):
        while True:
            try:
                await self.update_next_for_service(service)
            except TooFastError as e:
                asyncio.sleep(e.wait)
            asyncio.sleep(1 / self.rate)

    async def update_next_for_service(self, service):
        item_id = self._service_stacks[service].pop()
        if not item_id is None:
            data_item = self._data_digest.pop(item_id)

            try:
                await self._collectors[service].update_item(data_item)
            except TooFastError as e:
                self._service_stacks[service].insert(0, item_id)
                raise e
            except:
                self._error_record[item_id][service] += 1

                if self._error_record[item_id][service] < self.error_threshold:
                    self._service_stacks[service].insert(0, item_id)

            if all([not item_id in stack for stack in self._service_stacks]):
                self._save_item(item_id, data_item)
    
    def _save_item(self, item_id, data):
        self.data_partitioner.append(data)
        if item_id in self._data_digest: self._data_digest.pop(item_id)
        for stack in self._service_stacks.values():
            if item_id in stack: stack.remove(item_id)
        if item_id in self._error_record: self._error_record.pop(item_id)

    def _generate_item(self, index):
        self._data_digest[index] = {
            'genius_id' : index
        }

        for stack in self._service_stacks:
            stack.insert(0, index)

        self._error_record[index] = {
            'genius' : 0,
            'spotify' : 0,
            'youtube' : 0,
            'soundcloud' : 0
        }

    def save(self):
        pd.DataFrame({'indices' : self.indices}).to_csv(self.id_file, index = False)