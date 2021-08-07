#!/usr/bin/env bash
source ~/.bash_profile
cd ~/UpdateRideStats
source .venv/bin/activate
python3 src/updateRideStatsMembership PROD
deactivate
