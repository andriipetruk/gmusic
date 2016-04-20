import os, json, subprocess, sys
from subprocess import Popen, PIPE

default_terminal_color = '\033[m'

# Possible Dependencies:
#   gir1.2-gstreamer-1.0 libqt5gstreamer-1.0-0 libqtgstreamer-1.0-0
#   apt-cache -n search "gstreamer-1.0"

# Top dependency
# you can't really run anything in python without this
pip_command = 'which pip'
pip_popen = Popen(pip_command.split(" "), stdout=PIPE, stderr=PIPE)
pip_result, pip_error = pip_popen.communicate()
pip_missing = not ('pip' in pip_result)
if pip_missing:
    print('It looks like pip was not found on your system.')
    print('You can install pip with this command\n')
    print('\033[93m\tsudo apt-get install python-pip')
    print(default_terminal_color)
    sys.exit(1)


# Check Dependencies Commands
check_gst_command = 'dpkg -l python-gst-1.0'
pip_list = 'pip list'

# Check if this system has the required packages
gst_popen = Popen(check_gst_command.split(" "), stdout=PIPE, stderr=PIPE)
pip_list_popen = Popen(pip_list.split(" "), stdout=PIPE, stderr=PIPE)

# get the output from the popen/shell command
gst_result, gst_error = gst_popen.communicate()
pip_list_result = pip_list_popen.communicate()[0]

gst_missing = ("no packages found" in gst_error)
gmusicapi_missing = not ("gmusicapi" in pip_list_result)
pygobject_missing = not ("pygobject" in pip_list_result)

# blank line to differentiate between the PS1 / any accidental output
# *cough*dpkg*cough*
print '\n'

if gst_missing:
    print('It looks like python-gst-1.0 was not found on your system.')
    print('You can install them with this command\n')
    print('\033[93m\tsudo apt-get install python-gst-1.0\n')
    print(default_terminal_color)

if gmusicapi_missing or pygobject_missing:
    print('It looks like you don\'t have all the pip requirements.')
    print('You can install them with this command\n')
    print('\033[93m\tsudo pip install -r requirements.txt\n')
    print(default_terminal_color)

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
