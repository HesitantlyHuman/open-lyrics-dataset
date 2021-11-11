import aiohttp

class AsyncRandomClient():
    def __init__(self, proxy_file = 'network/rotating_client/proxies.json', headers_file = 'network/rotating_client/headers.json'):
        self.session = aiohttp.ClientSession()

    async def get(self, url, **kwargs):
        params = {
            'headers' : self.get_headers(),
            'proxy' : self.get_proxy(),
            'cookies' : {}
        }
        params = params.update(kwargs)

        return await self.session.get(url = url, **params)

    async def post(self, url, **kwargs):
        params = {
            'headers' : self.get_headers(),
            'proxy' : self.get_proxy(),
            'cookies' : {}
        }
        params = params.update(kwargs)

        return await self.session.post(url = url, **params)

    async def close(self):
        await self.session.close()

    def get_proxy(self):
        return None

    def get_headers(self):
        return None
