#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 18:53:51 2019

@author: tslcw

used instead of a configuration file for the update rideStats program.
"""

PROD = {'logLevel':'INFO',
        'logFile':'ursm.log',
        'smtpServer':'smtp.gmail.com',
        'smtpPort':587,
        'smtpFromAddress':'hbcridestats@gmail.com',
        'smtpPassword':'hbcbiker',
        'smtpToAddress':'leon@leonwebster.com',
        'clientAccount':'53245',
        'apiKey':'c93tyt9218h78gg4ewgx5pk0qjxbni',
        'clientID':'3zt2ef1tqt',
        'clientSecret':'jyx4b6f77xsjlwzpuxsf8bsc8ckc72',
        'filter':'member eq true',
        'top': 0,
        'async':False,
        'select':"'User ID' 'Alias' 'Gender' 'Member Since' 'Renewal Due' \
        'Membership Status' 'Group Participation' 'Mobile Phone' 'Telephone' \
        'City' 'State' 'Postal code' 'Member emails and newsletters'",
        'RideStatsURL':'https://hbc.ridestats.bike/admin/webservices/membershipUpdateService',
        'RideStatsClubID':'HBC',
        'RideStatsKey':'7c4155f5-5f58-4cd9-a18c-04804eeaa6cd'
        }
DEV = {'logLevel':'DEBUG',
       'logFile':'ursm.log',
       'smtpServer':'smtp.gmail.com',
       'smtpPort':587,
       'smtpFromAddress':'HBC.QA.RideStats@gmail.com',
       'smtpPassword':'hbcbiker',
       'smtpToAddress':'leon@leonwebster.com',
       'clientAccount':'53245',
       'apiKey':'c93tyt9218h78gg4ewgx5pk0qjxbni',
       'clientID':'3zt2ef1tqt',
       'clientSecret':'jyx4b6f77xsjlwzpuxsf8bsc8ckc72',
       'filter':'member eq true',
       'top': 10,
       'async':False,
       'select':"'User ID' 'Alias' 'Gender' 'Member Since' 'Renewal Due'\
       'Membership Status' 'Group Participation' 'Mobile Phone' 'Telephone'\
       'City' 'State' 'Postal code' 'Member emails and newsletters'",
       'RideStatsURL':'https://hbc.qa.ridestats.bike/admin/webservices/membershipUpdateService',
       'RideStatsClubID':'HBC',
       'RideStatsKey':'7c4155f5-5f58-4cd9-a18c-04804eeaa6cd'
      }
