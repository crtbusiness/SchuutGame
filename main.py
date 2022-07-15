import re
from numpy import true_divide
import pygame
from screeninfo import get_monitors

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
print(WIDTH, HEIGHT)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    run = True
    while(run):
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False         #If the user closes the window, the service stops itself
