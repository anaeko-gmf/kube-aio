
from aiohttp import hdrs

class BaseResource:

    root = "api"
    group = None
    version = "v1"
    name = None

    def __init__(self, server, session, ssl, ns=None):
        if not self.name:
            raise Exception("BaseResource subclass must define at least 'name'")
        url = [server, self.root, self.group, self.version ]
        url = [ s.strip("/") for s in url if s]
        if ns:
            url.extend(["namespaces", ns])
        url.append(self.name)
        self._url = "/".join(url)
        print(self._url)
        self._session = session
        self._ssl = ssl

    async def _request(self, method, **kwargs):
        kwargs["ssl"] = self._ssl
        return await self._session.request(method, self._url, **kwargs)

    async def _GET(self, **kwargs):
        return await self._request(hdrs.METH_GET, **kwargs)

    async def list(self):
        return await self._GET()
