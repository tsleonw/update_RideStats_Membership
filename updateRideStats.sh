#!/usr/bin/env bash
#
# Script to run the UpdateRideStatsMembership Program
# created Oct. 28, 2019
# @author:  Leon Webster
# ©2022 RideStats, LLC.
# cd to the path where this script is located, just in case.
cd /var/www/webroot/ROOT
# make sure the logs directory exists
if [ ! -d "logs" ] ;
then
  mkdir "logs"
fi
#activate the virtual environment.
source .venv/bin/activate
python3 src/ursm/updateRideStatsMembership.py PROD
deactivate
