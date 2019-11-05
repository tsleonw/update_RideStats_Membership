#!/usr/bin/env python3

"""
This module will make sure that the UpdateRideStats job ran successfully by checking the 
logs directory to make sure that a file called "ursm.log" exists and was created during 
current date.  If no file is found, or if the creation date is not the same as the current 
date, the email is sent to the administrator alerting them that the job did not run and a
log file was not produced.  
"""
from os import path
from datetime import date, datetime

logDirectory = '/Users/tslcw/UpdateRideStats/logs/'

lastLogTimeStamp = path.getmtime(logDirectory + 'ursm.log')
lastLogDate = date.fromtimestamp(lastLogTimeStamp)
today = date.today()

if lastLogDate == today:
    print('job ran today')
else:
    print('Job last ran on '+ lastLogDate)