#Use argh for this guy, to make it really nice to use
#import argh
import pandas as pd
import csv
import os
from tqdm import tqdm

from network.genius_interface import GeniusInterface
from data_management.data_partitioner import DataPartitioner

#Currently this is way too slow... we must configure it to use async requests :<
def scrape_genius(save_location, progress_file = './logging/progress.txt', start_index = None):

    data_partitioner = DataPartitioner(save_location)

    if start_index is None:
        start_index = data_partitioner.get_last_index()

    interface = GeniusInterface(start_index)

    pbar = tqdm(interface, position = 0, leave = True, total = 8192)
    for num_collected, song in enumerate(pbar):
        data_partitioner.append(song)
        data_partitioner.update_index(interface.index)

        pbar.update(1)

        if num_collected > 8192:
            break

#Argh stuff
if __name__ == '__main__':
    scrape_genius('./data/')