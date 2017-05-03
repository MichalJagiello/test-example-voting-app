import random

import requests


class ApiCall(object):

    def __init__(self, votes_page_url):
        self._votes_page_url = votes_page_url

    def get_voter_id(self):
        response = requests.get(self._votes_page_url)
        return response.cookies.get('voter_id')

    def post_vote(self, voter_id):
        cookies = {'voter_id': voter_id}
        requests.post(self._votes_page_url, cookies=cookies,
                      data={'vote': 'a' if random.random() < 0.5 else 'b'})

    def make_vote(self):
        voter_id = self.get_voter_id()
        self.post_vote(voter_id)
