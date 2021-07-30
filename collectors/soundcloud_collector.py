import json
import os
import time
import datetime

from network import SoundcloudInterface

from utils import noneless_dictionary_update

class SoundcloudCollector():
    def __init__(self, configuration_file = './info/services.json', interface = SoundcloudInterface()):
        self.interface = interface

    async def update_item(self, data_item):

        soundcloud_url = data_item.get('soundcloud_url', None)
        if not soundcloud_url is None:
            new_data = self.interface.get_track_details(soundcloud_url)
        else:
            song_title = data_item.get('title', None)
            if not song_title is None:
                artist = data_item.get('artist', '')
                soundcloud_url = self.interface.get_song_url(song_title, artist)
                new_data = self.interface.get_track_details(soundcloud_url)
            else:
                new_data = {}

        data_item = noneless_dictionary_update(data_item, new_data)
        return data_item
        