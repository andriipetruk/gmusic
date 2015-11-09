from gmusicapi import *
client = Mobileclient()
import json
credentials = json.load(open('data/unlocked/credentials.json','r'))

client.login(credentials['username'], credentials['password'], Mobileclient.FROM_MAC_ADDRESS)

songs = client.get_all_songs()
cbl = [s['title'] for s in songs if 'Carbon Based' in s['artist']]
from objects.CursedMenu import CursedMenu
def show(lis):
   x = CursedMenu(lis,title="Carbon Based Lifeforms",subtitle="All Tracks")
   x.menu()

show(cbl)
