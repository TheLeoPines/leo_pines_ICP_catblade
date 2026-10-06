#Code inspired by game dev Chris Bradfield who was inspired by Notch
import pygame as pg #Importing pygame as "pg"
from os import path
from sprites import * #Importing from a different made file to access on this file.
from settings import * #Importing from a different made file to access on this file.
from utils import * #Importing froma  different made file to access on this file.

'''


Data types: Boolean, JSON, strings.

Input (events):Keyboard, mouse, right click, voice,
power button, eye tracking, camera, gyroscoping, electrostatic, location, volume, 
microphone.


Process: cursor position, position of the player, physics.

Output: Graphics - things are drawn, sounds: jump, power up, walking, haptics.



'''
#Making the class game that uses all the mechanincs to make it
class Game:
    #Inputing screen and title that won't disappear when the player starts the program.
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen=pg.display.set_mode((WIDTH, HEIGHT))
        print("game initialized...")
        pg.display.set_caption(TITLE)
        self.running=True 
        self.playing=True
        self.clock=pg.time.Clock()

    def load_data(self,map):
        self.game_dir=path.dirname(__file__)
        self.img_dir=path.join(self.game_dir, 'images')
        self.snd_dir=path.join(self.game_dir,'audio')
        self.map=Map(path.join(self.game_dir,map))


    #Outputing a sprite/a character to controlled and outputing a wall and mob.
    def new(self):
        self.load_data('level1.txt')
        print(self.map.data)
        self.all_sprites=pg.sprite.Group()
        self.all_walls=pg.sprite.Group()
        self.all_mobs=pg.sprite.Group()
    
      
#Enumarating from map to titles to make player and walls as a tile.
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile=='1':
                    Wall(self,col,row)#For Wall in map
                if tile=="M":
                    Mob(self, col, row)#For mob in map
                # if tile =='P':
                    #Player (self,col,row)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile=='P':
                    Player(self,col, row)#For player is map


                



    #The process of the screen rendering in the background.
    def run(self):
         self.playing=True
         while self.running:
            self.dt=self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()


   #Output of the events of the drawings and quits when user is not playing.
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                if self.playing:
                    self.playing = False
                self.running = False

    def draw_text(self,text,size,color,x,y):
        font_name=pg.font.match_font('arial')
        font=pg.font.Font(font_name,size)
        text_surface=font.render(text,True,color)
        text_rect=text_surface.get_rect()
        text_rect.midtop=(x,y)
        self.screen.blit(text_surface,text_rect)
    
    #Calculates next frame it renders and updates the screen with the new frame.
    def update(self):
        self.all_sprites.update()
    #Output of filling out the sprites with color
    def draw(self):
        #This order matters as the first things are on the botton because they are the first to be drawn
        #The last lines are on the top
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text("Frames per second:"+str(floor(1/self.dt)),24,WHITE,WIDTH/2,HEIGHT/4)
        pg.display.flip()

   
#This runs the game
if __name__ == "__main__":
    g=Game()

#To run the game without the program quitting.
while g.running:
     g.new()
     g.run()


