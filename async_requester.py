import asyncio
import aiohttp
import requests

tasks = []


async def _make_async_req(method: str, url: str, headers, jsonize, session, data, json):
    if (session == None):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, json=json) as resp:
                if resp.status >= 200 and resp.status <= 400:
                    if (jsonize):
                        return await resp.json()
                    return await resp.text()
                else:
                    print("err when req")
                    return ""
    else:
        if (data != None):
            async with session.request(method, url, headers=headers, data=data) as resp:
                if resp.status >= 200 and resp.status <= 400:
                    if (jsonize):
                        return await resp.json()
                    return await resp.text()
                else:
                    print("err when req")
                    return ""
        else:
            async with session.request(method, url, headers=headers, json=json) as resp:
                if resp.status >= 200 and resp.status <= 400:
                    if (jsonize):
                        return await resp.json()
                    return await resp.text()
                else:
                    print("err when req")
                    return ""


async def send_async_request(method: str, url: str, headers=None, jsonize=False, json=None, data=None, session=None):
    if json is None:
        json = {}

    task = asyncio.ensure_future(
        _make_async_req(method, url, headers, jsonize=jsonize, json=json, data=data, session=session))
    tasks.append(task)


async def get_request_result():
    res = await asyncio.gather(*tasks)
    tasks.clear()
    return res


def send_sync_request(method: str, url: str, headers=None, json=None):
    if json is None:
        json = {}
    return requests.request(method=method, url=url, headers=headers, json=json)
