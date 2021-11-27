#!/usr/bin/env python3
"""
This module automates the deployment of the files needed to Update the HBC membership in RideStats.
it can be invoked from a shell with the following command:

    python3 Deploy.py [PROD|QA]

where "PROD" or "QA" indicate the environment you wish to deploy.

This works by creating a zip file with all relevent files.  This file should be stored in Wild Apricot
at http://www.hiawathabike.org/resources/RideStats.  Then all files listed in the manifest are copied from the current directory to either
a production location
"""

import os
import sys
from shutil import copy
from zipfile import ZipFile

prodDir = "/Users/tslcw/UpdateRideStats"
testDir = "/Users/tslcw/Dropbox/Projects/UpdateRideStatsMembership/deployTest"
manifest = ["src/ursm/deploy.py",
            "src/ursm/hbc_Member.py",
            "src/ursm/member_Error.py",
            "src/ursm/rideStatsClient.py",
            "src/ursm/updateRideStatsMembership.py",
            "src/ursm/URSMConfig.py",
            "src/ursm/waAPIClient.py",
            "updateRideStats.sh",
            ".env",
            ".env.sample",
            "LICENSE",
            '.gitignore',
            "doc/RideStatsmapping.numbers",
            'doc/README.md',
            ]


def copyFiles(target_directory):
    for file in manifest:
        newFile = copy(file, target_directory)
        print("created file:  ", newFile)


def createZipFile(target_directory):
    """
    create a zip file of the files needed to update the membership list in rideStats.
    """

    with ZipFile(target_directory + '/UpdateRideStats.zip', 'w') as deployZip:
        deployZip.debug = 3
        for file in manifest:
            deployZip.write(file)


if len(sys.argv) < 2:
    print("usage: 'python3 Deploy [PROD|TEST]")
    exit(1)
else:
    if sys.argv[1] == "PROD":
        targetDirectory = prodDir
    elif sys.argv[1] == "QA":
        targetDirectory = testDir
    else:
        print("usage: 'python3 Deploy [PROD|QA]")
        exit(1)
#os.chdir("/")
if not os.path.exists(targetDirectory):
    os.makedirs(targetDirectory)
createZipFile(targetDirectory)
# need to remember why I am copying files...
# copyFiles(targetDirectory)
