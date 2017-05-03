

class SplashClientError(Exception):
    """
    Base SplashClient error class
    """


class ServerNotResponseError(SplashClientError):
    """
    Exception raised when there is no connection with server
    or server do not return valid response on _ping request.
    """


class RenderHtmlError(SplashClientError):
    """
    Exception raised when rendering html request returns response with
    status code different than 200.
    """
