import pygame as pg
#Constants used throughout all the other files to make the game
WIDTH=1024
HEIGHT=768
TITLE="Best game ever!!!"
TILESIZE=32
FPS=30


#Colors
BGCOLOR=("blue")
WHITE=(255,255,255)
BLUE=(0,255,0)
RED=(255,0,0)
BLACK=(0,0,0)

#Player settings
PLAYER_SPEED=300
PLAYER_HIT_RECT=pg.Rect(0,0,TILESIZE-5,TILESIZE-5)
MOB_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)