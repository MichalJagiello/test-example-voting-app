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
    # post_session = get_session
    post_session = aiohttp.ClientSession(cookies={'voter_id': resp.cookies.get('voter_id')})
    post_resp = yield from post_session.post(url, data={'vote': 'a' if random.random() < 0.5 else 'b'})
    t2 = time.time()
    yield from post_resp.release()
    yield from resp.release()
    yield from post_session.close()
    yield from get_session.close()
    r = t2 - t1
    res.append(r)


def get_request(url):
	return requests.get(url)


def post_request(url, cookies):
	return requests.post(url, cookies=cookies,
	                     data={'vote': 'a' if random.random() < 0.5 else 'b'})

@asyncio.coroutine
def make_vote_requests(res, url):
    t1 = time.time()
    loop = asyncio.get_event_loop()
    get_fut = loop.run_in_executor(None, get_request, url)
    resp = yield from get_fut
    post_fut = loop.run_in_executor(None, post_request, url,
                                    {'voter_id': resp.cookies.get('voter_id')})
    yield from post_fut
    # yield from get_request(url)
    # yield from post_request(url,
    #                         {'voter_id': resp.cookies.get('voter_id')})
    # get_session = aiohttp.ClientSession()
    # resp = requests.get(url)
    # requests.post(url,
	#               cookies={'voter_id': resp.cookies.get('voter_id')},
	# 			  data={'vote': 'a' if random.random() < 0.5 else 'b'})
    t2 = time.time()
    r = t2 - t1
    res.append(r)


@asyncio.coroutine
def sleep_test(char):
	print("{} begin".format(char))
	yield from asyncio.sleep(1)
	print("{} end".format(char))


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
        futures = []
        c = 0
        number_of_requests = 1 << (i + 5)
        while c < windows_length:
            for n in range(number_of_requests):
                 futures.append(asyncio.async(callable(res, *args, **kwargs)))
            c += 1
            yield from asyncio.sleep(1)
        yield from asyncio.wait(futures)
        print("Number of requests: {}".format(number_of_requests))
        print("Median: {}".format(sorted(res)[len(res)//2]))
        print("Srednia: {}".format(sum(res)/len(res)))
    # print("\n\n")


@asyncio.coroutine
def aaaaa():
	import string
	futures = []
	for char in string.ascii_lowercase:
		futures.append(asyncio.async(sleep_test(char)))
	yield from asyncio.gather(*futures)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        # loop.run_until_complete(aaaaa())
        loop.run_until_complete(worker_with_count(5, 5, make_vote_requests, 'http://192.168.99.100/'))
        # loop.run_until_complete(worker_with_count(10, 100, make_vote, 'http://192.168.99.100:8000/'))
    finally:
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        loop.stop()
        loop.close()
