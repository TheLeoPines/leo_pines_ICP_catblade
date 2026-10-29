import pygame as pg #Importing pygame as pg
from settings import *#Importing setttings.py
from math import floor #Importing math

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
    
# Making a Timer class for time and cooldown for the object.
class Timer:
    def __init__(self):
        #Creating the starting times
        self.event_time=floor((pg.time.get_ticks())/1000) #Creating the cooldown as ticks
    def get_delta(self):
        #returns diference in time in seconds from time of generatin of particles
        return floor((pg.time.get_ticks())/1000)-self.event_time
    