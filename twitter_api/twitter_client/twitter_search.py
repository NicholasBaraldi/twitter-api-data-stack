import requests
import json
import logging

logger = logging.getLogger("twitter_search")


class twitter:
    """_summary_"""

    def __init__(self, bearer_token):

        self.bearer_token = bearer_token
        self._api_base_url = f"https://api.twitter.com/2/tweets/search/recent"

        logger.info("Class=twitter, Method=__init__ msg=Instance Created")

    def twitter_search(self, query: str, ntweet: int):
        params = {
            "query": query,
            "max_results": ntweet,
            "tweet.fields": "created_at",
            "expansions": "author_id",
            "user.fields": "description",
        }
        tweets = []
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r = requests.get(self._api_base_url, headers=headers, params=params).json()
        tweets.append(r)

        nreq = 200

        while nreq > 0:
            params["next_token"] = r["meta"]["next_token"]
            r = requests.get(self._api_base_url, headers=headers, params=params).json()
            print(r)
            tweets.append(r)
            nreq -= 1


data = json.load(open("./api_keys.json"))["Bearer Token"]
twitter(data).twitter_search("Lula", 100)
