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

GAME: Snake Game

GOALS: Eat apples, gain as much apples as possible, and survive.

RULES: You cannot go through walls, teleport to apples, or not start from 0.

FEEDBACK: Will stop the game and put a collided face one bumping into a wall.

FREEDOM: You can go any direction you want.

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
        self.high_score=0
        self.score=0
    #Loads external game files like images and audios and etc...
    def load_data(self,map):
        self.game_dir=path.dirname(__file__)
        self.game_save_file = path.join(self.game_dir, "highscore.txt")
        self.img_dir=path.join(self.game_dir, 'images')
        #Sound handling
        self.snd_dir=path.join(self.game_dir,'audio')
        self.pickup_snd=pg.mixer.Sound(path.join(self.snd_dir,"Picked_Coin_Echo.wav"))
        self.map=Map(path.join(self.game_dir,map))
        #Tries to open a new file unless already made
        try:
            with open(self.game_save_file,'x',encoding="utf-8") as file:
                file.write("Hello!")
            print("file created succesfully!")

        except FileExistsError:
            print("File already exists")
        #Tries to save score to new made file and if nothing to read then set to 0 until updated
        with open(self.game_save_file,'r') as file:
            try:
                self.high_score=int(file.read())
            except:
                # self.high_score=0
                print("high score set to zero")

    #Outputing a sprite/a character to controlled and outputing a wall and mob.
    def new(self):
        self.load_data('level1.txt')
        print(self.map.data)
        #Creates sprite groups to organize and update all game objects together
        self.all_sprites=pg.sprite.Group()
        self.all_walls=pg.sprite.Group()
        self.all_mobs=pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_particles=pg.sprite.Group()
    
      
#Enumarating from map to titles to make player and walls as a tile.
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile=='1':
                    Wall(self,col,row)#For Wall in map
                if tile=="M":
                    Mob(self, col, row)#For mob in map
                if tile=="C":
                        Coin(self,col,row)
                # if tile =='P':
                    #Player (self,col,row)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile=='P':
                    self.player=Player(self,col, row)#For player is map
        #Background music
        pg.mixer.music.load(path.join(self.snd_dir,"an_untold_legend_v2.wav"))
        pg.mixer.music.play(loops=-1)


                



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
                if self.score>self.high_score: 
                    with open(path.join(self.game_dir,self.game_save_file),'w') as f:
                        f.write(str(self.score))

                #To quit the game
                if self.playing:
                    self.playing = False
                    
                self.running = False
    #Text attributes
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
        #Displays the text and updates when player collects a coin
        self.draw_text(f"Frames per second:{1/self.dt}", 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(f"Coins:{self.player.coins}", 24, WHITE, WIDTH/2, HEIGHT/7)
        self.draw_text(f"Score:{self.score}", 24, WHITE, WIDTH/2, HEIGHT/9)
        self.draw_text(f"High Score:{self.high_score}", 24, WHITE, WIDTH/2, HEIGHT/12)
        pg.display.flip()

   
#This runs the game
if __name__ == "__main__":
    g=Game()

#To run the game without the program quitting.
while g.running:
     g.new()
     g.run()


