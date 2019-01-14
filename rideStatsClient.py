# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 11:37:44 2019

@author: tslcw
"""

import logging
import requests

class RideStatsAPI:
    """
    encapsulate the interaction with RideStats
    """
    _rideStatsURL = None
    _rideStatsKey = None
    _logger = None

    def __init__(self, rideStatsURL, rideStatsKey, logLevel=logging.DEBUG):
        self._rideStatsURL = rideStatsURL
        self._rideStatsKey = rideStatsKey
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logLevel)
        #set the log level for the requests module too
        logging.getLogger('requests').setLevel(logLevel)
        logging.getLogger('urllib3').setLevel(logLevel)

    def postToRideStats(self, payload):
        """
        post the json payload to rideStats
        """
        if self._rideStatsURL.upper() == "LOCALHOST":
            self._logger.info("rideStatsURL = 'localhost'; payload == \n %s",
                              (payload))
            return "RideStats URL was localHost.  see log for details"
        headers = {'authorization':self._rideStatsKey}
        response = requests.post(headers=headers,
                                 url=self._rideStatsURL,
                                 json=payload)
        self._logger.info("RideStats Webs Service returns status code %s",
                          response.status_code)
        self._logger.info("RideStats response = %s", response.text)
        if (response.status_code == 200 or
                response.status_code == 202):
            return response.text
        else:
            self._logger.info('url = %s', response.url)
            msg = "Call to RideStats API returned status code " + response.status_code
            raise Exception(msg)
