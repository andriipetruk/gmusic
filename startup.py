import os, json, subprocess, sys

# Check Dependencies
check_gst_command = 'dpkg -l python-gst-1.0'
check_gmusicapi_command = 'pip list | grep gmusicapi'
check_pygobject_command = 'pip list | grep pygobject'

gst_result = subprocess.check_output(check_gst_command.split(" "))
gmusicapi_result = subprocess.check_output(check_gmusicapi_command.split(" "))
pygobject_result  = subprocess.check_output(check_pygobject_command.split(" "))

# TODO: what if non-english system?
gst_missing = ("no packages found" in gst_result)
gmusicapi_missing = (not gmusicapi_result)
pygobject_missing = (not pygobject_result)

if gst_missing:
    print('It looks like python-gst-1.0 was not found on your system.')
    print('You can install them with this command\n')
    print('\033[93m\tsudo apt-get install python-gst-1.0')

if gmusicapi_missing or pygobject_missing:
    print('It looks like you don\'t have all the pip requirements.')
    print('You can install them with this command\n')
    print('\033[93m\tsudo pip install -r requirements.txt --no-cache-dir')

print(gst_missing)
print(gmusicapi_missing)
print(pygobject_missing)

if gst_missing or gmusicapi_missing or pygobject_missing:
    sys.exit(1)

# now that we have all the dependency shenanigans out of the way,
# load up the app
from gmusic.core.Core import Core


if not os.path.isfile('data/unlocked/credentials.json'):
    print('Welcome to GMusic, a Bash Terminal implementation of Google All-Access Music.')
    print('Please enter an application password for Google Music. This will be stored')
    print('locally on your device. WE WILL NEVER ACCESS THIS FILE OUTSIDE OF USE IN')
    print('GMUSIC ON THIS MACHINE. If you delete the file, you will be required to')
    print('rerun this script to generate a keyfile.\n')

    email = raw_input('Please enter your Google email:  ')
    password = raw_input('Please enter an application specific password:  ')
    with open('data/unlocked/credentials.json','w') as credentials:
    	json.dump({"username": email, "password": password}, credentials)

print('Welcome to GMusic. Logging in and loading your library.')

gm = Core()
gm.start()
