import aiohttp
import asyncio
import json

from bs4 import BeautifulSoup

class GeniusInterface():
    def __init__(self, configuration_file = './info/services.json', timeout = 100):
        with open(configuration_file) as json_file:
            genius_config_data = json.load(json_file)['genius']

        self.timeout = timeout
        self.token = genius_config_data['auth']['client-access-token']
        self.base_url = genius_config_data['auth']['base-url']
        self.cookie = genius_config_data['html']['cookie']

        self.session = aiohttp.ClientSession()

    async def get_html_data(self, url):
        headers = {
            'Cookie' : self.cookie
        }

        async with self.session.get(url, timeout = self.timeout, headers = headers) as response:
            response_message = await response.text()
            if not response.status == 200:
                raise RuntimeError('Genius collection failed')
            
        song_page_soup = BeautifulSoup(response_message, 'lxml')

        lyric_div = song_page_soup.find('div', {'class' : 'lyrics'})
        if lyric_div is not None:
            lyrics = lyric_div.get_text()
        else:
            lyrics = None

        meta_container = song_page_soup.find('meta', {'itemprop' : 'page_data'})
        if meta_container is not None:
            genres = json.loads(meta_container['content']).get('dmp_data_layer', {}).get('page', {}).get('genres', None)
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
                message = await response.text()
                raise RuntimeError('Genius collection failed')
            else:
                api_response = await response.json()
        
        return api_response.get('response', {}).get('song', {})

    async def close(self):
        await self.session.close()