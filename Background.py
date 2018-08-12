import pygame, os, configparser
from pygame.locals import *
from random import randint

cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.getcwd(), "config.ini"))

width = int(cfg["VIDEO"]["width"])
height = int(cfg["VIDEO"]["height"])
fullscreen = int(cfg["VIDEO"]["fullscreen"])
framerate = 60
volume = float(cfg["AUDIO"]["MasterVolume"])

#Couleurs
BLACK = (0,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255,0,0)
DARKGREEN = (0,122,0)
SKYBLUE = (0, 200, 200)

if fullscreen == True:
    videoflags = HWSURFACE|DOUBLEBUF|FULLSCREEN
elif fullscreen == False:
    videoflags = HWSURFACE|DOUBLEBUF

screen = pygame.display.set_mode((width, height), videoflags)
pygame.display.set_caption("Star Blazer")
screenRect = screen.get_rect()

bgLayer = pygame.Surface((width, 15))
pygame.draw.rect(bgLayer, SKYBLUE, (0,0,width,3))
pygame.draw.rect(bgLayer, SKYBLUE, (0,5,width,3))
pygame.draw.rect(bgLayer, SKYBLUE, (0,10,width,3))
bgLayerRect = bgLayer.get_rect()
bgLayerRect.left = 0
bgLayerRect.top = (height * 8/10) + 49

class Star:
    def __init__(self, x, y):
        self.surface = pygame.Surface((5,5))
        self.surface.fill(WHITE)
        self.x = x
        self.y = y

StarsBG = []

for i in range(0, 200):
    StarsBG.append(Star((7 * i), randint(5, bgLayerRect.top - 15)))
    
def BackgroundLayerRender():
    screen.fill(BLACK)
    screen.blit(bgLayer, bgLayerRect.topleft)
    for i in range(200):
        screen.blit(StarsBG[i].surface, (StarsBG[i].x, StarsBG[i].y))
        StarsBG[i].x -= 3
        if StarsBG[i].x <= -10:
            StarsBG[i].x = width + 1
    bgLayerRect.left = 0
    
