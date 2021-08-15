import io
import aiohttp
import json

async def session_bytes(url, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            data = io.BytesIO(await r.read())
            return data
async def session_json(url, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            return await r.json()
async def session_text(url, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            return json.loads((await r.text()))