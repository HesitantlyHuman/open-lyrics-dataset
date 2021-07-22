import json
import os
import time
import datetime

from network import SoundcloudInterface

from utils import noneless_dictionary_update

class SoundcloudCollector():
    def __init__(self, configuration_file = './info/services.json', interface = SoundcloudInterface()):
        self.interface = interface

    async def update_item(self, data_item):
        return data_item