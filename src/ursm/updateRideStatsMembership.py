#!/usr/bin/env python3
"""
This module sends a request to Wild Apricot for a list of club members using
the Wild Apricot API.  Wild Apricot returns a JSON list of members.  The module
then validates each member.  A list of valid members is sent to RideStats,
and an email is produced which reports the status of the run and lists any
errors.
"""

import argparse
import json
import logging
import logging.config
import smtplib
import sys
import time
import traceback

from datetime import datetime
from dotenv import dotenv_values
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging.handlers import TimedRotatingFileHandler


import URSMConfig

from hbc_Member import HBCMember
from rideStatsClient import RideStatsAPI
from waAPIClient import WaAPIClient


class Config:
    """
    Class acts as a value holder for global parms.
    Maybe this is not the most pythonic way to accomplish this,
    but I like that it encapsulates the transfer of the data
    from a parms file to the variables.
    """

    parms = {}
    logger = None
    logLevel = None
    environment = None

    def __init__(self):
        """
        load configuration and initialize the logger
        """
        self.loadParms()
        self.initLogger()

    def loadParms(self):
        """
        load the appropriate parms depending upon the environment that was
        passed in
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'env',
            help='specify the environment for updating RideStats. Either "QA" or "PROD"',
            choices=["PROD", "QA"],
        )
        self.environment = parser.parse_args().env
        self.parms = URSMConfig.CONFIG[self.environment]

    def initLogger(self):
        """
        initialize  logging using the dictionary in the config file
        """
        try:
            logging.config.dictConfig(URSMConfig.LOGGING)
            self.logger = logging.getLogger(f'{self.environment}_URSM')
            self.logger.debug("logging configured")
        except Exception as ex:
            print("could not initialize logging:  ", ex)
            sys.exit(1)
        self.logger.info(msg=f'loaded parms for the {self.environment} environment')


def emailResults(CONFIG, startTime, start, rideStatsResponse, errorList):
    """
    send an email detailing the work
    """
    server = None
    endTime = datetime.utcnow()
    end = time.perf_counter()
    numMembers = len(memberList)
    numerrorList = len(errorList)
    url = dotenv_values()[f'{CONFIG.environment}_RIDESTATS_URL']
    from_address = dotenv_values()[f'{CONFIG.environment}_SMTP_FROM_ADDRESS']
    to_address = dotenv_values()['SMTP_TO_ADDRESS']
    password = dotenv_values()[f'{CONFIG.environment}_SMTP_PASSWORD']

    msgText = f'RideStatsMemberUpdate started at {startTime.isoformat()}\n'
    msgText += f'RideStatsMemberUpdate completed at {endTime.isoformat()}\n'
    msgText += f'duration was {end-start}\n'
    msgText += f'The RideStats URL was {url}\n'
    msgText += f'There were {numMembers} members processed.\n'
    msgText += f'There were {numerrorList} members with errors\n'
    if errorList:
        msgText += "The following records had problems:\n"
        for memberError in errorList:
            for errorMessage in memberError.messages:
                msgText += f'{errorMessage}\n'
    msgText += "the response from RideStats was:\n"
    msgText += rideStatsResponse
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = 'Update RideStats Job Results'
    msg.attach(MIMEText(msgText, 'plain'))

    try:
        server = smtplib.SMTP(CONFIG.parms['smtpServer'],
                              CONFIG.parms['smtpPort'])
        server.starttls()
        server.login(from_address,
                     password)
        server.sendmail(from_address,
                        to_address,
                        msg.as_string())
    except Exception as ex:
        CONFIG.logger.exception(ex)
    finally:
        if server:
            server.quit()


def main():
    startTime = datetime.utcnow()
    start = time.perf_counter()
    CONFIG = Config()
    # start getting Wild Apricot response
    WA_API = WaAPIClient(CONFIG)
    waResponse = WA_API.getContacts()
    # End getting Wild Apricot Response
    # Start Constructing RideStats POST
    payload, errorList = construct_RideStats_payload(CONFIG, waResponse)
    # End Constructing RideStats POST
    # Post to RideStats or write to file
    if CONFIG.parms['PostToRideStats']:
        RIDESTATS_API = RideStatsAPI(CONFIG)
        rideStatsResponse = RIDESTATS_API.postToRideStats(payload)
    else:
        with open('../rideStatsPayload.json', 'w') as outfile:
            json.dump(payload, outfile)
        CONFIG.logger.info("rideStatsURL = 'localhost'; payload == \n %s",
                           payload)
        rideStatsResponse = "RideStats URL was localHost.  see log for details"
    # End post to RideStats or File
    # Log results
    if CONFIG.logger.isEnabledFor(logging.DEBUG):
        CONFIG.logger.debug("valid members = %s", memberList)
        CONFIG.logger.debug("errorList = %s", errorList)
    if CONFIG.logger.isEnabledFor(logging.INFO):
        CONFIG.logger.info(f'{str(len(memberList))} members were successfully validated')
        CONFIG.logger.info(f'response from RideStats was {rideStatsResponse}')
        CONFIG.logger.info('%s non-fatal errors were found', str(len(errorList)))
    # Email Results
    emailResults(CONFIG, startTime, start,  rideStatsResponse, errorList)


def construct_RideStats_payload(CONFIG, waResponse):
    global memberList, errorList
    memberList = []
    errorList = []
    CLUB_ID = dotenv_values()['RIDESTATS_CLUB_ID']
    payload = {"clubId": CLUB_ID}
    for each in waResponse:
        member = HBCMember(each)
        if member.memberError:
            errorList.append(member.memberError)
        if member.isValid():
            memberList.append(member.toDict())
        else:
            CONFIG.logger.error(msg = f'invalid member record: {member} ')
    payload["memberships"] = memberList
    return payload, errorList


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        traceback.print_exc(ex)
        sys.exit(1)
    finally:
        logging.shutdown()