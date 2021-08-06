"""
encapsulate the interactions with the Wild Apricot API.
based on the sample file WaApi.py, but modified to eliminate non-used cruft
(because as Kent Beck says "YAGNI") and to use the python requests package.

written by Leon Webster
version 1.0 12/20/2018

"""

import base64
import logging
import requests
from dotenv import dotenv_values

class WaAPIClient:
    """
    encapsulate the interaction with Wild Apricot
    """

    auth_endpoint = "https://oauth.wildapricot.org/auth/token"
    api_endpoint = "https://api.wildapricot.org"
    _token = None
    _version = "v2.1"
    logger = None

    def __init__(self, CONFIG):
        self._clientId = dotenv_values()['WA_CLIENT_ID']
        self._client_secret = dotenv_values()['WA_CLIENT_SECRET']
        self._APIKey = dotenv_values()['WA_API_KEY']
        self._client_account = dotenv_values()['WA_CLIENT_ACCOUNT']
        self._request_parms = {}
        if CONFIG.parms['filter']:
            self._request_parms["$filter"] = CONFIG.parms['filter']
        if CONFIG.parms['async']:
            self._request_parms['$async'] = 'True'
        else:
            self._request_parms['$async'] = 'False'
        if CONFIG.parms['top'] > 0:
            self._requests_parms['$top'] = CONFIG.parms['top']
        if CONFIG.parms['select']:
            self._request_parms['$select'] = CONFIG.parms['select']
        CONFIG.logger.debug('Params = %s', str(self._request_parms))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(CONFIG.logLevel)
        # set the log level for the requests module too
        logging.getLogger("requests").setLevel(CONFIG.logLevel)
        logging.getLogger("urllib3").setLevel(CONFIG.logLevel)

    def authenticateWithAPIKey(self, scope=None):
        """
        get the security token using oAuth 2.0
        """
        scope = "auto" if scope is None else scope
        data = {"grant_type": "client_credentials", "scope": scope}
        encodedKey = base64.standard_b64encode(
            ("APIKEY:" + self._APIKey).encode()
        ).decode()
        authString = "Basic " + encodedKey
        # print(authString)
        headers = {
            "ContentType": "application/x-www-form-urlencoded",
            "Authorization": authString,
        }
        authResponse = requests.post(url=self.auth_endpoint, headers=headers, data=data)
        self._token = authResponse.json()["access_token"]
        # print('token = ' + self._token)

    def getContacts(self):
        """
        return a list of contacts using the parms passed by the caller.
        call authenticateWithAPIKEY() first to get a new security token
        """
        self.authenticateWithAPIKey()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + self._token,
        }
        url = (
            self.api_endpoint
            + "/"
            + self._version
            + "/accounts/"
            + self._client_account
            + "/Contacts/"
        )
        response = requests.get(url, params=self._request_parms, headers=headers)
        self.logger.info(
            "response from Wild Apricot API was " + str(response.status_code)
        )
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(response.text)
        if response.status_code == 200:
            return response.json()["Contacts"]
        print("url = ", response.url)
        raise Exception("Call to WA API returned status code", response.status_code)
