
class ScrapperError(Exception):
    """
    Scrapper base exception
    """

class NoVotesHtmlError(ScrapperError):
    """
    Raises when HTML with no votes XPATH is provided into 'get_votes' function
    """
