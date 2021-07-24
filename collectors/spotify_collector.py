import json
import os
import time
import datetime

from network import SpotifyInterface

from utils import noneless_dictionary_update

class SpotifyCollector():
    def __init__(self, configuration_file = './info/services.json', interface = SpotifyInterface()):
        self.interface = interface

    async def update_item(self, data_item):
        spotify_data = await self._get_spotify_data(data_item)
        noneless_dictionary_update(data_item, spotify_data)

        listens_data = await self._get_listens_data(data_item)
        noneless_dictionary_update(data_item, listens_data)

        artist_data = await self._get_artist_data(data_item)
        noneless_dictionary_update(data_item, artist_data)

        data_item['spotify_collection_time'] = time.time()
        data_item['spotify_collection_time_human'] = datetime.now()

        return data_item

    async def _get_spotify_data(self, data_item):
        spotify_song_id = data_item.get('spotify_song_id', None)

        if spotify_song_id is None:
            spotify_url = data_item.get('spotify_url', None)
            if spotify_url is None:
                title = data_item.get('title', None)
                if title is None:
                    return {}

                artist = data_item.get('artist', None)
                spotify_track_data = await self.interface.search_by_string(title + artist)
            else:
                spotify_song_id = spotify_url.split('/')[-1]
                spotify_track_data = await self.interface.search_by_id(spotify_song_id)
        else:
            spotify_track_data = await self.interface.search_by_id(spotify_song_id)
            

        return {
            'spotify_popularity' : spotify_track_data.get('popularity', None),
            'duration_ms' : spotify_track_data.get('duration_ms', None),
            'explicit' : spotify_track_data.get('explicit', None),
            'spotify_song_id' : spotify_track_data.get('id', None),
            'spotify_album_id' : spotify_track_data.get('album', {}).get('id', None),
            'spotify_artist_id' : spotify_track_data.get('artists', [{}])[0].get('id', None)
        }

    async def _get_listens_data(self, data_item):
        spotify_song_id = data_item.get('spotify_song_id', None)
        spotify_album_id = data_item.get('spotify_album_id', None)
        song_listens_data = await self.interface.get_song_data(spotify_song_id, spotify_album_id)

        return {
            'spotify_listens' : song_listens_data.get('playcount', None)
        }

    async def _get_artist_data(self, data_item):
        spotify_artist_id = data_item.get('spotify_artist_id', None)
        artist_listens_data = await self.interface.get_artist_data(spotify_artist_id)

        return {
            'spotify_artist_monthly_listeners' : artist_listens_data.get('monthly_listeners', {}).get('listener_count', None)
        }
        