import httpx
import json
import pandas as pd

from bs4 import BeautifulSoup

#Annoyingly, the configuration file default location needs to be changed depending on the scope from which you call the interface
#TODO: make it not be that way!
class GeniusInterface():
    def __init__(self, index = 1, configuration_file = './info/services.json', timeout = 50):
        with open(configuration_file) as json_file:
            genius_service_data = json.load(json_file)['genius']

        self.index = index
        self.timeout = timeout
        self.token = genius_service_data['oauth']['client-access-token']
        self.base_url = genius_service_data['oauth']['base-url']
        self.min_index = genius_service_data['query']['min-id']
        self.max_index = genius_service_data['query']['max-id']

        assert self.min_index <= self.index <= self.max_index, 'Index must be between the min-id of {} and the max-id of {}'.format(self.min_index, self.max_index)

    def __next__(self):
        if self.index <= self.max_index:
            next_song = None
            #We only want to return an actual song, and not None
            while next_song is None:
                next_song = self.get_song(self.index)
                self.index += 1
            return next_song
        else:
            raise StopIteration

    def __iter__(self):
        return self

    def get_song(self, index):
        '''Takes a Genius song id, and returns a songs lyrics and metadata as a python dictionary'''
        api_response = self.query_index(index)
        if api_response is None:
            return None

        #Data accessable by the API
        title = try_dictionary_access(api_response, ['response', 'song', 'title'])
        artist = try_dictionary_access(api_response, ['response', 'song', 'primary_artist', 'name'])
        song_path = try_dictionary_access(api_response, ['response', 'song', 'path'])
        release_date = try_dictionary_access(api_response, ['response', 'song', 'release_date'])
        album_id = try_dictionary_access(api_response, ['response', 'song', 'album', 'id'])
        album_name = try_dictionary_access(api_response, ['response', 'song', 'album', 'name'])

        #Data accessable only via the html
        if not song_path is None:
            url = 'https://genius.com' + song_path
            song_page_soup = BeautifulSoup(httpx.get(url, timeout = self.timeout).text, 'html.parser')
            lyrics = song_page_soup.find('div', class_='lyrics').get_text()
            genres = try_dictionary_access(json.loads(song_page_soup.find('meta', itemprop='page_data')['content']), ['dmp_data_layer', 'page', 'genres'])
        else:
            url = None
            lyrics = None
            genres = None

        return {'genius_id' : index,
                'genius_album_id' : album_id,
                'title' : title,
                'album' : album_name,
                'artist' : artist,
                'lyrics' : lyrics,
                'genres' : genres,
                'release_date' : release_date,
                'genius_url' : url}

    def query_index(self, index):
        api_header = {
            'Accept' : 'application/json',
            'Host' : 'api.genius.com',
            'Authorization' : 'Bearer ' + self.token
        }

        api_response = httpx.get(self.base_url + '/songs/' + str(index), headers = api_header, timeout = self.timeout)

        if not api_response.status_code == httpx.codes.ok:
            if api_response.status_code == 404:
                return None
            else:
                raise RuntimeError('Encountered an unexpected network response of: {} from Genius API with message:\n {}'.format(api_response, api_response.text))
        else:
            api_response = api_response.json()

        return api_response

def try_dictionary_access(dictionary, keys):
    '''Tries to access a value in a nested dictionary, returns None if it fails'''
    try:
        for key in keys:
            dictionary = dictionary[key]
        return dictionary
    except (TypeError, KeyError) as error:
        return None
