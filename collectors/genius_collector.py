import json
import pandas as pd
import os
import random

from network import GeniusInterface
from utils import noneless_dictionary_update

class GeniusCollector():
    def __init__(self, interface = GeniusInterface()):
        self.interface = interface

    async def update(self, data_item):
        genius_id = data_item.get('genius_id', None)

        if not genius_id is None:
            api_data = self._get_api_data(genius_id)
            noneless_dictionary_update(data_item, api_data)

            genius_url = data_item.get('genius_url', None)
            if not genius_url is None:
                html_data = self._get_html_data(genius_url)
                noneless_dictionary_update(data_item, html_data)
        else:
            return data_item

    async def _get_html_data(self, genius_url):
        song_html_data = await self.interface.get_html_data(genius_url)

        return song_html_data

    async def _get_api_data(self, genius_id):
        song_api_data = await self.interface.get_api_data(genius_id)

        media_urls = GeniusCollector._retreive_media_urls(song_api_data, ['spotify', 'youtube', 'soundcloud'])

        api_data = {
            'genius_album_id' : song_api_data.get('album', {}).get('id', None),
            'title' : song_api_data.get('title', None),
            'album' : song_api_data.get('album', {}).get('name', None),
            'artist' : song_api_data.get('primary_artist', {}).get('name', None),
            'release_date' : song_api_data.get('release_date', None),
            'genius_url' : song_api_data.get('url', None)
        }
        api_data.update(media_urls)

        return api_data

    def _retreive_media_urls(genius_api_call, services):
        services = [service.lower() for service in services]
        urls = {service + '_url' : None for service in services}

        media_objects = genius_api_call.get('media', [])
        for media_object in media_objects:
            provider = media_object.get('provider', '')
            if provider.lower() in services:
                urls.update({provider.lower() + '_url' : media_object.get('url', None)})
        return urls