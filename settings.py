import pygame

# COLORS
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0, 255, 0)

# FPS
FPS = 60

# Delay of spawining rocks/crystals
DELAY_TIME = 60

# SIZES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FLOOR_HEIGHT = 100

CLOUDS_WIDTH = 500


### BULLETS COUNT
BULLETS = 3

### SHOW HOW MANY SCORES
SCORE_COUNT = 5


#### MENU OPTIONS
menu = True

rules = False

can_move = False

about = False

settings = False

ranking = False

### volume
volume = True

### keys change
shot = False
jump = False

JUMP_KEY = pygame.K_SPACE
SHOT_KEY = pygame.K_RETURN



# PLAYER  and SCORE
player = None
score = 0

# SPEED OF Background movement
SPEED_BOOST = 0
scroll = [0, 0, 0, 0, 0]

## Rocks and crystals
rocks = []
crystals = []


### Game states (start, lost, playing(default without variable))
lost = False
start = True
