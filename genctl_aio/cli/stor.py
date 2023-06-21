
import anyio
import asyncclick as click

from ..session import KubeSession
from ..resources.kube import PodResource

@click.group()
def stor():
    pass

@stor.group()
def watch():
    pass


@stor.command()
async def pods():

    print('pods')
    async with KubeSession() as session:
        await session.load_config()
        pods = session.get_resources("pods")[0]
        response = await pods.list()
        print(response)


@watch.command()
async def pods():
    print('watch pods')
