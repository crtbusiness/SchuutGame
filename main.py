import re
from numpy import true_divide
import pygame
from screeninfo import get_monitors
import os
pygame.font.init()
pygame.mixer.init()

# for m in get_monitors():
#     print(str(m) + "\n")

print(str(get_monitors()))

def getWidth():
    splits = str(get_monitors()).split() #splits the get_monitors() list into an array
    # for split in splits:
    #     print(split)
    toInt = re.findall(r'\b\d+\b', splits[2]) #Use regex to grab the number from array element width=####
    toInt = str(toInt[0]) #converts toInt from a list of one element to a string
    #print(toInt)
    return int(toInt) #convert toInt string to an int

def getHeight():
    splits = str(get_monitors()).split() #splits the get_monitors() list into an array
    # for split in splits:
    #     print(split)
    toInt = re.findall(r'\b\d+\b', splits[3]) #Use regex to grab the number from array element height=####
    toInt = str(toInt[0]) #converts toInt from a list of one element to a string
    #print(toInt)
    return int(toInt) #convert toInt string to an int


WINDOW_WIDTH = getWidth()/2
WINDOW_HEIGHT = getHeight()/2
#print(WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WINDOW_WIDTH//2 - 5, 0, 10, WINDOW_HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5 #Velocity for spaceship to move
BULLET_VEL = 7
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1 #Creates custom user event
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)    
#Rotates by x degrees, Resizes an image to (x,y) pixels

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("First Game!")        #Sets the window name

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    #WIN.fill(WHITE)     #Sets the background color of the window, uses RGB ------ DEPRECATED
    WIN.blit(SPACE, (0,0)) #Sets background to the space image
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE) #The 1 is for antialiasing, just use 1
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WINDOW_WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))       #Places image above the background layer at (x,y) coordinates
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()     #Updates display with new changes, ex. changing background color

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT player yellow, checks if pressing key would send spaceship offscreen
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT player yellow, checks if the right corner of spaceship tries to cross center border
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP player yellow
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < WINDOW_HEIGHT - 15: #DOWN player yellow
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT player red
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WINDOW_WIDTH: #RIGHT player red
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP player red
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < WINDOW_HEIGHT - 15: #DOWN player red
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): #Checks if the bullet rectangle collides with the red rectangle object
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WINDOW_WIDTH:
            yellow_bullets.remove(bullet) #Removes bullet if it goes off screen

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): #Checks if the bullet rectangle collides with the yellow rectangle object
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2, 
                        WINDOW_HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(WINDOW_WIDTH*3/4, WINDOW_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(WINDOW_WIDTH*1/4, WINDOW_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while(run):
        clock.tick(FPS)     #Caps framerate, caps how fast this while loop is allowed to run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False         #If the user closes the window, the service stops itself
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: #Checks if there are less than max bullets from yellow on screen
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5) #Spawns the bullet at the barrel of the ship
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed() #gets all keys that are pressed down
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    
    #pygame.quit() #Use this if you want the game to exit when someone wins, we're not using this because we are going to restart the match
    main()

if __name__ == "__main__":
    main()



#https://www.youtube.com/watch?v=jO6qQDNa2UY