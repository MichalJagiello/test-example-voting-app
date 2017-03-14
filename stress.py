import aiohttp
import asyncio
import time
import random
import signal
import requests


@asyncio.coroutine
def make_vote(res, url):
    t1 = time.time()
    get_session = aiohttp.ClientSession()
    resp = yield from get_session.get(url)
    t2 = time.time()
    post_session = aiohttp.ClientSession(cookies={'voter_id': resp.cookies.get('voter_id')})
    post_resp = yield from post_session.post(url, data={'vote': 'a' if random.random() < 0.5 else 'b'})
    yield from post_resp.release()
    yield from post_session.close()
    yield from resp.release()
    yield from get_session.close()
    r = t2 - t1
    res.append(r)


# @asyncio.coroutine
# def vote():
#     loop = asyncio.get_event_loop()
#     t1 = time.time()
#     r = requests.get('http://192.168.99.102:5000/')
#     if r.status_code != 200:
#         raise Exception("Dead")
#     requests.post('http://192.168.99.102:5000/', cookies={'voter_id': r.cookies.get('voter_id')}, data={'vote': 'a' if random.random() < 0.5 else 'b'})
#
#
# @asyncio.coroutine
# def call_api(l, address):
#     loop = asyncio.get_event_loop()
#     t1 = time.time()
#     future = loop.run_in_executor(None, requests.get, address)
#     res = yield from future
#     t2 = time.time()
#     r = t2 - t1
#     l.append(r)


@asyncio.coroutine
def worker_with_count(number_of_windows, windows_length, callable, *args, **kwargs):
    futures = []
    for i in range(number_of_windows):
        res = []
        c = 0
        number_of_requests = 1 << i
        while c < windows_length:
            futures = []
            for n in range(number_of_requests):
                 futures.append(asyncio.async(callable(res, *args, **kwargs)))
            yield from asyncio.gather(*futures)
            c += 1
        print("Number of requests: {}".format(number_of_requests))
        print("Median: {}".format(sorted(res)[len(res)//2]))
    # print("\n\n")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker_with_count(5, 100, make_vote, 'http://192.168.99.100:5000/'))
        # loop.run_until_complete(worker_with_count(10, 100, make_vote, 'http://192.168.99.100:8000/'))
    finally:
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        loop.stop()
        loop.close()
