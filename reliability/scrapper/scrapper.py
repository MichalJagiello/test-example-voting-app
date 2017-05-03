from lxml import html

from .errors import NoVotesHtmlError


class Scrapper(object):
    """
    Scrapper class
    """

    VOTES_XPATH = "/html/body/div[3]/span/text()"
    NO_VOTES = "No votes yet"
    VOTE_SPLIT_TEXT = " vote"

    @classmethod
    def get_votes(cls, html_string):
        tree = html.fromstring(html_string)
        votes_span = tree.xpath(cls.VOTES_XPATH)
        if not votes_span:
            raise NoVotesHtmlError
        votes_span_text = votes_span[0]
        if votes_span_text == cls.NO_VOTES:
            return 0
        return int(votes_span_text.split(cls.VOTE_SPLIT_TEXT)[0])
