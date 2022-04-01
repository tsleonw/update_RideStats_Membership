#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 18:53:51 2019

@author: tslcw

used as a configuration file for the update rideStats program.  But contains no sensitive information.
See .env.sample for an example .env file

Created on Sun Jan  6 18:53:51 2019

@author Leon Webster
©2022 RideStats, LLC
"""
CONFIG = {
    'PROD': {'smtpServer': 'smtp.gmail.com',
             'smtpPort': 587,
             'filter': 'member eq true',
             'top': 0,
             'async': False,
             'select': "'User ID' 'Alias' 'Gender' 'Member Since' 'Renewal Due'\
              'Membership Status' 'Group Participation' 'Mobile Phone' 'Home Phone'\
              'Address' 'City' 'State' 'Postal code' 'Member emails and newsletters' \
              'Emergency Contact' 'Emergency Contact Phone'  'Birthday' 'Birthdate' \
              'Creation Date' 'Country'  ",
             'PostToRideStats': True
             },
    'QA': {'smtpServer': 'smtp.gmail.com',
           'smtpPort': 587,
           'filter': 'member eq true',
           'top': 0,
           'async': False,
           'select': "'User ID' 'Alias' 'Gender' 'Member Since' 'Renewal Due'\
              'Membership Status' 'Group Participation' 'Mobile Phone' 'Home Phone'\
              'Address' 'City' 'State' 'Postal code' 'Member emails and newsletters' \
              'Emergency Contact' 'Emergency Contact Phone'  'Birthday' 'Birthdate' \
              'Creation Date' 'Country' ",
           'PostToRideStats': True,
           }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s | %(levelname)s | %(module)s:%(lineno)d | %(message)s'
        },
        'simple': {
            'format': '%(asctime)s | %(levelname)s | %(message)s'
        },
    },
    'handlers': {
        'QA_file': {'class': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': 'logs/ursm.qa.log',
                    'formatter': 'verbose',
                    'when': 'M',
                    'backupCount': 10,
                    },
        'PROD_file': {'class': 'logging.handlers.TimedRotatingFileHandler',
                      'filename': 'logs/ursm.log',
                      'formatter': 'verbose',
                      'backupCount': 30,
                      },
        'console': {'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                    'stream': 'ext://sys.stdout',
                    },
    },
    'loggers': {
        'PROD_URSM': {
            'level': 'INFO',
            'handlers': ['PROD_file'],
        },
        'QA_URSM': {
            'level': 'DEBUG',
            'handlers': [  # 'console', un-comment to log to console
                         'QA_file'],
        },
    },
}
