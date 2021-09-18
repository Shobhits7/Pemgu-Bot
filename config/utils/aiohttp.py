import aiohttp, io, json

async def r_json(session, error=str, url=str, headers=None):
    async with session.get(url) as r:
        if r.status != 200:
            return error
        return await r.json()

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