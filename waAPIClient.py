"""
encapsulate the interactions with the Wild Aprict API.
based on the sample file WaApi.py, but modified to eliminate non-used cruft
(because as Kent Beck says "YAGNI") and to use the python requests package.

written by Leon Webster
version 1.0 12/20/2018

"""
import base64
import logging
import requests


class WaAPIClient:
    """
    encapsulate the interaction with Wild Apricot
    """
    auth_endpoint = "https://oauth.wildapricot.org/auth/token"
    api_endpoint = "https://api.wildapricot.org"
    _token = None
    _clientId = None
    _client_secret = None
    _version = "v2.1"
    _APIKey = None
    logger = None

    def __init__(self, clientId, clientSecret, APIKey, logLevel=logging.DEBUG):
        if (clientId is None or
                clientSecret is None or
                APIKey is None):
            raise Exception("cannot create WaApiClient with clientID = ",
                            clientId, "and clientSecret = ", clientSecret)
        self._clientId = clientId
        self._clientSecret = clientSecret
        self._APIKey = APIKey
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logLevel)
        # set the log level for the requests module too
        logging.getLogger('requests').setLevel(logLevel)
        logging.getLogger('urllib3').setLevel(logLevel)

    def authenticateWithAPIKey(self, scope=None):
        """
        get the security token using oAuth 2.0
        """
        scope = "auto" if scope is None else scope
        data = {
            "grant_type": "client_credentials",
            "scope": scope
        }
        encodedKey = base64.standard_b64encode(('APIKEY:'
                                                + self._APIKey).encode()).decode()
        authString = 'Basic ' + encodedKey
        # print(authString)
        headers = {'ContentType': 'application/x-www-form-urlencoded',
                   'Authorization': authString}
        authResponse = requests.post(url=self.auth_endpoint,
                                     headers=headers, data=data)
        self._token = authResponse.json()["access_token"]
        # print('token = ' + self._token)

    def getContacts(self, params, accountNumber):
        """
        return a list of contacts using the parms passed by the caller.
        call authenticateWithAPIKEY() first to get a new security token
        """
        self.authenticateWithAPIKey()
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json",
                   "Authorization": "Bearer " + self._token}
        url = self.api_endpoint + "/" + self._version + "/accounts/" + accountNumber + "/Contacts/"
        response = requests.get(url, params=params, headers=headers)
        self.logger.info("response from Wild Apricot API was " + str(response.status_code))
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(response.text)
        if response.status_code == 200:
            return response.json()['Contacts']
        print('url = ', response.url)
        raise Exception("Call to WA API returned status code",
                        response.status_code)
