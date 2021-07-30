import aiohttp
import json

from bs4 import BeautifulSoup

class SoundcloudInterface():
    def __init__(self, configuration_file = './info/services.json', timeout = 100):
        with open(configuration_file) as json_file:
            soundcloud_configuration_data = json.load(json_file).get('soundcloud', None)

        self.session = aiohttp.ClientSession()

    async def get_song_url(self, song_title, song_artist):
        params = {
            'q' : song_title + ' ' + song_artist
        }

        response = await self.session.get('https://soundcloud.com/search/sounds', params = params)
        soup = BeautifulSoup(response.text)
        return soup.find('div', {'id' : 'app'}).find_all('ul')[1].find('a')['href']

    async def get_track_details(self, track_url):
        response = await self.session.get(track_url)
        soup = BeautifulSoup(response.text)

        return {
            'soundcloud_likes' : soup.find('meta', {'property' : 'soundcloud:like_count'})['content'],
            'soundcloud_downloads' : soup.find('meta', {'property' : 'soundcloud:download_count'})['content'],
            'soundcloud_comments' : soup.find('meta', {'property' : 'soundcloud:comments_count'})['content'],
            'soundcloud_genre_tags' : soup.find('meta', {'itemprop' : 'genre'})['content'],
            'soundcloud_playcount' : soup.find('meta', {'property' : 'soundcloud:play_count'})['content'],
            'soundcloud_artist_followers' : response.text.split('"followers_count":')[1].split(',"followings_count":')[0]
        }