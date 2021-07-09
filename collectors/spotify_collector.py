import json
import os

from network import SpotifyInterface

class SpotifyCollector():
    def __init__(self, configuration_file = './info/services.json', interface = SpotifyInterface()):
        self.interface = interface

    async def update_item(self, data_item):
        spotify_url = data_item.get('spotify_url', None)

        if spotify_url is None:
            title = data_item.get('title', None)
            if title is None:
                return data_item

            artist = data_item.get('artist', None)
            new_data = await self._get_data_from_search(title + artist)
        else:
            spotify_id = spotify_url.split('/')[-1]
            new_data = await self._get_data_from_id(spotify_id)

        data_item = data_item.update(new_data)
        return data_item

    async def _get_data_from_id(self, spotify_uri):
        return None
    
    async def _get_data_from_search(self, search_term):
        spotify_track_data = self.interface.search_by_string(search_term)
        