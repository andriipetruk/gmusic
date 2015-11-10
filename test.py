from gmusicapi import *
from objects.CursedMenu import CursedMenu
import json


client = Mobileclient()
credentials = json.load(open('data/unlocked/credentials.json','r'))
client.login(credentials['username'], credentials['password'], Mobileclient.FROM_MAC_ADDRESS)

songs = client.get_all_songs()
cbl = [s['title'] for s in songs if 'Carbon Based' in s['artist']]

x = CursedMenu()
x.show(cbl,title='Carbon Based Lifeforms',subtitle="All Tracks")
