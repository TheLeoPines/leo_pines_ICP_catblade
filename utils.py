import pygame as pg #Importing pygame as pg
from settings import *#Importing setttings.py
from math import floor

#Making a map class to make the map when called in main.py
class Map:
    def __init__(self,filename):
        self.data=[]
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth=len(self.data[0])
        self.tileheight=len(self.data)
        self.width=self.tilewidth * TILESIZE
        self.height=self.tileheight*TILESIZE
        print('map instantiated')
#Making a Spritesheet class to convert images to png when called in main.py
class Spritesheet:
    #Loading image and converts png to something pygame can use
    def __init__(self,filename):
        self.spritesheet=pg.image.load(filename).convert()

    def get_image(self,x,y,width,height):
        image=pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        new_image=pg.transform.scale(image, (width,height))
        image=new_image
        return image
# Making a Cooldown class for time and cooldown for the object.
class Cooldown:
    def __init__(self):
        #Creating the starting times
        self.event_time=0
        self.current_time=0
        self.delta=0
    #Creating the cooldown as ticks
    def ticking(self):
        self.current_time=floor((pg.time.get_ticks())/1000)
        #When assigned to equal it caused an error due to delta needing difference.
        self.delta=self.current_time-self.event_time 
    def start(self):
        self.start_time=pg.time.get_ticks()
    def ready(self):
        self.current_time=pg.time.get_ticks()

    