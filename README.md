# gmusic
Google Music Terminal Interface; written in Python 2.

## Before We Start
Create a `credentials.json` file in data/unlocked/. In this file, add the following...

```json
{
  "username": "___",
  "password": "___"
}
```
Note: if you use two-step authentication, password needs to be an application-specific password.

NEVER commit this data to your fork. You can use `python3 lock.py` to password-encrypt your credentials and `python3 unlock.py` to pasword-decrypt locked data.

## Usage
To launch Google Music Terminal Interface, simply run the `launch.py` script; commands will be displayed at the bottom of the terminal next to the command line interface, and pertinent information will be above.
