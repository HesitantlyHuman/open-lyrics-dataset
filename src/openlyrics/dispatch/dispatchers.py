import asyncio
import pandas as pd
import random
import json
import os
import time

from openlyrics.errors import TooFastError

class DispatchPool():
    def __init__(self, dispatchers, data_partitioner, progress_bar = None):
        self.pool = {}
        self.progress_bar = progress_bar
        self.data_partitioner = data_partitioner
        self.dispatchers = dispatchers
        for dispatcher in self.dispatchers:
            dispatcher.data_pool = self

    def start_services(self):
        loop = asyncio.get_event_loop()
        for dispatcher in self.dispatchers:
            loop.create_task(dispatcher.start_service_loop())
        loop.run_forever()

    def __getitem__(self, key):
        return self.pool[key]

    def __setitem__(self, key, value):
        self.pool[key] = value

        if all([not key in dispatcher.stack for dispatcher in self.dispatchers]):
            self.data_partitioner.update(self.pool[key])
            del self.pool[key]

            if not self.progress_bar is None:
                self.progress_bar.update(1)

class ServiceDispatcher():
    def __init__(self, collector, data_pool = None, rate = 10, error_threshold = 3):
        self.stack = []
        self.error_record = {}
        self.collector = collector
        self.data_pool = data_pool
        self.rate = 1 / rate
        self.error_threshold = error_threshold

    async def start_service_loop(self):
        while True:
            start = time.time()
            try:
                await self.update_next_item()
            except TooFastError as e:
                await asyncio.sleep(e.wait)
            await asyncio.sleep(self.rate - (start - time.time()))

    async def update_next_item(self):
        item_id = self.stack.pop()
        data_item = self.get_next_item(item_id)
        try:
            self.data_pool[item_id] = await self.collector.update_item(data_item)
        except TooFastError as e:
            self.stack.insert(0, item_id)
            raise e
        except:
            self.error_record[item_id] += 1

            if self.error_record[item_id] < self.error_threshold:
                self.stack.insert(0, item_id)
            else:
                self.data_pool.update_item(data_item)

    def get_next_item(self, item_id):
        return self.data_pool[item_id]


class GeniusDispatcher(ServiceDispatcher):
    def __init__(self, collector, data_pool = None, configuration_file = './info/services.json', id_file = './info/collection/genius_ids.csv', **kwargs):
        super().__init__(collector, data_pool, kwargs)

        self.id_file = id_file

        with open(configuration_file) as json_file:
            collection_data = json.load(json_file)['genius']['collection']
        
        if os.path.exists(id_file):
            self.stack = list(pd.read_csv(id_file)['indices'].values)
        else:
            self.stack = [i for i in range(collection_data['min_id'], collection_data['max-id'])]
            random.shuffle(self.stack)
            self.save()

    def get_next_item(self, item_id):
        return {
            'genius_id' : item_id
        }

    def save(self):
        pd.DataFrame({'indices' : self.stack}).to_csv(self.id_file, index = False)