import json
import os
import time
import datetime

from network import YoutubeInterface

from utils import noneless_dictionary_update

class YoutubeCollector():
    def __init__(self, configuration_file = './info/services.json', interface = YoutubeInterface()):
        self.interface = interface

    async def update_item(self, data_item):
        youtube_url = data_item.get('youtube_url', None)

        if youtube_url is None:
            song_title = data_item.get('title', None)
            if song_title is None:
                return data_item

            artist_name = data_item.get('artist', None)
            youtube_url = await self.interface.get_video_url_from_search(song_title, artist_name)
        
        youtube_data = await self.interface.get_video_data(youtube_url)
        data_item = noneless_dictionary_update(data_item, youtube_data)

        return data_item