import requests

from typing import Dict
from requests.exceptions import HTTPError

# TODO refactor to be async?
# a basic requests wrapper for post and get request
# new instance can be created - someApi = Request(<url>, <headers>)
# <headers> - additional headers e.g. 'x-api-key: token' and etc
# <url> - hostname with api suffix e.g. 'http://api.com/v1'
class Request:
    def __init__(self, url, headers: Dict={}):
        self.url = url
        self.headers = {
            'content-type': 'application/json',
            **headers,
        }

    def __handleResponse(self, res: requests.Response) -> Dict:
        try:
            res.raise_for_status()
        except HTTPError as http_err:
            return http_err
        except BaseException as err:
            raise Exception(err)
        return res.json()

    def get(self, endpoint: str) -> Dict:
        return self.__handleResponse(requests.get(
            self.url + endpoint,
            headers=self.headers,
        ))
        
    def post(self, endpoint: str, data: Dict) -> Dict:
        return self.__handleResponse(requests.post(
            self.url + endpoint,
            headers=self.headers,
            payload=data,
        ))
