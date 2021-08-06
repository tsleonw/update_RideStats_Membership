#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 18:53:51 2019

@author: tslcw

used instead of a configuration file for the update rideStats program.
"""
CONFIG = {
    'PROD': {'logLevel': 'INFO',
             'logFile': 'logs/ursm.log',
             'smtpServer': 'smtp.gmail.com',
             'smtpPort': 587,
             'smtpToAddress': 'leon@leonwebster.com',
             'filter': 'member eq true',
             'top': 0,
             'async': False,
             'select': "'User ID' 'Alias' 'Gender' 'Member Since' 'Renewal Due'\
              'Membership Status' 'Group Participation' 'Mobile Phone' 'Telephone'\
              'Address' 'City' 'State' 'Postal code' 'Member emails and newsletters' \
              'Emergency Contact' 'Emergency Contact Phone'  'Birthday' 'Birthdate' 'Creation Date'  ",
             'RideStatsClubID': 'HBC',
             'PostToRideStats': True
             },
    'QA': {'logLevel': 'DEBUG',
           'logFile': 'logs/ursm.qa.log',
           'smtpServer': 'smtp.gmail.com',
           'smtpPort': 587,
           'smtpToAddress': 'leon@leonwebster.com',
           'filter': 'member eq true',
           'top': 0,
           'async': False,
           'select': "'User ID' 'Alias' 'Gender' 'Member Since' 'Renewal Due'\
              'Membership Status' 'Group Participation' 'Mobile Phone' 'Telephone'\
              'Address' 'City' 'State' 'Postal code' 'Member emails and newsletters' \
              'Emergency Contact' 'Emergency Contact Phone'  'Birthday' 'Birthdate' 'Creation Date'  ",
           'RideStatsClubID': 'HBC',
           'PostToRideStats': False
           }
}
