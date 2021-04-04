import pytest
import json

from genius_interface import GeniusInterface
with open('../info/services.json') as json_file:
    data = json.load(json_file)
    token = data['genius']['oath']['client-access-token']

#TODO: create test cases
genius_interface_cases = [
]

@pytest.mark.parametrize('index, expected_response', genius_interface_cases)
def test_genius_interface(index, expected_response):
    interface = GeniusInterface(token = token)
    assert interface.get_song_item(index) == expected_response