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
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import URSMConfig
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


class MemberError:
    """
    container for errorList and warnings about a given member.  This will be added
    to the errorList array and needs to print in a nice fashion
    """
    firstName = None
    lastName = None
    exceptions = None
    messages = None
    memberRecord = None

    def __init__(self,
                 memberRecord,
                 msg,
                 exception=None):
        self.firstName = memberRecord['FirstName']
        self.lastName = memberRecord['LastName']
        self.memberRecord = memberRecord
        self.messages = [msg]
        if exception:
            self.exceptions = [exception]

    def addErrorRecord(self, msg, exception=None):
        """
        add an error to an existing error list
        """
        self.messages.append(msg)
        if exception:
            if self.exceptions:
                self.exceptions.append(exception)
            else:
                self.exceptions = [exception]


class Member:
    """
    Member represents a member of the club in Wild Apricot
    """

    def __init__(self, aDict):
        """
        construct a member object from a dictionary.
        """
        self._setDefaultValues()
        try:
            try:
                self._firstName = aDict['FirstName']
            except KeyError as ex:
                msg = "Error populating member first name" + ex.__repr__()
                self.postError(msg, aDict, ex)
            try:
                self._lastName = aDict['LastName']
            except KeyError as ex:
                msg = "Error populating member last name" + ex.__repr__()
                self.postError(msg, aDict, ex)
            self._email = aDict['Email']
            self._membershipType = aDict['MembershipLevel']['Name']
            self._status = aDict['Status']
            self._profileLastUpdated = datetime.now().date()
            for field in aDict['FieldValues']:
                if field['FieldName'] == "Member since":
                    if self._status == 'PendingNew':
                        self._memberSince = self._profileLastUpdated
                        msg = self._firstName + ' ' + self._lastName + ' is a pending new' + \
                              ' member.  using profile last updated date as memberSince.'
                        self.postError(msg, aDict, None)
                    else:
                        if field['Value']:
                            self._memberSince = datetime.fromisoformat((field['Value'])[:19]).date()
                        else:
                            msg = self._firstName + " " + self._lastName + \
                                  " does not have a valid member since date."
                            self.postError(msg, aDict, None)
                elif field['FieldName'] == "Gender":
                    if field['Value'] is not None:
                        self._gender = field['Value']['Label']
                    else:
                        self._gender = 'Neutral'
                elif field['FieldName'] == "Renewal due":
                    if self._status == 'PendingNew':
                        self._renewalDue = self._memberSince + timedelta(days=30)
                        msg = self._firstName + ' ' + self._lastName + ' is a pending new' \
                              + ' member.  Renewal due 30 days after profile last updated.'
                        self.postError(msg, aDict, None)
                    else:
                        if field['Value']:
                            self._renewalDue = datetime.fromisoformat(field['Value']).date()
                        else:
                            msg = self._firstName + " " + self._lastName + \
                                  " does not have a valid renewal due date."
                            self.postError(msg, aDict, None)
                elif field['FieldName'] == "Mobile Phone":
                    self._mobilePhone = self.phoneNumberFromString(field['Value'])
                elif field['FieldName'] == "Telephone":
                    self._telephone = self.phoneNumberFromString(field['Value'])
                elif field['FieldName'] == 'User ID':
                    self._memberID = field['Value']
                elif field['FieldName'] == 'Alias':
                    self._alias = field['Value']
                elif field['FieldName'] == 'City':
                    self._city = field['Value']
                elif field['FieldName'] == 'State':
                    self._state = field['Value']
                elif field['FieldName'] == 'Postal Code':
                    self._zipCode = field['Value']
                elif field['FieldName'] == 'Emergency Contact':
                    self._emergencyContact = field['Value']
                elif field['FieldName'] == 'Emergency Contact Phone':
                    self._emergencyContactPhone = self.phoneNumberFromString(field['Value'])
                    """if (self.emergencyContactPhone == '' or
                            self.emergencyContactPhone is None):
                        msg = self.firstName + ' ' + self.lastName + \
                              ' does not have an emergency contact phone number.'
                        self.postError(msg, aDict, None)"""
                elif field['FieldName'] == 'Birthday':
                    self._birthDate = field['Value']
                elif field['FieldName'] == "Group participation":
                    if field["Value"]:
                        for group in field["Value"]:
                            if group["Label"] == "Ride Leader":
                                self._isRideLeader = True
                elif field['FieldName'] == 'Creation Date':
                    self._creationDate = datetime.fromisoformat(field['Value'][:19]).date()
                    print(self._creationDate)
        except Exception as ex:
            msg = "Other error in member.__init__() " + ex.__repr__()
            self.postError(msg, aDict, ex)

    def _setDefaultValues(self):
        """
        set default values for instance variables.  Since the information in Wild Apricot may be missing fields, we
        need to make sure that the attributes exist with default values so serialization works without checking for
        the existence of each attribute.
        """
        self._memberID = None
        self._firstName = None
        self._lastName = None
        self._birthDate = None
        self._alias = None
        self._email = None
        self._status = None
        self._mobilePhone = None
        self._telephone = None
        self._city = None
        self._state = None
        self._zipCode = None
        self._membershipType = None
        self._isRideLeader = False
        self._memberSince = None
        self._creationDate = None
        self._renewalDue = None
        self._profileLastUpdated = None
        self._gender = None
        self._isValid = True
        self._memberError = None
        self._emergencyContact = None
        self._emergencyContactPhone = None

    def postError(self, msg, aDict, exception):
        """
        add an error to the members error list.  If there is no error list,
        create one.
        """
        if self._memberError is None:
            self._memberError = MemberError(aDict,
                                           msg,
                                           exception)
        else:
            self._memberError.addErrorRecord(msg, exception)
        CONFIG.logger.error(msg)

    def phoneNumberFromString(self, aString):
        """
        given a string, return the first 10 digits ignoring all non-numeric
        characters
        """
        digits = list(filter(lambda x: x.isdigit(), aString))
        phoneNumber = ''.join(digits)
        if len(phoneNumber) > 9:
            phoneNumber = phoneNumber[:10]
        return phoneNumber

    def isValid(self):
        """make sure that all required attributes of a member are present
        """
        if (self._memberID is None or
                self._firstName is None or
                self._lastName is None or
                self._email is None or
                self._memberSince is None or
                self._renewalDue is None or
                self._renewalDue < self._memberSince):
            CONFIG.logger.error(msg="invalid member record: "
                                    + str(self))
            return False
        else:
            return True

    def toDict(self):
        """
        render a json representation of a member
        """
        aDict = {}
        aDict["clubMemberId"] = self._memberID
        aDict["firstName"] = self._firstName
        aDict["lastName"] = self._lastName
        aDict['alias'] = self._alias
        aDict['city'] = self._city
        aDict['emailAddress'] = self._email
        aDict["gender"] = self._gender
        if self._memberSince:
            aDict["membershipStart"] = self._memberSince.isoformat()
        else:
            aDict['membershipStart'] = None
        if self._renewalDue:
            aDict["membershipEnd"] = self._renewalDue.isoformat()
        else:
            aDict['membershipEnd'] = None
        aDict['membershipType'] = self._membershipType
        aDict['phone1'] = self._mobilePhone
        aDict['phone2'] = self._telephone
        if self._isRideLeader:
            aDict["rideLeader"] = True
        else:
            aDict["rideLeader"] = False
        aDict['state'] = self._state
        aDict['emergencyContactName'] = self._emergencyContact
        aDict['emergencyContactPhone'] = self._emergencyContactPhone
        if self._birthDate:
            aDict['birthDate'] = self._birthDate
        else:
            aDict['birthDate'] = ''
        if self._zipCode:
            aDict['zipCode'] = self._zipCode
        else:
            aDict['zipCode'] = ''
        aDict['userLastModified'] = self._profileLastUpdated.isoformat()
        return aDict

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        aString = "Membership information for " + self._firstName + " " + \
                  self._lastName + " " + "\tMember ID = " \
                  + str(self._memberID) + "\n"
        if self._memberError is None:
            return aString
        aString += "/tMember Record has errors"
        for msg in self._memberError.messages:
            aString += "\t\t" + msg
        return aString



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
        member = Member(each)
        if member._memberError:
            errorList.append(member._memberError)
        if member.isValid():
            memberList.append(member.toDict())
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
    print(ex)

finally:
    logging.shutdown()
