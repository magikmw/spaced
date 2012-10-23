from math import tan,radians

###
# CONSTANTS
###

GAME_TITLE = "Spaced"
GAME_VERSION = "Alpha 1"

#projection plane dimensions, etc.
PP_WIDTH     = 320  
PP_HEIGHT    = 200
PP_CENTRE_X  = PP_WIDTH/2
PP_CENTRE_Y  = PP_HEIGHT/2
FOV          = 60
PP_DISTANCE  = int((PP_WIDTH / 2) / tan(radians(FOV/2)))
ANGLE_SHIFT  = FOV/PP_WIDTH
SCALE        = 2
BAR_HEIGHT   = 50

#the player speed
PLAYER_SPEED = 0.05
TURN_SPEED = 3

#configuration options
HEAD_BOB = False