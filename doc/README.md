

**This is very much a work in progress**
UpdateRideStatsMembership (URSM) is a python program that will read membership data from Wild Apricot and use that data to update membership information on RideStats.  It does this using the Wild Apricot API and the RideStats web service.  

# Requirements:

UpdateRideStatsMembership requires the following:
- A current version of Python 3.  It has been tested with version 3.9, but should work with any version of Python greater than 3.6.
- [Requests](https://docs.python-requests.org/en/master/) version 2.26.0 Requests is a wonderful library for utilizing http.  More information about Requests is available at [https://docs.python-requests.org/en/master/]()
- [python-dotenv](https://github.com/theskumar/python-dotenv).  Dotenv is used to support .env files which contain key-value pairs.  This is all in an attempt to move the program closer to the [12-factor]( https://12factor.net) principles.  

# Setup:

In order to use this program you need to do the following:

1.  Unzip the updateRideStats.zip file to create a updateRideStats directory. 
2.  cd to the updateRideStats directory.
3.  Create a virtual environment using the following command:
```
	python3 -m venv .venv --prompt ursm

```

4. activate the virtual environment with the following command:
```
	source .venv/bin/activate
```
5. install the requests library with the following command:
	
```
	pip install requests
```

6. install the dotenv library with the following command:
```
	pip install python-dotenv
```

7. create a .env file with the appropriate values for your installation.  You can use .env.sample as a template. 
8. modify the updateRideStats.sh file to make sure that all directory references are accurate
9. create an entry in the crontab file to execute the updateRideStats.sh file at the time of your choosing.  Here is the entry I am using:
```
	0 0 * * * /var/www/webroot/ROOT/updateRideStats.sh
```
This entry is the absolute path to the shell script, and will run the script once a day at midnight.  
