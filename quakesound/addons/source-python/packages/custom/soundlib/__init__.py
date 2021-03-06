# ========================================
# IMPORTS
# ========================================
from filters.players import PlayerIter
from engines.server import engine_server
from players.entity import Player
from players.helpers import edict_from_userid, index_from_userid

# ========================================
# SOUND PLAY
# ========================================

def playgamesound(userid, _sound):
	client_command(userid, 'play %s' % _sound)

# ========================================
# USERID GETTERS
# ========================================

def getUseridList():
	for i in PlayerIter.iterator():
		yield i.userid

def client_command(userid, __cmd__):
	engine_server.client_command(edict_from_userid(userid), __cmd__)
    
def getTeam(userid):
	return Player(index_from_userid(userid)).team
