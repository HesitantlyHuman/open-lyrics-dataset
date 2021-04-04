#TODO: Implement... :<
import pandas as pd
import os
 
#Configure so that the save frequency can be smaller than the partition lengths
#This would additionally require loading the last csv and checking its length when we first create the partitioner
class DataPartitioner():
    def __init__(self, save_location = './data/', progress_file = './info/logging/progress.txt', partition_length = 8192):
        self.lyrics_location = os.path.join(save_location, 'lyrics/raw')
        self.meta_location = os.path.join(save_location, 'meta')
        self.progress_file = progress_file

        self.partition_length = partition_length
        
        self._temp_lyrics = []
        self._temp_meta = []
        
        self._all_keys = ['genius_id']
        self._lyrics_keys = ['lyrics']

        self.current_file_number = self.get_current_file_number()
        self.current_index = self.get_last_index()

    def append(self, incoming_data):
        #Grab the lyrics and id
        lyric_info = {key: incoming_data[key] for key in incoming_data.keys() if key in self._lyrics_keys or key in self._all_keys}
        #All the other stuff
        meta_data = {key: incoming_data[key] for key in incoming_data.keys() if key not in self._lyrics_keys}

        self._temp_lyrics.append(lyric_info)
        self._temp_meta.append(meta_data)

        if len(self._temp_lyrics) >= self.partition_length:
            self.save_collected_items()
            self._temp_lyrics = []
            self._temp_meta = []
            self.current_file_number += 1

    def save_collected_items(self):
        lyrics_to_save = pd.DataFrame(self._temp_lyrics)
        lyrics_save_path = os.path.join(self.lyrics_location, 'open-lyrics-{:3.}.csv'.format(self.current_file_number))
        lyrics_to_save.to_csv(lyrics_save_path)

        meta_to_save = pd.DataFrame(self._temp_lyrics)
        meta_save_path = os.path.join(self.lyrics_location, 'open-lyrics-meta-{:3.}.csv'.format(self.current_file_number))
        meta_to_save.to_csv(meta_save_path)

        self.save_index(self.current_index)

    def save_index(self, index_to_save):
        index_dataframe = pd.read_csv(self.progress_file, index_col = 'service')
        index_dataframe['collection_progress']['genius'] = index_to_save
        index_dataframe.to_csv(self.progress_file, index = False)

    def get_last_index(self):
        index_dataframe = pd.read_csv(self.progress_file, index_col = 'service')
        return index_dataframe['collection_progress']['genius']
        
    def update_index(self, index):
        self.current_index = index

    def get_current_file_number(self):
        latest_save_file = os.listdir(self.lyrics_location)[-1]
        latest_save_number = int(latest_save_file.split('-')[-1].split('.')[0])
        return latest_save_number + 1