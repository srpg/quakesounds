import path
from events import Event
from core import GAME_NAME
from players.entity import Player
from engines.sound import Sound
from players.constants import HitGroup
from stringtables.downloads import Downloadables
from listeners import OnLevelInit

__FILEPATH__	= path.Path(__file__).dirname()
DOWNLOADLIST_PATH	= __FILEPATH__ + '/download/download.txt'

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

@OnLevelInit
def map_start(map):
	players.clear()

def _play(sound):
	Sound(f'quake/{sound}')
		    
@Event('round_start')
def round_start(args):
	_play('prepare.mp3')
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
			players[userid] = 0
			_play('suicide.wav')

		player = Player.from_userid(userid)
		if not player.team == Player.from_userid(attacker).team:
			players[userid] = 0
			players[attacker] += 1

			if _firstblood and GAME_NAME == 'cstrike':
				_play('firstblood.wav')
				setFirstblood(False)
			else:
				sound = getSound(players[attacker])
				if sound is not None:
					_play(sound)

			if GAME_NAME == 'cstrike' and args.get_int('headshot'):
				_play('headshot.mp3')
			else:
				if player.last_hitgroup == HitGroup.HEAD:
					_play('headshot.mp3')

			if args.get_string('weapon') == 'knife':
				_play('humiliation.mp3')

def setFirstblood(a):
	global _firstblood
	_firstblood = a
	
def getSound(i):
	if i in _sounds:
		return _sounds[i]
	return None

_sounds = {5: 'multikill.mp3', 6: 'rampage.mp3', 7: 'killingspree.mp3', 9: 'dominating.mp3', 15: 'ultrakill.mp3', 18: 'ludicrouskill.wav',  20: 'wickedsick.mp3', 21: 'monsterkill.mp3', 23: 'holyshit.mp3', 24: 'godlike.mp3', 32: 'bottomfeeder.mp3', 35: 'unstoppable.mp3'}
