# gmusic [![Code Climate](https://codeclimate.com/github/etkirsch/gmusic/badges/gpa.svg)](https://codeclimate.com/github/etkirsch/gmusic) [![Build Status](https://travis-ci.org/etkirsch/gmusic.svg)](https://travis-ci.org/etkirsch/gmusic) [![Join the chat at https://gitter.im/etkirsch/gmusic](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/etkirsch/gmusic?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Google Music Terminal Interface; written in Python 2.

## Before We Start
When you first start GMusic, a startup script will prompt you for your Google email and an application-specific password. These credentials will NEVER be accessed by anyone here. Please do use an application-specific password, as we prefer you have the increased security it provides.


### Dependencies

Before we get to anything, we need to install the python package manager
```
sudo apt-get install python-pip
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
To launch Google Music Terminal Interface, simply run the `gmusic.py` script; commands will be displayed at the bottom of the terminal next to the command line interface, and pertinent information will be above.

Example:
```
python gmusic.py
```

or

```
./run
```



## DJ Streaming Service
A [GMusic DJ Streaming service](https://github.com/NullVoxPopuli/gmusic-sync-service) has been written by Preston Sego

## Authors
* Evan Kirsch ([etkirsch](https://github.com/etkirsch)) -- Lead Developer
* Preston Sego ([NullVoxPopuli](https://github.com/NullVoxPopuli)) -- Sync Service Author and Associate Developer
