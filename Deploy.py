#!/usr/bin/env python3
"""
This module automates the deployment of the files needed to Update the HBC membership in RideStats.
it can be invoked from a shell with the following command:

    python3 Deploy.py [PROD|TEST]

where "PROD" or "TEST" indicate the environment you wish to deploy.

This works by creating a zip file with all relevent files.  This file should be stored in Wild Apricot
at http://www.hiawathabike.org/resources/RideStats.  Then all files listed in the manifest are copied from the current directory to either
a production location
"""

from zipfile import ZipFile
from shutil import copy
import os
import sys

prodDir = "/Users/tslcw/updateRideStats"
testDir = "./deployTest"
manifest = ["waAPIClient.py",
            "URSMConfig.py",
            "updateRideStatsMembership.py",
            "hbc_Member.py",
            "member_Error.py",
            "updateRideStats.zip",
            "rideStatsClient.py",
            "updateRideStats.sh",
            "readme.txt",
            "Deploy.py",
            "RideStatsmapping.numbers"
            ]
targetDirectory = "/Users/tslcw/UpdateRideStats/Test/"

def copyFiles(manifest, targetDirectory):
    for file in manifest:
        newFile = copy(file,targetDirectory)
        print("created file:  ", newFile)

def createZipFile():
    """
    create a zip file of the files needed to update the membership list in rideStats.
    """

    zip = ZipFile('UpdateRideStats.zip', 'w')
    """
    zip.write('rideStatsClient.py')
    zip.write('updateRideStats.sh')
    zip.write('updateRideStatsMembership.py')
    zip.write('URSMConfig.py')
    zip.write("waAPIClient.py")
    zip.write("readme.txt")
    zip.write("Deploy.py")"""
    for file in manifest:
        if file != 'updateRideStats.zip':
            zip.write(file)
    zip.close()

createZipFile()
if len(sys.argv) < 2:
    print("usage: 'python3 Deploy [PROD|TEST]")
    exit(1)
else:
    if sys.argv[1] == "PROD":
        targetDirectory = prodDir
    elif sys.argv[1] == "TEST":
        targetDirectory = testDir
    else:
        print("usage: 'python3 Deploy [PROD|TEST]")
        exit(1)
if not os.path.exists(targetDirectory):
    os.makedirs(targetDirectory)
copyFiles(manifest, targetDirectory)
