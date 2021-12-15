#Maybe use the google search to find the videos?

import re
import aiohttp
import asyncio
import json

from bs4 import BeautifulSoup

class YoutubeInterface():
    def __init__(self, configuration_file = './info/services.json'):
        with open(configuration_file) as json_file:
            youtube_config_data = json.load(json_file)['youtube']

        self.session = aiohttp.ClientSession()

        self.headers = youtube_config_data['collection']['google_headers']

    async def get_urls_from_search(self, song_title, artist_name):
        params = {
            'client' : 'firefox-b-1-d',
            'q' : song_title + ' ' + artist_name + ' youtube'
        }

        response = await self.session.get('https://www.google.com/search', headers = self.headers, params = params)
        response = await response.text()

        soup = BeautifulSoup(response, 'lxml')
        return [result_block.find('a')['href'] for result_block in soup.find('div', {'id' : 'search'}).find_all('div', {'class' : 'g'})]

    async def get_video_data(self, video_url):
        response = await self.session.get(video_url)
        response = await response.text()

        youtube_page_soup = BeautifulSoup(response, 'lxml')

        hidden_data_block = youtube_page_soup.find_all('script')[39]
        hidden_data_raw = hidden_data_block.string
        json_start_location = hidden_data_raw.find('{')
        json_end_location = hidden_data_raw.rfind(';')
        hidden_data = json.loads(hidden_data_raw[json_start_location:json_end_location])
        hidden_data = hidden_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']

        data = {
            'youtube_title' : hidden_data['title']['runs'][0]['text'],
            'youtube_views' : hidden_data['viewCount']['videoViewCountRenderer']['viewCount']['simpleText'],
            'youtube_likes' : hidden_data['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['toggledText']['accessibility']['accessibilityData']['label'],
            'youtube_dislikes' : hidden_data['videoActions']['menuRenderer']['topLevelButtons'][1]['toggleButtonRenderer']['toggledText']['accessibility']['accessibilityData']['label']

        }

        return data

    async def close(self):
        await self.session.close()




