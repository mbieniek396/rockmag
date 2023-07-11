import pygame
import assets
import settings as s
import objects as o
import random
import json
import os

### FONT ###
### initialize fonts for text on screen
pygame.font.init()

## set fonts
LOST_FONT = pygame.font.SysFont('comicsans', 80)
LOST_LOWER_FONT = pygame.font.SysFont('comicsans', 40)

MEDIUM_FONT = pygame.font.SysFont('comicsans', 50)
LOW_FONT = pygame.font.SysFont('comicsans', 25)
MIDLOW_FONT = pygame.font.SysFont('comicsans', 30)

## Initialize mixer for music
pygame.mixer.init()

## load music
BG_MUSIC = pygame.mixer.Sound('./assets/music/bg_music.mp3')
BG_MUSIC.play(loops=-1)

JUMP_SOUND = pygame.mixer.Sound('./assets/music/jump.mp3')
DIE_SOUND = pygame.mixer.Sound('./assets/music/dead.mp3')
FIREBALL_SOUND = pygame.mixer.Sound('./assets/music/fireball.mp3')


### Setup screen display
screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
pygame.display.set_caption('Rock mag')

### load assets (background/floor grahpics)
assets = assets.Assets()


# Tiles (For background scrolling)
TILES = 2


### EVENTS
END_GAME = pygame.USEREVENT + 1


def prepare():
    ### initializing the playing state
    s.SPEED_BOOST = 0
    s.player = o.Player()
    s.score = 0
    s.can_move = True

def main():

    SM_X = 4+s.SPEED_BOOST
    C_X = 4+s.SPEED_BOOST
    PM_X = 5+s.SPEED_BOOST
    BGM_X = 2+s.SPEED_BOOST
    F_X = 6+s.SPEED_BOOST

    #### Load ranking ####
    ranking = []
    try:
        with open('ranking.json') as jf:
            ranking = json.load(jf)
    except:
        pass

    #### Menu options ####
    options = []
    doptions = []
    options.append(o.Option(MEDIUM_FONT.render("Back to menu", 1, s.BLUE), "back"))#0
    options.append(o.Option(MEDIUM_FONT.render("1. Play", 1, s.BLUE), "play"))#1
    options.append(o.Option(MEDIUM_FONT.render("2. Rules", 1, s.BLUE), "rules"))#2
    options.append(o.Option(MEDIUM_FONT.render("3. Settings", 1, s.BLUE), "settings"))#3
    options.append(o.Option(MEDIUM_FONT.render("4. Ranking", 1, s.BLUE), "ranking"))#4
    options.append(o.Option(MEDIUM_FONT.render("5. About", 1, s.BLUE), "about"))#5
    options.append(o.Option(MEDIUM_FONT.render("6. Exit", 1, s.BLUE), "exit"))#6

    options.append(o.Option(MEDIUM_FONT.render("Volume is On", 1, s.BLUE), "musicOff"))#7
    options.append(o.Option(MEDIUM_FONT.render("Volume is Off", 1, s.BLUE), "musicOn"))#8
    options[8].enabled = False


    doptions.append(o.Key_option("shot", s.SHOT_KEY))#0
    doptions.append(o.Key_option("jump", s.JUMP_KEY))#1

    run = True
    clock = pygame.time.Clock()
    
    ## Delay for rocks/crystal spawns
    delay = s.DELAY_TIME
    
    while run:
        clock.tick(s.FPS)
            
        #### EVENTS ######
        for event in pygame.event.get():
            if event.type == END_GAME:
                s.lost = True
                s.can_move = False
                ranking = save_score(ranking, os.getlogin())
                

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    handle_options(options, doptions, pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if s.jump:
                    doptions[1].key = event.key
                    s.jump = False
                    doptions[1].show_normal()
                if s.shot:
                    doptions[0].key = event.key
                    s.shot = False
                    doptions[0].show_normal()
                if event.key == doptions[0].key:
                    if s.lost or s.start:
                       pass
                    elif len(s.player.bullets) < s.BULLETS + s.SPEED_BOOST:
                        ### Shoot bullet(Fireball)
                        if s.volume:
                            FIREBALL_SOUND.play()
                        s.player.bullets.append(o.Bullet(s.player.x, s.player.y))
        
        if s.can_move:
            ### Animate player running
            s.player.animate()
            ### Spawn rocks of crystals
            delay-=1
            if delay == 0:
                delay = s.DELAY_TIME
                make_obstacle()
            ## Handle jump
            keys_pressed = pygame.key.get_pressed()
            handle_movement(keys_pressed, doptions[1])

            handle_bullets()

            handle_hits()

        draw(SM_X,C_X,PM_X,BGM_X, F_X, options, ranking, doptions)
        
    pygame.quit()


def handle_options(options, doptions, pos):

    if s.settings:
        for opt in doptions:
            if opt.hitbox().collidepoint(pos):
                if opt.option == "shot":
                    s.shot = True
                    s.jump = False
                    opt.show_press_message()
                    doptions[1].show_normal()
                    return
                elif opt.option == "jump":
                    s.jump = True
                    s.shot = False
                    opt.show_press_message()
                    doptions[0].show_normal()
                    return
    for option in options:
        if option.hitbox().collidepoint(pos):
            if s.menu:
                if option.option == "play":
                    ## Start playing state
                    s.start = False
                    s.lost = False
                    s.rocks = []
                    s.crystals = []
                    s.menu = False
                    prepare()
                    return
                elif option.option == "rules":
                    s.rules = True
                    s.menu = False
                    return
                elif option.option == "settings":
                    s.settings = True
                    s.menu = False
                    return
                elif option.option == "ranking":
                    s.ranking = True
                    s.menu = False
                    return
                elif option.option == "about":
                    s.about = True
                    s.menu = False
                    return
                elif option.option == "exit":
                    exit()
            elif option.option == "back" and not s.can_move:
                s.rules = False
                s.about = False
                s.ranking = False
                s.settings = False
                s.shot = False
                s.jump = False
                doptions[0].show_normal()
                doptions[1].show_normal()
                s.menu = True
                s.lost = False
                s.start = True
                return
            elif s.settings:
                if option.enabled and option.option == "musicOn" and not s.volume:
                    s.volume = True
                    s.shot = False
                    s.jump = False
                    doptions[0].show_normal()
                    doptions[1].show_normal()
                    BG_MUSIC.play(loops=-1)
                    option.enabled = False
                    options[7].enabled = True
                    return
                elif option.enabled and option.option == "musicOff":
                    s.volume = False
                    s.shot = False
                    s.jump = False
                    doptions[0].show_normal()
                    doptions[1].show_normal()
                    BG_MUSIC.stop()
                    option.enabled = False
                    options[8].enabled = True
                    return
                





def save_score(ranking, nick):
    if len(ranking) >= s.SCORE_COUNT:
        if ranking[-1]["score"] >= s.score:
            return ranking
        ranking.pop()
    ranking.append({"nick":nick, "score":s.score})

    ranking = sorted(ranking, key=lambda x: x["score"])
    ranking.reverse()

    with open('ranking.json', 'w') as jf:
        json.dump(ranking, jf)
    return ranking

def handle_hits():
    ### Check if player runs into rock or crystal

    for rock in s.rocks:
        if rock.hitbox().colliderect(s.player.hitbox()):
            s.rocks.remove(rock)
            if s.volume:
                DIE_SOUND.play()
            s.player.hp -= 1
            if s.player.hp == 0:
                return pygame.event.post(pygame.event.Event(END_GAME))

    for crystal in s.crystals:
        if crystal.hitbox().colliderect(s.player.hitbox()):
            s.crystals.remove(crystal)
            if s.volume:
                DIE_SOUND.play()
            s.player.hp -= 1
            if s.player.hp == 0:
                return pygame.event.post(pygame.event.Event(END_GAME))

def handle_bullets():
    ### Check if bullet destroys crystal, or if rock destroys the bullet

    for bullet in s.player.bullets:
        for crystal in s.crystals:
            if bullet.hitbox().colliderect(crystal.hitbox()):
                s.player.bullets.remove(bullet)
                s.crystals.remove(crystal)
                s.score+=1
                s.SPEED_BOOST = s.score//10
        for rock in s.rocks:
            if bullet.hitbox().colliderect(rock.hitbox()):
                s.player.bullets.remove(bullet)

def make_obstacle():
    ### Make a rock or crystal(random chance)

    if random.randint(0, max(5, 7-s.SPEED_BOOST)) < 4:
        if random.randint(0, 2) == 0:
            s.crystals.append(o.Crystal())
        else:
            s.rocks.append(o.Rock())

def drawBG(sheet, n, speed=2, w=s.SCREEN_WIDTH, h=-50):
    #### Draw the background part for paralax effect

    i = 0
    while(i < TILES):
        screen.blit(sheet, (w*i+ s.scroll[n], h))
        i += 1

    s.scroll[n] -= speed

    if abs(s.scroll[n]) > w:
        s.scroll[n] = 0

def handle_movement(keys_pressed, jump):
    ## Handle jump

    if keys_pressed[jump.key]:
        if not s.player.jumping:
            if s.volume:
                JUMP_SOUND.play()
            s.player.jumping = True
            s.player.sprite = s.player.jump_sprite
    
    s.player.jump()


def draw(SM_X,C_X,PM_X,BGM_X, F_X, options, ranking, doptions):
    ### Draw everything on the screen
    
    ### Draw background
    screen.blit(assets.bg, (0,-50))
    drawBG(assets.bgMountains, 3, BGM_X)
    drawBG(assets.secondaryMountain, 2, SM_X)
    drawBG(assets.primaryMountain, 0, PM_X)
    drawBG(assets.clouds, 1,C_X,h=10)
    # Draw floor
    drawBG(assets.floor, 4, F_X, h=s.SCREEN_HEIGHT-s.FLOOR_HEIGHT)

    if not s.start:
        if s.lost:
            s.player.x -= F_X
        screen.blit(s.player.sprite, (s.player.x, s.player.y))
  
        for bullet in s.player.bullets:
            if bullet.x > s.SCREEN_WIDTH *1.4:
                s.player.bullets.remove(bullet)
            bullet.x += bullet.speed+s.SPEED_BOOST
            screen.blit(bullet.sprite, (bullet.x, bullet.y))

    for rock in s.rocks:
        rock.x -= F_X
        screen.blit(rock.sprite, (rock.x, rock.y))
    for crystal in s.crystals:
        crystal.x -= F_X
        screen.blit(crystal.sprite, (crystal.x, crystal.y))
    
    if s.lost:
        lost_text = LOST_FONT.render("You lost!", 1, s.RED)
        screen.blit(lost_text, (s.SCREEN_WIDTH/2-lost_text.get_width()/2, s.SCREEN_HEIGHT/2-lost_text.get_height()/2))
        option = options[0]
        option.y = s.SCREEN_HEIGHT-option.h*2
        screen.blit(option.text, (option.x, option.y))
    elif s.start:
        # lost_text = MEDIUM_FONT.render("To start the game press enter...", 1, s.BLUE)
        # lost_lower_text = LOW_FONT.render("Use SPACE to jump over rocks, and ENTER to shoot blue crystals", 1, s.BLUE)
        # screen.blit(lost_text, (s.SCREEN_WIDTH/2-lost_text.get_width()/2, s.SCREEN_HEIGHT/2-lost_text.get_height()/2))
        # screen.blit(lost_lower_text, (s.SCREEN_WIDTH/2-lost_lower_text.get_width()/2, s.SCREEN_HEIGHT/2+lost_text.get_height()/2+lost_lower_text.get_height()))
        if s.rules:
            lost_lower_text = MIDLOW_FONT.render(f"Use {doptions[1].getKey()} to jump over rocks", 1, s.BLUE)
            x = 50
            d = lost_lower_text.get_height()+20
            y = s.SCREEN_HEIGHT/2-d
            screen.blit(lost_lower_text, (x, y))
            y+=d
            another = MIDLOW_FONT.render(f"Use {doptions[0].getKey()} to shoot firball and destroy crystals", 1, s.BLUE)
            screen.blit(another, (x, y))
        elif s.settings:
            if s.volume:
                on = options[7]
            else:
                on = options[8]
            on.y = on.h*2
            screen.blit(on.text, (on.x, on.y))
            for i, opt in enumerate(doptions):
                on = opt
                on.y = on.h*(4+i)
                screen.blit(on.text, (on.x, on.y))
        elif s.ranking:
            x = s.SCREEN_WIDTH/3
            y = s.SCREEN_HEIGHT/6
            d = s.SCREEN_HEIGHT/10
            for i, place in enumerate(ranking):
                another = MEDIUM_FONT.render(f"{place['nick']}", 1, s.GREEN)
                score = MEDIUM_FONT.render(f"{place['score']}", 1, s.GREEN)
                screen.blit(another, (x, y+d*i))
                screen.blit(score, (x+x, y+d*i))
        elif s.about:
            lost_lower_text = LOST_FONT.render("Author is Zosia Polak", 1, s.BLUE)
            x = s.SCREEN_WIDTH/2-lost_lower_text.get_width()/2
            d = lost_lower_text.get_height()+20
            y = s.SCREEN_HEIGHT/2-d
            screen.blit(lost_lower_text, (x, y))
        if s.menu:
            for i, option in enumerate(options):
                if option.option == "back" or option.option == "musicOn" or option.option == "musicOff":
                    continue
                option.y = option.h*i+10
                screen.blit(option.text, (option.x, option.y))
        else:
            option = options[0]
            option.y = s.SCREEN_HEIGHT-option.h*2
            screen.blit(option.text, (option.x, option.y))
    else:
        lost_text = LOST_FONT.render(str(s.player.hp), 1, s.WHITE)
        screen.blit(lost_text, (lost_text.get_width()/2, lost_text.get_height()/4))
        screen.blit(assets.heart, (lost_text.get_width()*1.7, lost_text.get_height()/2))
    if not s.start:
        lost_text = LOST_FONT.render(str(s.score), 1, s.BLUE)
        screen.blit(lost_text, (s.SCREEN_WIDTH/2-lost_text.get_width()/2, lost_text.get_height()/4))

    pygame.display.update()


if __name__ == "__main__":
    main()
