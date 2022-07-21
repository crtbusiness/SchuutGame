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


WIDTH = getWidth()/2
HEIGHT = getHeight()/2
#print(WIDTH, HEIGHT)

WHITE = (255, 255, 255)

FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)    
#Rotates by x degrees, Resizes an image to (x,y) pixels

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")        #Sets the window name

def draw_window():
    WIN.fill(WHITE)     #Sets the background color of the window, uses RGB
    WIN.blit(YELLOW_SPACESHIP, (WIDTH*1/4, HEIGHT/2))       #Places image above the background layer at (x,y) coordinates
    WIN.blit(RED_SPACESHIP, (WIDTH*3/4, HEIGHT/2))
    pygame.display.update()     #Updates display with new changes, ex. changing background color


def main():
    clock = pygame.time.Clock()
    run = True
    while(run):
        clock.tick(FPS)     #Caps framerate, caps how fast this while loop is allowed to run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False         #If the user closes the window, the service stops itself
        draw_window()
    
    
    pygame.quit()

if __name__ == "__main__":
    main()
