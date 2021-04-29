# ========================================
# IMPORTS
# ========================================
from filters.players import PlayerIter
from players.entity import Player
from engines.sound import Sound

# ========================================
# SOUND PLAY
# ========================================

def playgamesound(userid, _sound):
	player = Player.from_userid(userid)
	Play_sound = Sound('%s' % (_sound))
	Play_sound.play(player.index)

# ========================================
# USERID GETTERS
# ========================================

def getUseridList():
	for i in PlayerIter.iterator():
		yield i.userid
    
def getTeam(userid):
	return Player.from_userid(userid).team
