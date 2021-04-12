#Use argh for this guy, to make it really nice to use
#import argh
import pandas as pd
import asyncio
import csv
import os

from tqdm import tqdm

from network.genius_interface import GeniusInterface
from data_management.data_partitioner import DataPartitioner
from collectors import collection_worker

async def scrape_genius(save_location, n_workers = 5, progress_file = './logging/progress.txt', start_index = None):

    data_partitioner = DataPartitioner(save_location, partition_length = 10)

    if start_index is None:
        start_index = data_partitioner.get_last_index()

    interface = GeniusInterface(start_index)

    workers = []
    for worker_num in range(n_workers):
        worker = asyncio.create_task(collection_worker(interface, data_partitioner))

    pbar = tqdm(total = 100, position = 0, leave = True)
    while interface.has_next():
        pbar.update(interface.index - pbar.n - start_index)

    for worker in workers:
        worker.cancel()
    
    await interface.close()

#Argh stuff
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape_genius('./data/'))