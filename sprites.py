import pygame as pg #Importing pygame as "pg"
from settings import * #Importing from a different made file to access on this file.
from pygame.sprite import Sprite #Importing the sprite command from pygame as "Sprite"
from utils import * #Importing from a different made file to access on this file.

from random import randint #Importing randomizer

from os import path #using windows terminal to build file paths (so I can access images and audios and such.)

vec=pg.math.Vector2 #Velocity calculations

#Collision when two objects colide
def collide_hit_rect(one,two):
     return one.hit_rect.colliderect(two.rect)

#Collision and reposition of the sprite
def collide_with_walls(sprite,group,dir):
    #Check for x collision
    if dir=='x':
        #Checking to see if we've collided with hitrects
        hits=pg.sprite.spritecollide(sprite,group,False,collide_hit_rect)
        if hits:
            #This line checks to see if we're to the left side of the wall
            if hits[0].rect.centerx>sprite.hit_rect.centerx:
                #Reposition the player(sprite) to the left side of the wall
                sprite.pos.x=hits[0].rect.left-sprite.hit_rect.width/2
            #This line checks to see if we're to the right side of the wall
            if hits[0].rect.centerx<sprite.hit_rect.centerx:
                #Reposition the player(sprite) to the right side of the wall
                sprite.pos.x=hits[0].rect.right+sprite.hit_rect.width/2
            sprite.vel.x*=-1 #To bounce the player horizontally once colliding
            sprite.hit_rect.centerx=sprite.pos.x

    #Checking for y collision 
    if dir=='y':
        #Checking to see if we've collided with hitrects
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            #This line checks to see if we're to the above of the wall
            if hits[0].rect.centery > sprite.hit_rect.centery:
                #Reposition the player(sprite) to the top of the wall
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            #This line checks to see if we're to the below of the wall
            if hits[0].rect.centery < sprite.hit_rect.centery:
                #Reposition the player(sprite)to the bottom of the wall
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y*=-1 #To bounce player vertically
            sprite.hit_rect.centery = sprite.pos.y
        

#The Player class to call it in main.py to produce a player sprite
class Player(Sprite):
    # Gives the player a sprite and sets the size and color of the sprites
    def __init__(self,game,x,y):
        self.groups=game.all_sprites
        Sprite.__init__(self, self.groups)#To load sprite when game starts
        self.game=game
        self.spritesheet=Spritesheet(path.join(self.game.img_dir,"sprite_sheet.png"))
        self.load_images() #To load images, literally
        self.image=pg.Surface((TILESIZE,TILESIZE))
        self.image=self.spritesheet.get_image(0,0,TILESIZE,TILESIZE) #Getting the image
        self.image.set_colorkey(BLACK)
        # self.image.fill(WHITE)
        self.rect=self.image.get_rect()
        self.hit_rect=PLAYER_HIT_RECT
        self.vel=vec(0,0)
        self.acc=vec(0,0)#Acceleration, yayayaya!
        self.pos=vec(x*TILESIZE,y*TILESIZE)
         # animation stuff
        self.last_update = 0
        self.current_frame = 0
        self.dir = "none"
        self.coins = 0
        self.cofric=-0.1 #Another instance for friction for ice and etc
        self.jumping=False #So when player initialized it won't start jumping/to make the variable
        self.launched=False #So when player initialized it is not launched yet
        self.hp=PLAYER_HP #Gives player health when initialized
        self.last_hit=0 #Cooldown to prevent hit lasting forever,depleting the sprites hp.
        print('player instantiated')
        print(self.pos)
        # self.vx, self.vy=0,0
        # self.x=x*TILESIZE
        # self.y=y*TILESIZE
    
    #Reads keyboard input and results in movement (which my game specifically does not need...for the movement part at least)
    def get_keys(self):
        #reset v to zero
        #Listen for events specific to keys
        #change velocity based on which key is
        # self.vel=vec(0,0) 
        # self.x, self.vy=0,0
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]: #Clicking a goes left
            self.acc.x=-PLAYER_SPEED
            # self.vel.x=-PLAYER_SPEED
            # self.vx=-PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:#Clicking d goes right
            self.dir="right"
            self.acc.x=PLAYER_SPEED
            # self.vel.x=PLAYER_SPEED
            # self.vx=PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:#Clicking w goes up/jumps
            self.jump()
            # self.acc.y=-PLAYER_SPEED
            # self.vel.y=-PLAYER_SPEED
            # self.vy=-PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:#Clicking s goes down
            self.acc.y=PLAYER_SPEED
            # self.vel.y=PLAYER_SPEED
            # self.vy=PLAYER_SPEED

        if keys[pg.K_SPACE]: #Clicking space jumps
            self.jump()


        #Check to see if player is moving diagonal
        if self.vel.x!=0 and self.vel.y!=0:
            self.vel*=0.7071
        #   self.vel.normalize()
        
        # if self.vx!=0 and self.vy!=0:
        #     self.vx*=0.7071
        #     self.vy*=0.7071

    #Adding a launch function to make aim (I asked Gemini how would I add aim in pygame that would launch the player
    # and it told me to get the direction from the player's mouse, calculate a launch vector, and apply physics on the player.
    #Originally the direction and vectors was wrong so it reccomended me to use normalize so it can keep a constant (shrinked) vector 
    #of 1. Then after I just adapted it to vec and self.pos)
    def launch(self, target_pos): 
        #Calculates direction from player to mouse
        if not self.launched:
            # Converts mouse (x, y) into a vector and points from player to mouse (Target-Start).
            #Originally was reserved and only target_pos but Mr.Cozort adviced me to reverse it and Ethan Dang adviced
            #me to treat the target_pos as coordinates so when converting them to vectors you can easily calculate the vector subtraction.
            aim_dir = (vec(target_pos[0], target_pos[1]) - self.pos).normalize() 

            #Avoids dividing by zero if mouse is on the position of the player
            if aim_dir.length()>0:
                print(aim_dir)#debugged aim_dir
                self.vel=aim_dir*PLAYER_LAUNCH_SPEED 
                self.launched=True

    #Giving the image animation (cycling)
    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames) #Updating frames from previous frame
            #Creates parements for rectangle on map when hit
            center = self.rect.center
            self.image = self.idle_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center=center
    #Position of spritesheet (spritesheet is incomplete right now so this is a place holder for player only)
    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                            ]
        
    #Gives player ability to jump on certain conditions (jump not needed for my game)
    def jump(self):
        #Can only jump if on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping: #Checks whether it should play sound when jumping and ready to jump.
            self.game.jump_sound.play()
            self.jumping =True
            self.vel.y =-PLAYER_JUMP


    def is_jumping(self): #Checks if it's jumping and if it collides so you don't double jump
        if self.vel.y > 0: 
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                self.jumping = False



    #Outputing the position of the player and updating the game
    def update(self):
        self.animate()
        # Ethan suggested removing this if block as he noticed it's already called somewhere else and I didn't realize that it was skipping
        # self.hit._rect updates and collisions ,fixing the aiming during class but now always the mob to collide with the player 
        # #before it launches... :)))
        # if not self.launched:
        #     self.rect.center=self.pos
        #     return

        # I asked Gemini for the Physics that the game ball vs ball uses of the player when in motion
        self.rect.center=self.pos
        self.pos+=self.vel
        self.hit_rect.centerx=self.pos.x

        #Made it similar to jump function but also uses timer class from utils and more specifically time from py game
        #to make sure the collision starts the dmg but goes on cooldown/stops the dmg on the last hit.
        mob_hits=pg.sprite.spritecollide(self, self.game.all_mobs, False, collide_hit_rect)
        if mob_hits:
            now=pg.time.get_ticks()
            if now-self.last_hit>500:
                self.last_hit=now
                #I plan to eventually change collision to projectile as it will just result in a draw ALL the time...unless I do it where it's
                #only the first one in the collision actually takes the dmg.
                self.hp-=COLLISION_DMG#The actual damage when collides
                mob_hits[0].hp-=COLLISION_DMG #Same for mob but mob_hits is a list so makes sense for it to be the first hit.
                mob_hits[0].vel*=-1 #Mob bounces backwards after collision like player
                self.game.pickup_snd.play()#Uses coin sound but can easily replace to make it sound like a collide sound or bonk or wtv.

            #Checks if player or mob is defeated
            if self.hp<=0:
                self.kill()
            if mob_hits[0].hp<=0:
                mob_hits[0].kill()



        #When collides with wall
        collide_with_walls(self, self.game.all_walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls,'y')
        self.rect.center = self.hit_rect.center

        # Collisions with mob (Checks collision using wall collision method).
        self.hit_rect.centerx=self.pos.x
        collide_with_walls(self, self.game.all_mobs,'x')
        self.hit_rect.centery=self.pos.y
        collide_with_walls(self, self.game.all_mobs,'y')
        self.rect.center=self.hit_rect.center

        

           
        #Non of these utilities are needed so we won't call their functions
        # self.is_jumping()
        # self.acc=vec(0,PLAYER_GRAV)#Gravity
        # self.get_keys()#Process the clicked key
        # self.acc.x+=self.vel.x*PLAYER_FRIC
        # self.acc.y+=self.vel.y*self.cofric
        # self.rect.center=self.pos
        # self.pos+=self.vel+0.5*self.acc
        # self.vel+=self.acc
        # hits=pg.sprite.spritecollide(self,self.game.all_coins,True)
        # if hits:
        #     for i in range(100): # Run a loop 100 times to generate multiple particles once a coin is hit.
        #         Particle(self.game, hits[0].x, hits[0].y)
        #     self.coins += 1
        #     #Sound will play when coin is hit
        #     self.game.pickup_snd.play()
        #     self.game.score += 1
        # # self.pos+=self.vel*self.game.dt
        # self.hit_rect.centerx=self.pos.x
        # collide_with_walls(self,self.game.all_walls,'x')
        # self.hit_rect.centery=self.pos.y
        # if collide_with_walls(self,self.game.all_walls,'y'):
        #     self.jumping=False# to make sure to update whether you can jump or not.
        #     # self.rect.center=self.hit_rect.center
        


#Making a wall class to call in main.py to make the wall.
class Wall(Sprite):
    def __init__(self,game,x,y):
            self.groups=game.all_sprites, game.all_walls
            Sprite.__init__(self, self.groups)
            self.game=game
            self.image=pg.Surface((TILESIZE,TILESIZE))
            self.image.fill(BLUE)
            self.rect=self.image.get_rect()
            self.vx, self.vy=0,0
            self.x=x*TILESIZE
            self.y=y*TILESIZE
            self.rect.x=self.x
            self.rect.y=self.y
            # print("wall initialized")
            # print(self.rect.x)
            # print(self.rect.y)
# Making a particle class to call in main.py to make the particles.
class Particle(Sprite):
    def __init__(self,game,x,y):
            self.groups=game.all_sprites, game.all_particles #Makes a sprite group for particles
            Sprite.__init__(self, self.groups)
            self.game=game
            #Scales the particles by dividing it by 8 and filling it with a white color.
            self.image=pg.Surface((TILESIZE/8,TILESIZE/8))
            self.image.fill(WHITE)
            self.rect=self.image.get_rect()
            self.vel=vec(randint(-180,180),randint(-180,180))#Gives randomized vector
            self.pos=vec(x,y)
            #Sets particle speed randomly
            self.speed=randint(-5,10)
            if self.speed==0:
                self.speed=2
            #A cooldown timer that ticks when the particle is generated
            self.countdown=Timer()
            self.countdown.event_time=floor(pg.time.get_ticks()/1000)
            print(self.rect.x)
            print(self.rect.y)
            print(str(len(self.game.all_particles)))
    # Checks whether after a certain amount of time it will kill the particle and so it scatters around.
    def update(self):
        # self.countdown.ticking()
        self.pos+=self.vel*self.speed*self.game.dt
        self.rect.center = self.pos
        # self.rect.x+=self.speed*randint(-5,5)
        # self.rect.y+=self.speed*randint(-5,5)
        #If countdown is bigger than giving time one initiated then it kills the particle.
        if self.countdown.get_delta()>0.5:
            self.kill()
            print("NOOO:(")

#Making a coin class since why not:
class Coin(Sprite):
     #Making a Coin class to input a coin sprite when called in main.py
     def __init__(self, game, x, y):
        #Making the coin group
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #The shape of the coin itself and color
        pg.draw.circle(self.image, (YELLOW), (16, 16), 16)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        print(self.rect.x)
        print(self.rect.y)
#Making a Mob class to input a mob sprite when called in main.py
class Mob(Sprite):
    def __init__(self,game,x,y):
            self.groups=game.all_sprites, game.all_mobs #Sprite group for mob
            Sprite.__init__(self, self.groups)
            self.game=game
            #Inputs the images for the mob
            self.evilcat=Spritesheet(path.join(self.game.img_dir,"evilcat.png"))
            self.cutycat=Spritesheet(path.join(self.game.img_dir,"cutycat.jpg"))
            self.last_update=0
            self.current_frame=0
            self.load_images() #To load images, literally
            self.image=pg.Surface((TILESIZE,TILESIZE))
            self.image.fill(RED)
            self.rect=self.image.get_rect()
            #Speed, position, and direction of the mob and enviroments that effect the mob
            self.speed=1
            self.vx, self.vy=500,0
            self.x=x*TILESIZE
            self.y=y*TILESIZE
            self.rect.x=self.x
            self.rect.y=self.y
            self.speed = 100
            self.vel = vec(MOB_LAUNCH_SPEED,0).rotate(randint(0,360)) #So the direction is random at 360 degrees unless I make it so it's multiplayer
            self.pos = vec(x*TILESIZE,y*TILESIZE)
            self.x = x*TILESIZE
            self.y = y*TILESIZE
            self.rect.x = self.x
            self.rect.y = self.y
            self.coins=0
            self.pos=vec(x*TILESIZE,y*TILESIZE)
            self.dir = "none"
            self.last_update = 0
            self.current_frame = 0
            self.hit_rect = MOB_HIT_RECT #Mob collides with walls
            self.hp=MOB_HP #Gives mob health when initialized
            print("mob initialized")
            print(self.rect.x)
            print(self.rect.y)
    #Cycles mob animation frames (to animate the mob basically)
    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames) #Updating frames from previous frame
            bottom = self.rect.bottom
            self.image = self.idle_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            
    #Gets the animations from the spritesheet (which is incomplete right now so these are place holders for the mob)
    def load_images(self):
        self.idle_frames = [self.evilcat.get_image(0,0,TILESIZE, TILESIZE), #Defines spritesheet
                            self.evilcat.get_image(TILESIZE,0,TILESIZE, TILESIZE) #Defines spritesheet
                            ]
        self.run_frames= [self.cutycat.get_image(0,0,TILESIZE, TILESIZE), #Defines spritesheet
                          self.cutycat.get_image(TILESIZE,0,TILESIZE,TILESIZE) #Defines spritesheet
                          ]
    # uses autocomplete by creating a chase method using pos vectors and obj as a parameter
    def chase(self, obj): 
        if self.pos.x < obj.pos.x:
            self.vel.x = self.speed
            self.dir = "right"
        elif self.pos.x > obj.pos.x:
            self.vel.x = -self.speed
            self.dir = "left"
        else:
            self.vel.x = 0
        if self.pos.y < obj.pos.y:
            self.vel.y = self.speed
        elif self.pos.y > obj.pos.y:
            self.vel.y = -self.speed
        else:
            self.vel.y = 0

    #Updating velocity
    def update(self):
        #Thanks pygame for the .right
        # if self.rect.right>WIDTH or self.rect.x<0:
        #      self.speed*=-1
        #      self.y+=TILESIZE
        #Animation
        # self.x+=self.vx*self.game.dt*self.speed
        # self.rect.x=self.x
        # self.rect.y=self.y
        self.animate()
        #Mob waits until player is ready...or at least when it's initialized which is fine for now
        if not self.game.player:
            self.rect.center=self.pos
            return
        # self.chase(self.game.player) #Chase is not needed anymore so no need to call it.
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center
            
        

         
    

            
    
    