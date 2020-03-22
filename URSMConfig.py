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
             'smtpFromAddress': 'hbcridestats@gmail.com',
             'smtpPassword': 'hbcbiker',
             'smtpToAddress': 'leon@leonwebster.com',
             'clientAccount': '53245',
             'apiKey': 'c93tyt9218h78gg4ewgx5pk0qjxbni',
             'clientID': '3zt2ef1tqt',
             'clientSecret': 'jyx4b6f77xsjlwzpuxsf8bsc8ckc72',
             'filter': 'member eq true',
             'top': 0,
             'async': False,
             'select': "'User ID' 'Alias' 'Gender' 'Member Since' 'Renewal Due' \
              'Membership Status' 'Group Participation' 'Mobile Phone' 'Telephone' \
              'City' 'State' 'Postal code' 'Member emails and newsletters' \
              'Emergency Contact' 'Emergency Contact Phone'  'Birthday'",
             'RideStatsURL': 'https://hbc.ridestats.bike/admin/webservices/membershipUpdateService',
             'RideStatsClubID': 'HBC',
             'RideStatsKey': 'bd582f04-c87c-4f1e-b26a-97d3968a2ca2',
             'PostToRideStats': True
             },
    'QA': {'logLevel': 'DEBUG',
           'logFile': 'logs/ursm.qa.log',
           'smtpServer': 'smtp.gmail.com',
           'smtpPort': 587,
           'smtpFromAddress': 'hbc.qa.ridestats@gmail.com',
           'smtpPassword': 'KrgA8Uivh9EAiWq',
           'smtpToAddress': 'leon@leonwebster.com',
           'clientAccount': '53245',
           'apiKey': 'c93tyt9218h78gg4ewgx5pk0qjxbni',
           'clientID': '3zt2ef1tqt',
           'clientSecret': 'jyx4b6f77xsjlwzpuxsf8bsc8ckc72',
           'filter': 'member eq true',
           'top': 0,
           'async': False,
           'select': "'User ID' 'Alias' 'Gender' 'Member Since' 'Renewal Due'\
            'Membership Status' 'Group Participation' 'Mobile Phone' 'Telephone'\
            'City' 'State' 'Postal code' 'Member emails and newsletters' \
            'Emergency Contact' 'Emergency Contact Phone'  'Birthday' 'Creation Date'  ",
           'RideStatsURL': 'https://hbc.qa.ridestats.bike/admin/webservices/membershipUpdateService',
           'RideStatsClubID': 'HBC',
           'RideStatsKey': 'a6f674ed-645f-4817-b61a-49cba307673d',
           'PostToRideStats': True
           }
}
