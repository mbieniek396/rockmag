import pygame
import settings as s

class Player:
    def __init__(self):
        ## Position and size
        self.w = 40
        self.h = 80
        self.x = 300
        self.base_y = 520-self.h
        self.y = self.base_y

        # Health
        self.hp = 3

        # Movement
        self.maxJump = 20
        self.jumping = False
        self.jumpSpeed = self.maxJump
        self.gravity = 1
        
        # Bullets
        self.bullets = []

        # Sprite
        self.idle = pygame.image.load('./assets/character/character.png').convert_alpha()
        self.idle = pygame.transform.scale(self.idle, (self.w, self.h))

        self.sprite = self.idle

        #Jumping sprite
        self.jump_sprite = pygame.image.load('./assets/character/Jump.png').convert_alpha()
        self.jump_sprite = pygame.transform.scale(self.jump_sprite, (self.w, self.h))

        # Running sprite
        self.running = []
        self.running_frame = 0
        for i in range(1, 9):
            temp = pygame.image.load(f"./assets/character/Run{i}.png").convert_alpha()
            temp = pygame.transform.scale(temp, (self.w, self.h))
            self.running.append(temp)

    def hitbox(self):
        ## Return rectangle as player hitbox
        return pygame.Rect(self.x, self.y, self.w, self.h)
        
    def animate(self):
        ## Anmite through running animation if on the floor level(not jumping)
        if self.y == self.base_y:
            self.running_frame+=0.15
            if self.running_frame > 7:
                self.running_frame = 0
            self.sprite = self.running[int(self.running_frame)]

    def jump(self):
        ## Jumping
        if self.jumping:
            self.y -= self.jumpSpeed
            self.jumpSpeed -= self.gravity
            if self.jumpSpeed < -self.maxJump:
                self.jumping = False
                self.sprite = self.idle
                self.jumpSpeed = self.maxJump

class Bullet:
    def __init__(self, x, y):
        self.w = 40
        self.h = 40
        self.x = x
        self.y = y
        self.speed = 5

        self.sprite = pygame.image.load('./assets/bullet.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.w, self.h))

    def hitbox(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Rock:
    def __init__(self):
        self.w = 80
        self.h = 70
        self.x = s.SCREEN_WIDTH *1.2
        self.y = 520-self.h

        self.sprite = pygame.image.load('./assets/rocks/cave_rock2.png')
        self.sprite = pygame.transform.scale(self.sprite, (self.w, self.h))

    def hitbox(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

        



class Crystal:
    def __init__(self):
        self.w = 150
        self.h = 200
        self.x = s.SCREEN_WIDTH *1.2
        self.y = 520-self.h

        self.sprite = pygame.image.load('./assets/crystals/blue.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.w, self.h))

    def hitbox(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)
    

class Option:
    def __init__(self, text, option):
        self.w = text.get_width()
        self.h = text.get_height()
        self.x = s.SCREEN_WIDTH/2-self.w/2
        self.y = 100

        self.enabled = True
        
        self.text = text
        self.option = option

    def hitbox(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)
    
pygame.font.init()

class Key_option:
    def __init__(self, option, key):
        self.key = key
        self.MEDIUM_FONT = pygame.font.SysFont('comicsans', 50)      
        self.text = self.MEDIUM_FONT.render(f"{option} key: {self.getKey()}", 1, s.BLUE)
        self.option = option
        

        self.w = self.text.get_width()
        self.h = self.text.get_height()
        self.x = s.SCREEN_WIDTH/2-self.w/2
        self.y = 100

    def show_press_message(self):
        self.text = self.MEDIUM_FONT.render(f"Press any key to change {self.option} key", 1, s.BLUE)
        self.w = self.text.get_width()
        self.x = s.SCREEN_WIDTH/2-self.w/2

    def show_normal(self):
        self.text = self.MEDIUM_FONT.render(f"{self.option} key: {self.getKey()}", 1, s.BLUE)
        self.w = self.text.get_width()
        self.x = s.SCREEN_WIDTH/2-self.w/2

    def getKey(self):
        return pygame.key.name(self.key) if pygame.key.name(self.key) != "return" else "enter"

    def hitbox(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    