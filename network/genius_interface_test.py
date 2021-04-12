import asyncio
import json

from genius_interface import GeniusInterface

async def func():
    interface = GeniusInterface()
    print(await interface.get_html_data('https://genius.com/Drake-u-with-me-lyrics'))
    await interface.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())