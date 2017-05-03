import unittest

from errors import NoVotesHtmlError
from scrapper import Scrapper


NO_VOTES_HTML = """
<!DOCTYPE html><html><head>
    <meta charset="utf-8">
    <title>Cats vs Dogs!</title>
    <base href="/index.html">
    <meta name="viewport" content="width=device-width, initial-scale = 1.0">
    <meta name="keywords" content="docker-compose, docker, stack">
    <meta name="author" content="Tutum dev team">
    <link rel="stylesheet" href="/static/stylesheets/style.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
  </head>
  <body>
    <div id="content-container">
      <div id="content-container-center">
        <h3>Cats vs Dogs!</h3>
        <form id="choice" name="form" method="POST" action="/">
          <button id="a" type="submit" name="vote" class="a" value="a">Cats</button>
          <button id="b" type="submit" name="vote" class="b" value="b">Dogs</button>
        </form>
        <div id="tip">
          (Tip: you can change your vote)
        </div>
        <div id="hostname">
          Processed by container ID 15081299fc4d
        </div>
      </div>
    </div>
    <script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.js"></script>



</body></html>
"""


DB_ERROR_HTML = """
<!DOCTYPE html><html ng-app="catsvsdogs" class="ng-scope"><head><style type="text/css">@charset "UTF-8";[ng\:cloak],[ng-cloak],[data-ng-cloak],[x-ng-cloak],.ng-cloak,.x-ng-cloak,.ng-hide:not(.ng-hide-animate){display:none !important;}ng\:form{display:block;}.ng-animate-shim{visibility:hidden;}.ng-anchor{position:absolute;}</style>
    <meta charset="utf-8">
    <title>Cats vs Dogs -- Result</title>
    <base href="/index.html">
    <meta name="viewport" content="width=device-width, initial-scale = 1.0">
    <meta name="keywords" content="docker-compose, docker, stack">
    <meta name="author" content="Docker">
    <link rel="stylesheet" href="/stylesheets/style.css">
  </head>
  <body ng-controller="statsCtrl" class="ng-scope" style="opacity: 1;">
     <div id="background-stats">
       <div id="background-stats-1">
       </div><!--
      --><div id="background-stats-2">
      </div>
    </div>
    <div id="content-container">
      <div id="content-container-center">
        <div id="choice">
          <div class="choice cats">
            <div class="label">Cats</div>
            <div class="stat ng-binding">50.0%</div>
          </div>
          <div class="divider"></div>
          <div class="choice dogs">
            <div class="label">Dogs</div>
            <div class="stat ng-binding">50.0%</div>
          </div>
        </div>
      </div>
    </div>
    <div id="result">
      <!-- ngIf: total == 0 -->
      <!-- ngIf: total == 1 -->
      <!-- ngIf: total >= 2 -->
    </div>
    <script src="socket.io.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.5/angular.min.js"></script>
    <script src="app.js"></script>


</body></html>
"""


ZERO_VOTES_HTML = """
<!DOCTYPE html><html ng-app="catsvsdogs" class="ng-scope"><head><style type="text/css">@charset "UTF-8";[ng\:cloak],[ng-cloak],[data-ng-cloak],[x-ng-cloak],.ng-cloak,.x-ng-cloak,.ng-hide:not(.ng-hide-animate){display:none !important;}ng\:form{display:block;}.ng-animate-shim{visibility:hidden;}.ng-anchor{position:absolute;}</style>
    <meta charset="utf-8">
    <title>Cats vs Dogs -- Result</title>
    <base href="/index.html">
    <meta name="viewport" content="width=device-width, initial-scale = 1.0">
    <meta name="keywords" content="docker-compose, docker, stack">
    <meta name="author" content="Docker">
    <link rel="stylesheet" href="/stylesheets/style.css">
  </head>
  <body ng-controller="statsCtrl" class="ng-scope" style="opacity: 1;">
     <div id="background-stats">
       <div id="background-stats-1" style="width: 50%;">
       </div><!--
      --><div id="background-stats-2" style="width: 50%;">
      </div>
    </div>
    <div id="content-container">
      <div id="content-container-center">
        <div id="choice">
          <div class="choice cats">
            <div class="label">Cats</div>
            <div class="stat ng-binding">50.0%</div>
          </div>
          <div class="divider"></div>
          <div class="choice dogs">
            <div class="label">Dogs</div>
            <div class="stat ng-binding">50.0%</div>
          </div>
        </div>
      </div>
    </div>
    <div id="result">
      <!-- ngIf: total == 0 --><span ng-if="total == 0" class="ng-scope">No votes yet</span><!-- end ngIf: total == 0 -->
      <!-- ngIf: total == 1 -->
      <!-- ngIf: total >= 2 -->
    </div>
    <script src="socket.io.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.5/angular.min.js"></script>
    <script src="app.js"></script>


</body></html>
"""


ONE_VOTE_HTML = """
<!DOCTYPE html><html ng-app="catsvsdogs" class="ng-scope"><head><style type="text/css">@charset "UTF-8";[ng\:cloak],[ng-cloak],[data-ng-cloak],[x-ng-cloak],.ng-cloak,.x-ng-cloak,.ng-hide:not(.ng-hide-animate){display:none !important;}ng\:form{display:block;}.ng-animate-shim{visibility:hidden;}.ng-anchor{position:absolute;}</style>
    <meta charset="utf-8">
    <title>Cats vs Dogs -- Result</title>
    <base href="/index.html">
    <meta name="viewport" content="width=device-width, initial-scale = 1.0">
    <meta name="keywords" content="docker-compose, docker, stack">
    <meta name="author" content="Docker">
    <link rel="stylesheet" href="/stylesheets/style.css">
  </head>
  <body ng-controller="statsCtrl" class="ng-scope" style="opacity: 1;">
     <div id="background-stats">
       <div id="background-stats-1" style="width: 100%;">
       </div><!--
      --><div id="background-stats-2" style="width: 0%;">
      </div>
    </div>
    <div id="content-container">
      <div id="content-container-center">
        <div id="choice">
          <div class="choice cats">
            <div class="label">Cats</div>
            <div class="stat ng-binding">100.0%</div>
          </div>
          <div class="divider"></div>
          <div class="choice dogs">
            <div class="label">Dogs</div>
            <div class="stat ng-binding">0.0%</div>
          </div>
        </div>
      </div>
    </div>
    <div id="result">
      <!-- ngIf: total == 0 -->
      <!-- ngIf: total == 1 --><span ng-if="total == 1" class="ng-binding ng-scope">1 vote</span><!-- end ngIf: total == 1 -->
      <!-- ngIf: total >= 2 -->
    </div>
    <script src="socket.io.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.5/angular.min.js"></script>
    <script src="app.js"></script>


</body></html>
"""


LOT_VOTES_HTML = """
<!DOCTYPE html><html ng-app="catsvsdogs" class="ng-scope"><head><style type="text/css">@charset "UTF-8";[ng\:cloak],[ng-cloak],[data-ng-cloak],[x-ng-cloak],.ng-cloak,.x-ng-cloak,.ng-hide:not(.ng-hide-animate){display:none !important;}ng\:form{display:block;}.ng-animate-shim{visibility:hidden;}.ng-anchor{position:absolute;}</style>
    <meta charset="utf-8">
    <title>Cats vs Dogs -- Result</title>
    <base href="/index.html">
    <meta name="viewport" content="width=device-width, initial-scale = 1.0">
    <meta name="keywords" content="docker-compose, docker, stack">
    <meta name="author" content="Docker">
    <link rel="stylesheet" href="/stylesheets/style.css">
  </head>
  <body ng-controller="statsCtrl" class="ng-scope" style="opacity: 1;">
     <div id="background-stats">
       <div id="background-stats-1" style="width: 50%;">
       </div><!--
      --><div id="background-stats-2" style="width: 50%;">
      </div>
    </div>
    <div id="content-container">
      <div id="content-container-center">
        <div id="choice">
          <div class="choice cats">
            <div class="label">Cats</div>
            <div class="stat ng-binding">50.0%</div>
          </div>
          <div class="divider"></div>
          <div class="choice dogs">
            <div class="label">Dogs</div>
            <div class="stat ng-binding">50.0%</div>
          </div>
        </div>
      </div>
    </div>
    <div id="result">
      <!-- ngIf: total == 0 -->
      <!-- ngIf: total == 1 -->
      <!-- ngIf: total >= 2 --><span ng-if="total &gt;= 2" class="ng-binding ng-scope">53773 votes</span><!-- end ngIf: total >= 2 -->
    </div>
    <script src="socket.io.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.5/angular.min.js"></script>
    <script src="app.js"></script>


</body></html>
"""


class ScrapperTestCase(unittest.TestCase):

    def test_no_html(self):
        self.assertRaises(NoVotesHtmlError, Scrapper.get_votes, "Some string\b")

    def test_no_votes(self):
        self.assertRaises(NoVotesHtmlError, Scrapper.get_votes, NO_VOTES_HTML)

    def test_empty_votes(self):
        self.assertEqual(0, Scrapper.get_votes(ZERO_VOTES_HTML))

    def test_one_vote(self):
        self.assertEqual(1, Scrapper.get_votes(ONE_VOTE_HTML))

    def test_some_votes(self):
        self.assertEqual(53773, Scrapper.get_votes(LOT_VOTES_HTML))


if __name__ == "__main__":
    unittest.main()
