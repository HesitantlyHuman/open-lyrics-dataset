import pandas as pd
import asyncio
import csv
import os

from tqdm import tqdm

from network.genius_interface import GeniusInterface
from data_management import DataPartitioner
from collectors import GeniusCollector

async def collect_next(collector, data_partitioner, progress_bar = None):
    data = await next(collector)

    if data is not None:
        data_partitioner.append(data)

    if progress_bar is not None:
        progress_bar.update(1)

async def collection_loop(save_location, collector, requests_per_second = 8):
    async with DataPartitioner(save_location, collector = collector) as data_partitioner:
        pbar = tqdm(total = len(collector.indices), position = 0, leave = True)
        while collector.has_next():
            asyncio.create_task(collect_next(collector, data_partitioner, progress_bar = pbar))
            await asyncio.sleep(1 / requests_per_second)

async def scrape(save_location, site):
    if site.lower() == 'genius':
        async with GeniusCollector() as collector:
            await collection_loop(save_location, collector)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape('./data/', site = 'Genius'))