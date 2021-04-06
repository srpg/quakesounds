import os, path, soundlib
from events import Event
from core import GAME_NAME
from players.entity import Player
from players.helpers import index_from_userid
from players.constants import HitGroup
from stringtables.downloads import Downloadables

__FILEPATH__	= path.Path(__file__).dirname()
DOWNLOADLIST_PATH	= os.path.join(__FILEPATH__ + '/download/download.txt')

games = ['csgo', 'cstike

players = {}
_firstblood = False

def load():
	setDL()
    
def setDL():
	downloadables = Downloadables()
	with open(DOWNLOADLIST_PATH) as f:
		for line in f:
			line = line.strip()
			if not line:
				continue
			downloadables.add(line)


@Event('map_start')    
def map_start(args):
	players.clear()

def _play(userid, sound):
	for userid in soundlib.getUseridList():
		soundlib.playgamesound(userid, 'quake/%s' % sound)  
		    

@Event('round_start')
def round_start(args):
	for i in soundlib.getUseridList():
		soundlib.playgamesound(i, 'quake/prepare.mp3')
	setFirstblood(True)

@Event('player_spawn')
def player_spawn(args):
	userid = args.get_int('userid')
	if not userid in players:
		players[userid] = 0

@Event('player_death')
def player_death(args):
	userid = args.get_int('userid')
	attacker = args.get_int('attacker')
	if attacker > 0:
		if userid == attacker:
			for i in soundlib.getUseridList():
				soundlib.playgamesound(i, 'quake/suicide.wav')
		if not soundlib.getTeam(userid) == soundlib.getTeam(attacker):
			players[userid] = 0
			players[attacker] += 1

			if _firstblood:
				soundlib.playgamesound(attacker, 'quake/firstblood.wav')
				setFirstblood(False)
			else:
				sound = getSound(players[attacker])
				if sound:
					_play(attacker, sound)
			if GAME_NAME in games:
				if args.get_int('headshot'):
					for i in soundlib.getUseridList():
						soundlib.playgamesound(i, 'quake/headshot.mp3')
			else:
				Player(index_from_userid(userid)).last_hitgroup == HitGroup.HEAD:
					for i in soundlib.getUseridList():
						soundlib.playgamesound(i, 'quake/headshot.mp3')
	
			if args.get_string('weapon') == 'knife':
				for i in soundlib.getUseridList():
					soundlib.playgamesound(i, 'quake/humiliation.mp3')

def setFirstblood(a):
	global _firstblood
	_firstblood = a
	
def getSound(i):
	if i in _sounds:
		return _sounds[i]
	return None

_sounds = {5: 'multikill.mp3', 6: 'rampage.mp3', 7: 'killingspree.mp3', 9: 'dominating.mp3', 15: 'ultrakill.mp3', 18: 'ludicrouskill.wav',  20: 'wickedsick.mp3', 21: 'monsterkill.mp3', 23: 'holyshit.mp3', 24: 'godlike.mp3', 32: 'bottomfeeder.mp3', 35: 'unstoppable.mp3'}
_others = {0: 'prepare.mp3', 1: 'firstblood.wav'}
