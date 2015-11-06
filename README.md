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

NEVER commit this data to your fork. You can use `python lock.py` to password-encrypt your credentials and `python unlock.py` to pasword-decrypt locked data.

## Usage
At the moment, `gmusic` is used in a python2 interpreter window. The gist of this is as follows....

```python
from gmusic.py import GoogleMusic
gm = GoogleMusic()
gm.login()
gm.get(song="___", artist="___")
gm.play(2)
```

### Other commands

* **.get(song="", artist="", album="")** - Searches library for songs, artists, or albums matching the criteria provided; can specify any of the three fields and omit the rest if desired (e.g. `gm.get(artist="Hybrid")`)
* **.play(num)** - Plays a song using the `num` as index from the most recent search (`.get`)
* **.pause()** - Pauses a song
* **.stop()** - Stops a song
