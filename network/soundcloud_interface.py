import aiohttp
import json

from bs4 import BeautifulSoup

class SoundcloudInterface():
    def __init__(self, configuration_file = './info/services.json', timeout = 100):
        with open(configuration_file) as json_file:
            soundcloud_configuration_data = json.load(json_file).get('soundcloud', None)

    async def get_data(self, url):
        return None