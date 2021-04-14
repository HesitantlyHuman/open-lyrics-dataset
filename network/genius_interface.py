import aiohttp
import asyncio
import json

from bs4 import BeautifulSoup

from utilities.utils import try_dictionary_access

class GeniusInterface():
    def __init__(self, configuration_file = './info/services.json', timeout = 100):
        with open(configuration_file) as json_file:
            genius_config_data = json.load(json_file)['genius']

        self.timeout = timeout
        self.token = genius_config_data['oauth']['client-access-token']
        self.base_url = genius_config_data['oauth']['base-url']

        self.cookie = genius_config_data['html']['cookie']

        self.session = aiohttp.ClientSession()

    async def get_song(self, index):
        '''Takes a Genius song id, and returns a songs lyrics and metadata as a python dictionary. Returns none if no song exists at that endpoint'''
        song_item = await self.get_api_data(index)

        if song_item is None:
            return None

        if not song_item['genius_url'] is None:
            web_data = await self.get_html_data(song_item['genius_url'])
            song_item.update(web_data)

        return song_item

    async def get_html_data(self, url):

        headers = {
            'Cookie' : self.cookie
        }

        async with self.session.get(url, timeout = self.timeout, headers = headers) as response:
            html = await response.text()
        song_page_soup = BeautifulSoup(html, 'lmxl')

        lyric_div = song_page_soup.find('div', {'class' : 'lyrics'})
        if lyric_div is not None:
            lyrics = lyric_div.get_text()
        else:
            lyrics = None

        meta_container = song_page_soup.find('meta', {'itemprop' : 'page_data'})
        if meta_container is not None:
            genres = try_dictionary_access(json.loads(meta_container['content']), ['dmp_data_layer', 'page', 'genres'])
        else:
            genres = None

        return {
            'lyrics' : lyrics,
            'genres' : genres
        }

    async def get_api_data(self, index):
        api_header = {
            'Accept' : 'application/json',
            'Host' : 'api.genius.com',
            'Authorization' : 'Bearer ' + self.token
        }

        async with self.session.get(self.base_url + '/songs/' + str(index), headers = api_header, timeout = self.timeout) as response:
            if not response.status == 200:
                if response.status == 404:
                    return None
                else:
                    message = await response.text()
                    raise RuntimeError(f'Encountered an unexpected network response of: {response.status} from Genius API with message: {message} when performing query of index: {index}')
            else:
                api_response = await response.json()

        title = try_dictionary_access(api_response, ['response', 'song', 'title'])
        artist = try_dictionary_access(api_response, ['response', 'song', 'primary_artist', 'name'])
        genius_url = try_dictionary_access(api_response, ['response', 'song', 'url'])
        release_date = try_dictionary_access(api_response, ['response', 'song', 'release_date'])
        album_id = try_dictionary_access(api_response, ['response', 'song', 'album', 'id'])
        album_name = try_dictionary_access(api_response, ['response', 'song', 'album', 'name'])

        api_data = {
            'genius_id' : index,
            'genius_album_id' : album_id,
            'title' : title,
            'album' : album_name,
            'artist' : artist,
            'release_date' : release_date,
            'genius_url' : genius_url
        }

        return api_data

    async def close(self):
        await self.session.close()