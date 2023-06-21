
import asyncio
from concurrent.futures import ThreadPoolExecutor
import ssl

import aiohttp

from ._auth import KubeAuth
from .resources.kube import PodResource



class KubeSession:

    _auth = None
    _executor = None
    _session = None
    _ssl = None

    def __init__(self, executor=None):
        self._executor = ThreadPoolExecutor()
        self._session = aiohttp.ClientSession()
        self._auth = None
        self._ssl = None
        self._server = None
        self._resources = {}
        self._register_resources()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    def _load_config(self):
        auth = KubeAuth()
        auth.load_kubeconfig()
        sslContext = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=auth.server_ca_file)
        sslContext.load_cert_chain(certfile=auth.client_cert_file, keyfile=auth.client_key_file, password=None)
        return auth, sslContext

    def _register_resources(self):
        self._resources["pods"] = PodResource

    async def load_config(self):
        loop = asyncio.get_event_loop()
        self._auth, self._ssl = await loop.run_in_executor(self._executor, self._load_config)
        self._server = self._auth.server

    def get_resources(self, *args):
        resources = []
        for arg in args:
            cls = self._resources.get(arg)
            if not cls:
                raise Exception("no resource registered for '%s'" % arg)
            resources.append(cls)

        return [cls(self._server, self._session, self._ssl) for cls in resources]
