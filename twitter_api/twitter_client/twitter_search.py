from ctypes import Union
from typing import Tuple
import requests
import json
import logging

logger = logging.getLogger("twitter_search")


class Twitter:
    """_summary_"""

    def __init__(self, bearer_token) -> None:
        """Create request session and recieve authorization params.

        Args:
            bearer_token (str): Authentication token.
        """
        self.bearer_token = bearer_token
        self._api_base_url = f"https://api.twitter.com/2/tweets/search/recent"

        logger.info("Class=twitter, Method=__init__ msg=Instance Created")

    def _twitter_search(self, query: str, ntweet: int, nreq: int) -> Tuple[list, list]:
        """Call the API and store requests in a Tuple.

        Args:
            query (str): Query param.
            ntweet (int): Number of tweets per request.

        Returns:
            Tuple[list, list]: Tuple of tweets and users.
        """

        params = {
            "query": query,
            "max_results": ntweet,
            "tweet.fields": "created_at",
            "expansions": "author_id",
            "user.fields": "description",
        }
        tweets = []
        users = []
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r = requests.get(self._api_base_url, headers=headers, params=params).json()

        while nreq > 0 and "next_token" in r["meta"]:
            params["next_token"] = r["meta"]["next_token"]
            r = requests.get(self._api_base_url, headers=headers, params=params).json()
            tweets += r["data"]
            users += r["includes"]["users"]
            nreq -= 1
        return tweets, users

    def make_req(self, query: str, ntweet: int, nreq: int) -> Tuple:
        """Call _twitter_search and raises an error if reqs are not done.

        Args:
            query (str): Query param.
            ntweet (int): Number of tweets per request.
            nreq (int): Number of requests.

        Raises:
            Exception: Stops method if tweets_list are empty.

        Returns:
            list: Tuple
        """
        tweets_list, users_list = self._twitter_search(query, ntweet, nreq)
        if tweets_list:
            logger.info("Class=twitter, Method=make_req msg=API returned successfully")
            return tweets_list, users_list
        raise Exception("Class=twitter, Method=make_req msg=API return failed")
