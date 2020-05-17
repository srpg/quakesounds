import os, path, soundlib
from events import Event
from stringtables.downloads import Downloadables

__FILEPATH__	= path.path(__file__).dirname()
DOWNLOADLIST_PATH	= os.path.join(__FILEPATH__ + '/download/download.txt')

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

@Event('rpg_playerspawn')
def rpg_playerspawn(args):
	userid = args.get_int('userid')
	if not userid in players:
		players[userid] = 0

@Event('player_death')
def player_death(args):
	userid = args.get_int('userid')
	attacker = args.get_int('attacker')
	if attacker > 0:
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

def setFirstblood(a):
	global _firstblood
	_firstblood = a

def getSound(i):
	if i in _sounds:
		return _sounds[i]
	return None

_sounds = {3: 'rampage.mp3', 5: 'dominating.mp3', 7: 'killingspree.mp3', 9: 'monsterkill.mp3', 12: 'ludicrouskill.wav', 14: 'ultrakill.mp3', 16: 'godlike.mp3', 18: 'wickedsick.mp3', 21: 'holyshit.mp3', 24: 'unstoppable.mp3', 32: 'bottomfeeder.mp3'}
_others = {0: 'prepare.mp3', 1: 'firstblood.wav'}
