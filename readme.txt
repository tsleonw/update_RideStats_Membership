UpdateRideStats is a small application that invokes the Wild Apricot Web Service API to extract a list of HBC Members.  Each member in the list is checked to make sure that there is sufficient data to populate the membership database in RideStats.  If data is missing, it attempts to fill in the data with reasonable values.  For example, if the "Profile Last Updated" field is missing, today's date is used.  All phone numbers are trimmed to the first 10 digits in the string.  After the data is validated, the programs invokes a RideStats web service to upload the list of members to RideStats.  Lastly, the program sends an email to 'leon@leonwebster.com' informing him of the results.

the following files are included in this zip file:

1.  updateRideStats.sh  -- the shell command which runs the application.  
2.  updateRideStatsMembership.py -- the main python program.  This program may be run from the command line where the usage is:
    python3 updateRideStatsMembership.py PROD | QA
    where "PROD" or "QA" represent the environment that is being invoked. 
3.  URSMCONFIG.py  -- A python file containing the configuration information for both the PROD and QA environment.  The configuration values are entries in a dictionary.  This scheme is used in lieu of a more traditional config file since it is just as easy to change a python file as it is to change a config file, and no compilation is needed.
4.  rideStatsClient.py -- this file encapsulates the interaction with the RideStats web service.
5.  waAPIClient.py -- this file encapsulates the interaction with the Wild Apricot API.
6.  Deploy.py -- this file automates the deployment of the system, creating the zip file and copying all files to either a production directory
    or a test directory (to test the deployment).

This directory should be unzipped to create a "updateRideStats" directory which is located in the user's home directory.  

The job is scheduled using the standard cron utility with the followig crontab entry:
     0 0* * * * cd ~/updateRideStats && ./updateRideStats.sh


