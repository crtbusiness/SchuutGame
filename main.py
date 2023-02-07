import re
from numpy import true_divide
import pygame
from screeninfo import get_monitors
import os

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

FPS = 60
VEL = 5 #Velocity for spaceship to move
BULLET_VEL = 7
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1 #Creates custom user event
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('SchuutGame/Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)    
#Rotates by x degrees, Resizes an image to (x,y) pixels

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('SchuutGame/Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("First Game!")        #Sets the window name

def draw_window(red, yellow, red_bullets, yellow_bullets):
    WIN.fill(WHITE)     #Sets the background color of the window, uses RGB
    pygame.draw.rect(WIN, BLACK, BORDER)
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

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): #Checks if the bullet rectangle collides with the yellow rectangle object
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)


def main():
    red = pygame.Rect(WINDOW_WIDTH*3/4, WINDOW_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(WINDOW_WIDTH*1/4, WINDOW_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while(run):
        clock.tick(FPS)     #Caps framerate, caps how fast this while loop is allowed to run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False         #If the user closes the window, the service stops itself
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: #Checks if there are less than max bullets from yellow on screen
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5) #Spawns the bullet at the barrel of the ship
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed() #gets all keys that are pressed down
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets)
    
    
    pygame.quit()

if __name__ == "__main__":
    main()



#https://www.youtube.com/watch?v=jO6qQDNa2UY