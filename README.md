# gmusic [![Code Climate](https://codeclimate.com/github/etkirsch/gmusic/badges/gpa.svg)](https://codeclimate.com/github/etkirsch/gmusic) <a href="https://codeclimate.com/github/etkirsch/gmusic/coverage"><img src="https://codeclimate.com/github/etkirsch/gmusic/badges/coverage.svg" /></a>
Google Music Terminal Interface; written in Python 2.

## Before We Start
Create a `credentials.json` file in data/unlocked/. In this file, add the following...

```
mkdir data/unlocked
echo '{"username": "you@gmail.com", "password": "yourpassword"}' >> data/unlocked/credentials.json
```
Note: if you use two-step authentication, password needs to be an application-specific password.

NEVER commit this data to your fork. You can use `python3 lock.py` to password-encrypt your credentials and `python3 unlock.py` to pasword-decrypt locked data.


### Dependencies

The `python-pip` package that comes with ubuntu is horribly broken, and doesn't seem to work.. which is hilarious, cause so many ubuntu apps use python....
To get a working version of `python-pip`:
```
curl -O https://pypi.python.org/packages/source/p/pip/pip-7.1.2.tar.gz#md5=3823d2343d9f3aaab21cf9c917710196
tar xvfz pip-7.1.2.tar.gz
cd pip-7.1.2
sudo python setup.py install
```

Then, install the dependencies specific to gmusic

```
sudo pip install -r requirements.txt --no-cache-dir 
```

And `pygst`:

```
sudo apt-get install python-gst0.10 gstreamer0.10-plugins-good gstreamer0.10-plugins-ugly
```



## Usage
To launch Google Music Terminal Interface, simply run the `launch.py` script; commands will be displayed at the bottom of the terminal next to the command line interface, and pertinent information will be above.

Example:
```
python launch.py
```
