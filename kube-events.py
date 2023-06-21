import aiohttp
import asyncio
import ssl

from genctl_aio._auth import KubeAuth


auth = KubeAuth()
auth.load_kubeconfig()
print(dir(auth))
print(auth.server_ca_file)
print(auth.client_cert_file)
print(auth.client_key_file)
print(auth.server)
print(auth.username)


url = auth.server + "/api/v1/events?watch=true"
print(url)
# url = "https://127.0.0.1:45855/api/v1/events"
params= {"watch": "true"}
headers = {"content-type": "application/json"}

sslContext = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=auth.server_ca_file)
sslContext.load_cert_chain(certfile=auth.client_cert_file, keyfile=auth.client_key_file, password=None)

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url, params=params, ssl=sslContext) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
                else:
                    print(msg.data)

url = auth.server + "/api/v1/pods?watch=true"

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=sslContext) as resp:
            print(resp.status)
            async for line in resp.content:
                print(line)
asyncio.run(main())
