import pandas as pd
import re
import os
 
#Configure so that the save frequency can be smaller than the partition lengths
#This would additionally require loading the last csv and checking its length when we first create the partitioner
class DataPartitioner():
    def __init__(self, save_location = './data/', progress_file = './info/logging/progress.txt', partition_length = 8192):
        self.lyrics_location = os.path.join(save_location, 'lyrics/raw')
        self.meta_location = os.path.join(save_location, 'meta')
        self.progress_file = progress_file

        for necessary_path in [self.lyrics_location, self.meta_location]:
            DataPartitioner.verify_directory(necessary_path)

        self.partition_length = partition_length
        
        self._temp_lyrics = []
        self._temp_meta = []
        
        self._all_keys = ['genius_id']
        self._lyrics_keys = ['lyrics']

        self._lyric_save_format = 'open-lyrics-{:03}.csv'
        self._meta_save_format = 'open-lyrics-meta-{:03}.csv'

        self.current_file_number = 0

        self.load_from_previous_if_exists(self.lyrics_location, self.meta_location, self.progress_file)
        self.current_index = self.get_last_index()

    def append(self, incoming_data):
        #Grab the lyrics and id
        lyric_info = {key: incoming_data[key] for key in incoming_data.keys() if key in self._lyrics_keys or key in self._all_keys}
        #All the other stuff
        metadata = {key: incoming_data[key] for key in incoming_data.keys() if key not in self._lyrics_keys}

        self._temp_lyrics.append(lyric_info)
        self._temp_meta.append(metadata)

        if len(self._temp_lyrics) >= self.partition_length:
            self.save_collected_items()
            self._temp_lyrics = []
            self._temp_meta = []
            self.current_file_number += 1

    def save_collected_items(self):
        lyrics_to_save = pd.DataFrame(self._temp_lyrics)
        lyrics_save_path = os.path.join(self.lyrics_location, self._lyric_save_format.format(self.current_file_number))
        lyrics_to_save.to_csv(lyrics_save_path, index = False)

        meta_to_save = pd.DataFrame(self._temp_meta)
        meta_save_path = os.path.join(self.meta_location, self._meta_save_format.format(self.current_file_number))
        meta_to_save.to_csv(meta_save_path, index = False)

        self.save_index(self.current_index)

    def load_from_previous_if_exists(self, lyrics_location, metadata_location, progress_file):
        lyric_regex_string = re.sub('\{.+\}', '[0-9]+', self._lyric_save_format)
        meta_regex_string = re.sub('\{.+\}', '[0-9]+', self._meta_save_format)
        lyrics_file_names = [file_name for file_name in os.listdir(lyrics_location) if re.match(lyric_regex_string, file_name)]
        meta_file_names = [file_name for file_name in os.listdir(metadata_location) if re.match(meta_regex_string, file_name)]

        assert len(lyrics_file_names) == len(meta_file_names), 'There are unequal numbers of meta files and lyrics files'

        if len(lyrics_file_names) == 0:
            return

        lyrics_number = int(re.findall('[0-9]+', lyrics_file_names[-1])[0])
        meta_number = int(re.findall('[0-9]+', meta_file_names[-1])[0])

        assert lyrics_number == meta_number, 'Lyrics and meta file numbers do not match!'

        loaded_lyrics_dataframe = pd.read_csv(os.path.join(lyrics_location, lyrics_file_names[-1]))
        loaded_meta_dataframe = pd.read_csv(os.path.join(metadata_location, meta_file_names[-1]))

        self._temp_lyrics = loaded_lyrics_dataframe.to_dict(orient = 'records')
        self._temp_meta = loaded_meta_dataframe.to_dict(orient = 'records')

        self.current_file_number = lyrics_number

    def save_index(self, index_to_save):
        index_dataframe = pd.read_csv(self.progress_file, index_col = 'service')
        index_dataframe['collection_progress']['genius'] = index_to_save
        index_dataframe.to_csv(self.progress_file)

    def get_last_index(self):
        index_dataframe = pd.read_csv(self.progress_file, index_col = 'service')
        return index_dataframe['collection_progress']['genius']
        
    def update_index(self, index):
        if index > self.current_index:
            self.current_index = index

    def verify_directory(file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)