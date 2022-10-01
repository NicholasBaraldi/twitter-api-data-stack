import pytest

from twitter_api.twitter_client.twitter_search import Twitter

# class TestTwitter:

# @pytest.mark.parametrize(
#     "query, ntweet", "nreq" [("#lula", 100, 2), ("#eleicoes2022", 150, 3)]
# )
# def test_make_req(self, query, ntweet, nreq):

#     tweets = Twitter.make_req()
#     assert len(tweets) == nreq


def test_make_req():
    nreq = 2
    tweets = Twitter().make_req("#lula", 100, nreq)
    assert len(tweets) == nreq
