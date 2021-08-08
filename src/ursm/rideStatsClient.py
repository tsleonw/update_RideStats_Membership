# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 11:37:44 2019

@author: tslcw
"""


import logging
import requests
from dotenv import dotenv_values


class RideStatsAPI:
    """
    encapsulate the interaction with RideStats
    """
    _rideStatsURL = None
    _rideStatsKey = None
    _logger = None

    def __init__(self, CONFIG):
        self._rideStatsKey = dotenv_values()[f'{CONFIG.environment}_RIDESTATS_KEY']
        self._rideStatsURL = dotenv_values()[f'{CONFIG.environment}_RIDESTATS_URL']
        self._logger = logging.getLogger(f'{CONFIG.environment}_URSM.' + __name__)

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
