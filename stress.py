import aiohttp
import asyncio
import time
import random
import requests

import argparse


@asyncio.coroutine
def make_vote(res, url):
    t1 = time.time()
    get_session = aiohttp.ClientSession()
    resp = yield from get_session.get(url)
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
    t2 = time.time()
    r = t2 - t1
    res.append(r)


@asyncio.coroutine
def worker_with_count(number_of_windows, windows_length, callable, *args, **kwargs):
    futures = []
    print("Number of requests per second\tResults")
    for i in range(number_of_windows):
        res = []
        futures = []
        c = 0
        number_of_requests = 1 << i
        while c < windows_length:
            for n in range(number_of_requests):
                futures.append(asyncio.async(callable(res, *args, **kwargs)))
            c += 1
            yield from asyncio.sleep(1)
        yield from asyncio.wait(futures)
        # print("Number of requests: {}".format(number_of_requests))
        # print("Median: {}".format(sorted(res)[len(res)//2]))
        # print("Srednia: {}".format(sum(res)/len(res)))
        print("{} {}".format(number_of_requests, sorted(res)))


def get_argparser():
    parser = argparse.ArgumentParser(description='Example voting app stress '
                                                 'test app.')
    parser.add_argument('url',
                        help='An url of example voting app \'vote\' app.')
    parser.add_argument('requests_windows', type=int,
                        help='Number of requests windows. In each window the '
                             'number of request which are going to be send '
                             'is equal to 2^n, where n is the number of '
                             'window decreased by one, eg. in the second '
                             'window 2^1 requests are going to be send every '
                             'second, in the 5th window 2^4 requests are '
                             'going to be send.')
    parser.add_argument('window_length', type=int,
                        help='This value determine how long requests window '
                             'is (in seconds). Every second bunch of request '
                             'are going to be send.')

    return parser


if __name__ == "__main__":
    parser = get_argparser()
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker_with_count(args.requests_windows,
                                                  args.window_length,
                                                  make_vote_requests,
                                                  args.url))
    finally:
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        loop.stop()
        loop.close()
