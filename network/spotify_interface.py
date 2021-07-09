import aiohttp
import asyncio
import json
import base64

class SpotifyInterface():
    def __init__(self, configuration_file = './info/services.json', playcount_librespot_endpoint = 'https://api.t4ils.dev'):
        with open(configuration_file) as json_file:
            spotify_config_data = json.load(json_file)['spotify']

        self.oauth_credentials = spotify_config_data['auth']
        self.token = None

        self.session = aiohttp.ClientSession()

        self.listens_endpoint = playcount_librespot_endpoint

    async def search_by_id(self, spotify_song_id):
        pass

    async def search_by_string(self, string):
        if self.token is None:
            self.token = await self._get_token(self.oauth_credentials)

        headers = {
            'Authorization' : self.token
        }
        data = {
            'q' : string,
            'type' : 'track'
        }

        response = await self.session.get('https://api.spotify.com/v1/search', headers = headers, params = data)
        content = await response.text()
        return json.loads(content)['tracks']['items'][0]

    async def get_song_data(self, spotify_song_id, spotify_album_id):
        response = await self.session.get(self.listens_endpoint + '/albumPlayCount?albumid=' + spotify_album_id)
        response = await response.text()
        response = json.loads(response)
        for disc in response['data']['discs']:
            for track in disc['tracks']:
                if track['uri'].split(':')[-1] == spotify_song_id:
                    return track

    async def get_artist_data(self, spotify_artist_id):
        response = await self.session.get(self.listens_endpoint + '/artistInfo?artistid=' + spotify_artist_id)
        response = await response.text()
        response = json.loads(response)
        return response

    async def _get_token(self, oauth_dictionary):
        authorization_id = 'Basic ' + str(base64.b64encode(bytes(oauth_dictionary['client_id'] + ':' + oauth_dictionary['client_secret'],'utf-8')),'utf-8')
        
        headers = {'Authorization' : authorization_id}
        data = {'grant_type' : 'client_credentials'}

        response = await self.session.post(oauth_dictionary['access_token_url'], data = data, headers = headers)
        response = await response.text()
        response = json.loads(response)
        return response['token_type'] + ' ' + response['access_token']

    async def close(self):
        await self.session.close()