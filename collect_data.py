from dispatch.collection_dispatcher import CollectionDispatcher
import pandas as pd
import asyncio
import csv
import os

from tqdm import tqdm

from network.genius_interface import GeniusInterface
from data_management import DataPartitioner
from collectors import GeniusCollector

class ProgressDataPartitioner():
    def __init__(self, data_partitioner, progress_bar):
        self.data_partitioner = data_partitioner
        self.progress_bar = progress_bar
    
    def update(self, x):
        self.data_partitioner.update(x)
        self.progress_bar.update(1)

async def collect():
    with DataPartitioner('./data/') as data_partitioner:
        pbar = tqdm(total = 6703114)
        partitioner = ProgressDataPartitioner(data_partitioner, pbar)
        with CollectionDispatcher(partitioner) as dispatcher:
            await dispatcher.start_generating_items()
            await dispatcher.start_service('genius')
            await dispatcher.start_service('spotify')
            await dispatcher.start_service('youtube')
            await dispatcher.start_service('soundcloud')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(collect())