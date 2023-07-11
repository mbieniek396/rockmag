import pygame
import settings as s

class Assets:

    def __init__(self):
        path = "./assets/"
        self.bg = pygame.image.load(path+'Background/1.png').convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (s.SCREEN_WIDTH,600))

        self.primaryMountain = pygame.image.load(path+'Background/5.png').convert_alpha()
        self.primaryMountain = pygame.transform.scale(self.primaryMountain, (s.SCREEN_WIDTH,600))
        
        self.secondaryMountain = pygame.image.load(path+'Background/4.png').convert_alpha()
        self.secondaryMountain = pygame.transform.scale(self.secondaryMountain, (s.SCREEN_WIDTH,600))
        
        self.bgMountains = pygame.image.load(path+'Background/2.png').convert_alpha()
        self.bgMountains = pygame.transform.scale(self.bgMountains, (s.SCREEN_WIDTH,600))
        
        self.clouds = pygame.image.load(path+'Background/3.png').convert_alpha()
        self.clouds = pygame.transform.scale(self.clouds, (s.CLOUDS_WIDTH,200))


        self.floor = pygame.image.load(path+'floor.png').convert_alpha()
        self.floor = pygame.transform.scale(self.floor, (800, 100))

        self.heart = pygame.image.load(path+'heart.png').convert_alpha()
        self.heart = pygame.transform.scale(self.heart, (60, 60))
        
        