BMAT Test
=========

Description
-----------
Web service will listen to a port, will answer to GET / POST requests and return JSON dictionaries. It is enabling the following operations:

- Insert a new radio station.
- Insert a new artist.
- Insert a new song.
- Insert a new play.
- Get all the plays for a given song between two dates.
- Get all the songs played on a given channel between two dates.

Dependencies
------------

- falcon==1.1.0
- gunicorn==19.6.0
- python-dateutil==2.5.3
- python-mimeparse==1.6.0
- six==1.10.0
- SQLAlchemy==1.1.3


Quickstart
----------

This application has been tested on Linux. 
The application doesnt need to access to internet, does not use internet for installation. All packeges requirements are at folder packages.


To use this application you must follow this steps:

*Note: for list the options available make the script:*

       # make list


**Steps to deploy the application:**

1.  If you use virtualenv or virtualenvwrapper, first create and activate an environment, before running the setup. For example:

        # virtualenv2 python2 env_name

        # . env_name /bin/activate

2. To install all requirements contained at ./packages:  

        # make PACKAGEDIR=Full_directory_to_packages setup

        

Execute app
-----------

Finally to run the application, for example, being accesible at http://127.0.0.1:5000:

    # make run IP=127.0.0.1 PORT=5000
    

License
-------
GPL. Author: jesusropi@gmail.com
