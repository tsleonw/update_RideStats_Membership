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
        # set the log level for the requests module too
        logging.getLogger('requests').setLevel(logLevel)
        logging.getLogger('urllib3').setLevel(logLevel)

    def postToRideStats(self, payload):
        """
        post the payload to rideStats
        """
        headers = {'authorization': self._rideStatsKey}
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('RideStats URL = %s', self._rideStatsURL)
            self._logger.debug('RideStats payload = %s', payload)
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
            self._logger.info('payload = %s', payload)
            self._logger.info('url = %s', response.url)
            self._logger.critical('Call to RideStats API return status code %d', response.status_code)
            msg = "Call to RideStats API returned status code " + str(response.status_code)
            raise Exception(msg)
