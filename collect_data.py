#Use argh for this guy, to make it really nice to use
#import argh
import pandas as pd
import asyncio
import csv
import os

from tqdm import tqdm

from network.genius_interface import GeniusInterface
from data_management.data_partitioner import DataPartitioner
from collectors import GeniusCollector

async def collect(collector, data_partitioner, progress_bar = None):
    data = await next(collector)
    data_partitioner.append(data)

    if progress_bar is not None:
        progress_bar.update(1)

async def scrape_genius(save_location, requests_per_second = 1):
    with DataPartitioner(save_location, partition_length = 1000) as data_partitioner:
        async with GeniusCollector() as collector:
            pbar = tqdm(total = collector.max_index, position = 0, leave = True)
            while collector.has_next():
                asyncio.create_task(collect(collector, data_partitioner, progress_bar = pbar))
                await asyncio.sleep(1 / requests_per_second)

#Argh stuff
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape_genius('./data/'))