#!/usr/bin/env python3
"""
This module sends a request to Wild Apricot for a list of club members using
the Wild Apricot API.  Wild Apricot returns a JSON list of members.  The module
then validates each member.  A list of valid members is sent to RideStats,
and an email is produced which reports the status of the run and lists any
errorList.

TODO:
        1) [DONE]get git figured out -- eliminate the unused files in the repository,
           make sure all neeeded files are there.
        2) [DONE]make parms configurable by environment & make environment a paramter
           that is passed in at startup.
        3) complete the error handling for creating a member.  Loook at alternaives
           for error checking, especially key errors.
        4) [Done]modify the email so that it reports which environment it comes from
           and the URL used for ridestats.
        5) construct some mock objects for testing, especially the calls to Wild
           Apricot and RideStats.
        6) [DONE]Rename the parm file.
        7) [DONE]store the production code on the wild apricot website.
        8) [Done]implment logrotate
"""


import logging
import json
import smtplib
import sys
from datetime import datetime

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

    _parmFile = "URSMParms.json"
    parms = {}
    logger = None
    logLevel = None


    def __init__(self):
        """
        try:
            with open(self._parmFile) as readFile:
                self.parms = json.load(readFile)
              #  print("parms = ", self.parms)
        except Exception as ex:
            print("could not load parmFile:", self._parmFile)
            print('Exception: ', ex)
            exit(1)
        """
        self.loadParms()
        self.initLogger()

    def loadParms(self):
        if len(sys.argv) < 2 or (sys.argv[1] != 'PROD' and sys.argv[1] != 'QA'):
            print('No environment specified. \n')
            print('usage:  updateRideStatsMembership.py PROD|DEV')
            sys.exit(1)
        else:
            self.environment = sys.argv[1]
            self.parms = URSMConfig.CONFIG[self.environment]

    def initLogger(self):
        try:
            logFormat = "%(asctime)s - %(levelname)s - %(module)s:%(lineno)d -- %(message)s"
            self.logLevel = getattr(logging, self.parms['logLevel'].upper())
            logging.basicConfig(filename=self.parms['logFile'],
                                level=self.logLevel,
                                format=logFormat)
            self.logger = logging.getLogger(__name__)
        except Exception as ex:
            print("could not initialize logging:  ", ex)
            exit(-1)
        self.logger.info(msg='loaded parms from '+self._parmFile)


class MemberError:
    """
    container for errorList and warnings about a given member.  This will be added
    to the errorList array and needs to print in a nice fashion
    """
    firstName = None
    lastName = None
    exceptions = []
    messages = []
    memberRecord = None

    def __init__(self,
                 memberRecord,
                 msg,
                 exception=None):
        self.firstName = memberRecord['FirstName']
        self.lastName = memberRecord['LastName']
        self.memberRecord = memberRecord
        self.messages.append(msg)
        if exception:
            self.exceptions.append(exception)

    def addErrorRecord(self, msg, exception=None):
        """
        add an error to an existing error list
        """
        self.messages.append(msg)
        if exception:
            self.exceptions.append(exception)


class Member:
    """
    Member represents a member of the club in Wild Apricot
    """
    memberID = None
    firstName = None
    lastName = None
    birthDate = None
    alias = None
    email = None
    mobilePhone = None
    telephone = None
    city = None
    state = None
    zipCode = None
    membershipType = None
    isRideLeader = False
    memberSince = None
    renewalDue = None
    profileLastUpdated = None
    gender = None
    isValid = True
    memberError = None
    emergencyContact = None
    emergencyContactPhone = None

    def __init__(self, aDict):
        """
        construct a member object from a dictionary.
        """
        try:
            try:
                self.firstName = aDict['FirstName']
            except KeyError as ex:
                msg = "Error populating member first name" + ex.__repr__()
                self.postError(msg, aDict, ex)
            try:
                self.lastName = aDict['LastName']
            except KeyError as ex:
                msg = "Error populating member last name" + ex.__repr__()
                self.postError(msg, aDict, ex)
            self.email = aDict['Email']
            self.membershipType = aDict['MembershipLevel']['Name']

            try:
                self.profileLastUpdated = datetime.fromisoformat(
                    (aDict['ProfileLastUpdated'])[:19]).date()
            except KeyError as ex:
                msg = self.firstName +  ' ' + self.lastName + \
                      ' does not have a valid "Profile Last Updated" field in Wild Apricot'
#                msg = "error populating profileLastUpdated " +  ex.__repr__()
                self.postError(msg, aDict, ex)
                self.profileLastUpdated = datetime.now().date()

            for field in aDict['FieldValues']:
                if field['FieldName'] == "Member since":
                    self.memberSince = datetime.fromisoformat((field['Value'])[:19]).date()
                elif field['FieldName'] == "Gender":
                    if field['Value'] is not None:
                        self.gender = field['Value']['Label']
                    else:
                        self.gender = 'Neutral'
                elif field['FieldName'] == "Renewal due":
                    self.renewalDue = datetime.fromisoformat(field['Value']).date()
                elif field['FieldName'] == "Mobile Phone":
                    self.mobilePhone = field['Value']
                elif field['FieldName'] == "Telephone":
                    self.telephone = field['Value']
                elif field['FieldName'] == 'User ID':
                    self.memberID = field['Value']
                elif field['FieldName'] == 'Alias':
                    self.alias = field['Value']
                elif field['FieldName'] == 'City':
                    self.city = field['Value']
                elif field['FieldName'] == 'State':
                    self.state = field['Value']
                elif field['FieldName'] == 'Postal Code':
                    self.zipCode = field['Value']
                elif field['FieldName'] == 'Emergency Contact':
                    self.emergencyContact = field['Value']
                elif field['FieldName'] == 'Emergency Contact Phone':
                    self.emergencyContactPhone = field['Value']
                elif field['FieldName'] == 'Birthday':
                    self.birthDate = field['Value']
                elif field['FieldName'] == "Group participation":
                    if field["Value"]:
                        for group in field["Value"]:
                            if group["Label"] == "Ride Leader":
                                self.isRideLeader = True
        except Exception as ex:
            msg = "Other error in member.__init__() " + ex.__repr__()
            self.postError(msg, aDict, ex)

    def postError(self, msg, aDict, exception):
        """
        add an error to the members error list.  If there is no error list,
        create one.
        """
        if self.memberError is None:
            self.memberError = MemberError(aDict,
                                           msg,
                                           exception)
        else:
            self.memberError.addErrorRecord(msg, exception)
        CONFIG.logger.exception(msg)

    def validate(self):
        """make sure that all required attributes of a member are present
        """
        if (self.memberID is None or
                self.firstName is None or
                self.lastName is None or
                self.email is None or
                self.memberSince is None or
                self.renewalDue is None or
                self.renewalDue < self.memberSince):
            CONFIG.logger.error(msg="invalid member record: "
                                + str(self))
            self.isValid = False

    def toDict(self):
        """
        render a json representation of a member
        """
        aDict = {}
        aDict["clubMemberId"] = self.memberID
        aDict["firstName"] = self.firstName
        aDict["lastName"] = self.lastName
        aDict['alias'] = self.alias
        aDict['city'] = self.city
        aDict['emailAddress'] = self.email
        aDict["gender"] = self.gender
        if self.memberSince:
            aDict["membershipStart"] = self.memberSince.isoformat()
        else:
            aDict['membershipStart'] = None
        if self.renewalDue:
            aDict["membershipEnd"] = self.renewalDue.isoformat()
        else:
            aDict['membershipEnd'] = None
        aDict['membershipType'] = self.membershipType
        aDict['phone1'] = self.mobilePhone
        aDict['phone2'] = self.telephone
        aDict["rideLeader"] = self.isRideLeader
        aDict['state'] = self.state
        aDict['emergencyContactName'] = self.emergencyContact
        aDict['emergencyContactPhone'] = self.emergencyContactPhone
        if self.birthDate:
            aDict['birthDate'] = self.birthDate
        else:
            aDict['birthDate'] = ''
        if self.zipCode:
            aDict['zipCode'] = self.zipCode
        else:
            aDict['zipCode'] = ''
        if self.profileLastUpdated:
            aDict['userLastModified'] = self.profileLastUpdated.isoformat()
        else:
            aDict['userLastModified'] = None
        return aDict

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        aString = "Membership information for " + self.firstName + " " + \
                  self.lastName + " " + "\tMember ID = "\
                  + str(self.memberID) + "\n"
        if self.memberError is None:
            return aString
        else:
            aString += "/tMember Record has errors"
            for msg in self.memberError.messages:
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

    msg = "RideStatsMemberUpdate started at " + startTime.isoformat() + "\n"
    msg += "RideStatsMemberUpdate completed at " + endTime.isoformat() + "\n"
    msg += "duration was " + str(endTime - startTime) + "\n"
    msg += 'The RideStats URL was ' + CONFIG.parms['RideStatsURL'] + '\n'
    msg += "There were " + str(numMembers) + " members processed.\n"
    msg += "There were " + str(numerrorList) + " members with errors\n"
    if errorList:
        msg = msg + "The following records had problems:\n"
        for memberError in errorList:
            msg += '\t' + memberError.firstName + ' ' + memberError.lastName + "\n"
            for errorMessage in memberError.messages:
                msg += "\t\t" + str(errorMessage) + "\n"
    msg += "the response from RideStats was:\n"
    msg += rideStatsResponse

    try:
        server = smtplib.SMTP(CONFIG.parms['smtpServer'],
                              CONFIG.parms['smtpPort'])
        server.starttls()
        server.login(CONFIG.parms['smtpFromAddress'],
                     CONFIG.parms['smtpPassword'])
        msg = "Subject:  WARequests Report\n\n" + msg
        server.sendmail(CONFIG.parms['smtpFromAddress'],
                        CONFIG.parms['smtpToAddress'],
                        msg)
    except Exception as ex:
        CONFIG.logger.exception(ex)
    finally:
        if server is not None:
            server.quit()


try:
    startTime = datetime.utcnow()
    CONFIG = Config()
    WA_API = WaAPIClient(CONFIG.parms['clientID'],
                         CONFIG.parms['clientSecret'],
                         CONFIG.parms['apiKey'],
                         CONFIG.logLevel)
    response = getMembers()
    memberList = []
    errorList = []
    payload = {"clubId":"HBC"}
    for each in response:
        member = Member(each)
        if member.memberError:
            errorList.append(member.memberError)
        if member.isValid:
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
                           (payload))
        rideStatsResponse = "RideStats URL was localHost.  see log for details"
    if CONFIG.logger.isEnabledFor(logging.DEBUG):
        CONFIG.logger.debug("valid members = %s", memberList)
        CONFIG.logger.debug("errorList = %s", str(errorList))
    if CONFIG.logger.isEnabledFor(logging.INFO):
        CONFIG.logger.info('%s members were successfully validated', str(len(memberList)))
        CONFIG.logger.info("response from RideStats was %s", rideStatsResponse)
        CONFIG.logger.info('%s non-fatal errors were found', str(len(errorList)))
    emailResults()

except Exception as ex:
    print(ex)

finally:
    logging.shutdown()
