import requests
import json

class twitter:

    def twitter_search(self, query : str):
            data = json.load(open('./api_keys.json'))["Bearer Token"]
            headers = {"Authorization": f"Bearer {data}"}
            url = 'https://api.twitter.com/2/tweets/search/recent?query=' + query
            r = requests.get(url, headers = headers)
            return r.json()

print(twitter().twitter_search('LULA'))