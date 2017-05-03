import urllib.parse

import requests

from .errors import ServerNotResponseError, RenderHtmlError


class SplashClient(object):
    """
    SplashClient
    """

    PING_URL = '_ping'
    RENDER_HTML_URL = 'render.html'

    def __init__(self, splash_server_url):

        self._server_url = splash_server_url
        self._ping_url = urllib.parse.urljoin(self._server_url, self.PING_URL)
        self._render_html_url = urllib.parse.urljoin(self._server_url,
                                                     self.RENDER_HTML_URL)
        self._ping()

    def _ping(self):
        """
        Check if splash server is running.
        """
        try:
            response = requests.get(self._ping_url)
            if response.status_code != 200:
                raise ServerNotResponseError
        except requests.exceptions.RequestException:
            raise ServerNotResponseError

    def _render_html(self, url, timeout, wait):
        params = {
            'url': url,
            'timeout': timeout,
            'wait': wait
        }
        response = requests.get(self._render_html_url, params=params)
        if response.status_code != 200:
            raise RenderHtmlError(response.content)
        return response.content

    def render_html(self, url, timeout=10, wait=1):
        """
        Render given url.
        """
        self._ping()
        return self._render_html(url, timeout, wait)
