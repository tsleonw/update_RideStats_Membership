#!/usr/bin/env python3
"""
This module sends a request to Wild Apricot for a list of club members using
the Wild Apricot API.  Wild Apricot returns a JSON list of members.  The module
then validates each member.  A list of valid members is sent to RideStats,
and an email is produced which reports the status of the run and lists any
errorList.
"""

import logging
from logging.handlers import TimedRotatingFileHandler
import json
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback

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
        if len(sys.argv) < 2 or (sys.argv[1] != 'PROD' and sys.argv[1] != 'QA'):
            print('No environment specified. \n')
            print('usage:  updateRideStatsMembership.py PROD|QA')
            sys.exit(1)
        else:
            self.environment = sys.argv[1]
            self.parms = URSMConfig.CONFIG[self.environment]

    def initLogger(self):
        """
        initialize the logging using a timed rotating file handler
        """
        try:
            logFormat = logging.Formatter('%(asctime)s | %(levelname)s \
                                          |%(module)s:%(lineno)d | %(message)s')
            self.logLevel = getattr(logging, self.parms['logLevel'].upper())
            handler = TimedRotatingFileHandler(self.parms['logFile'],
                                               when='midnight',
                                               backupCount=28)
            handler.setFormatter(logFormat)
            self.logger = logging.getLogger()
            self.logger.setLevel(self.logLevel)
            self.logger.addHandler(handler)
        except Exception as ex:
            print("could not initialize logging:  ", ex)
            sys.exit(1)
        self.logger.info(msg='loaded parms for the ' + self.environment + ' environment')


def getMembers():
    """
    make a call to Wild Apricot and return a list of members
    """
    params = {}
    if CONFIG.parms['filter']:
        params["$filter"] = CONFIG.parms['filter']
    if CONFIG.parms['async']:
        params['$async'] = 'True'
    else:
        params['$async'] = 'False'
    if CONFIG.parms['top'] > 0:
        params['$top'] = CONFIG.parms['top']
    if CONFIG.parms['select']:
        params['$select'] = CONFIG.parms['select']
    CONFIG.logger.debug('Params = %s', str(params))
    return WA_API.getContacts(params, CONFIG.parms['clientAccount'])


def emailResults():
    """
    send an email detailing the work
    """
    server = None
    endTime = datetime.utcnow()
    numMembers = len(memberList)
    numerrorList = len(errorList)

    msgText = "RideStatsMemberUpdate started at " + startTime.isoformat() + "\n"
    msgText += "RideStatsMemberUpdate completed at " + endTime.isoformat() + "\n"
    msgText += "duration was " + str(endTime - startTime) + "\n"
    msgText += 'The RideStats URL was ' + CONFIG.parms['RideStatsURL'] + '\n'
    msgText += "There were " + str(numMembers) + " members processed.\n"
    msgText += "There were " + str(numerrorList) + " members with errors\n"
    if errorList:
        msgText += "The following records had problems:\n"
        for memberError in errorList:
            msgText += '\t' + memberError.firstName + ' ' + memberError.lastName + "\n"
            for errorMessage in memberError.messages:
                msgText += "\t\t" + str(errorMessage) + "\n"
    msgText += "the response from RideStats was:\n"
    msgText += rideStatsResponse
    msg = MIMEMultipart()
    msg['From'] = CONFIG.parms['smtpFromAddress']
    msg['To'] = CONFIG.parms['smtpToAddress']
    msg['Subject'] = 'Update RideStats Job Results'
    msg.attach(MIMEText(msgText, 'plain'))

    try:
        server = smtplib.SMTP(CONFIG.parms['smtpServer'],
                              CONFIG.parms['smtpPort'])
        server.starttls()
        server.login(CONFIG.parms['smtpFromAddress'],
                     CONFIG.parms['smtpPassword'])
        server.sendmail(CONFIG.parms['smtpFromAddress'],
                        CONFIG.parms['smtpToAddress'],
                        msg.as_string())
    except Exception as ex:
        CONFIG.logger.exception(ex)
    finally:
        if server:
            server.quit()


try:
    startTime = datetime.utcnow()
    CONFIG = Config()
    WA_API = WaAPIClient(CONFIG.parms['clientID'],
                         CONFIG.parms['clientSecret'],
                         CONFIG.parms['apiKey'],
                         CONFIG.logLevel)
    waResponse = getMembers()
    memberList = []
    errorList = []
    payload = {"clubId": "HBC"}
    for each in waResponse:
        member = HBCMember(each)
        if member.memberError:
            errorList.append(member.memberError)
        if member.isValid():
            memberList.append(member.toDict())
        else:
            CONFIG.logger.error(msg="invalid member record: "
                                    + member.str())
    payload["memberships"] = memberList
    if CONFIG.parms['PostToRideStats']:
        RIDESTATS_API = RideStatsAPI(CONFIG.parms['RideStatsURL'],
                                     CONFIG.parms['RideStatsKey'],
                                     logLevel=CONFIG.logLevel)
        rideStatsResponse = RIDESTATS_API.postToRideStats(payload)
    else:
        with open('rideStatsPayload.json', 'w') as outfile:
            json.dump(payload, outfile)
        CONFIG.logger.info("rideStatsURL = 'localhost'; payload == \n %s",
                           payload)
        rideStatsResponse = "RideStats URL was localHost.  see log for details"
    if CONFIG.logger.isEnabledFor(logging.DEBUG):
        CONFIG.logger.debug("valid members = %s", memberList)
        CONFIG.logger.debug("errorList = %s", errorList)
    if CONFIG.logger.isEnabledFor(logging.INFO):
        CONFIG.logger.info('%s members were successfully validated', str(len(memberList)))
        CONFIG.logger.info("response from RideStats was %s", rideStatsResponse)
        CONFIG.logger.info('%s non-fatal errors were found', str(len(errorList)))
    emailResults()

except Exception as ex:
    traceback.print_exc()


finally:
    logging.shutdown()
