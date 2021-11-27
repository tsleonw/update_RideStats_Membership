#!/usr/bin/env bash
source ~/.bash_profile
cd ~/UpdateRideStats
if [ ! -d "logs" ] ;
then
  mkdir "logs"
fi
source .venv/bin/activate
python3 src/ursm/updateRideStatsMembership.py PROD
deactivate
