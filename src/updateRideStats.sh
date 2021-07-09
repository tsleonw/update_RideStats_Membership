#!/usr/bin/env bash
source ~/.bash_profile
cd ~/UpdateRideStats
source env/bin/activate
python3 -m updateRideStatsMembership PROD
deactivate
