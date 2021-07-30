from tqdm import tqdm
from data_management import DataPartitioner
from collectors import *
from dispatch import *

def collect():
    with DataPartitioner('./data/') as data_partitioner:
        pbar = tqdm(total = 6703114)

        dispatch_workers = [
            GeniusDispatcher(GeniusCollector()),
            ServiceDispatcher(SpotifyCollector()),
            ServiceDispatcher(YoutubeCollector()),
            ServiceDispatcher(SoundcloudCollector())
        ]

        dispatch_pool = DispatchPool(
            dispatchers = dispatch_workers,
            data_partitioner = data_partitioner,
            progress_bar = pbar
        )

        dispatch_pool.start_services()

if __name__ == '__main__':
    collect()