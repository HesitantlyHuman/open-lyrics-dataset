import aiohttp
import asyncio
import json

from bs4 import BeautifulSoup

from utilities.utils import try_dictionary_access

class GeniusInterface():
    def __init__(self, configuration_file = './info/services.json', timeout = 100):
        with open(configuration_file) as json_file:
            genius_oauth_data = json.load(json_file)['genius']['oauth']

        self.timeout = timeout
        self.token = genius_oauth_data['client-access-token']
        self.base_url = genius_oauth_data['base-url']

        self.session = aiohttp.ClientSession()

    async def get_song(self, index):
        '''Takes a Genius song id, and returns a songs lyrics and metadata as a python dictionary. Returns none if no song exists at that endpoint'''
        song_item = await self.get_api_data(index)
        
        if song_item is None:
            return None

        if not song_item['genius_url'] is None:
            url = 'https://genius.com' + song_item['genius_url']
            web_data = await self.get_html_data(url)
            song_item.update(web_data)

        return song_item

    async def get_html_data(self, url):
        async with self.session.get(url, timeout = self.timeout) as response:
            html = await response.text()
        song_page_soup = BeautifulSoup(html, 'html.parser')
        lyrics = song_page_soup.find('div', class_='lyrics').get_text()
        genres = try_dictionary_access(json.loads(song_page_soup.find('meta', itemprop='page_data')['content']), ['dmp_data_layer', 'page', 'genres'])

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
                    raise RuntimeError('Encountered an unexpected network response of: {} from Genius API with message:\n {}'.format(response.status, message))
            else:
                api_response = await response.json()

        title = try_dictionary_access(api_response, ['response', 'song', 'title'])
        artist = try_dictionary_access(api_response, ['response', 'song', 'primary_artist', 'name'])
        song_path = try_dictionary_access(api_response, ['response', 'song', 'path'])
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
            'genius_url' : song_path
        }

        return api_data

    async def close(self):
        await self.session.close()