import pandas as pd

csv_file_location = 'dataset-location-here'
#It is recommended that chunk size is a multiple of your batch size if you are using the dataset to train an ML model
chunk_size = 2048

with pd.read_csv(csv_file_location, chunksize = chunk_size) as openLyrics:
    #Do the things here
    pass

#TODO: create dataloader wrappers for both tensorflow and pytorch