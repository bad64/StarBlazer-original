import pygame, os
from Background import *

class StageElement:
    def __init__(self, name):
        self.name = name
        self.IsObjective = False
        self.sprite = pygame.image.load(os.path.join(os.getcwd(), "resources", name + ".png"))
        self.rect = self.sprite.get_rect()
        self.rect.bottom = bgLayerRect.top
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top
        self.hitpoints = 3

class EmptyStageElement:
    def __init__(self):
        self.name = "Empty"
        self.IsObjective = False
        self.sprite = pygame.Surface((50,50))
        self.sprite.set_colorkey((0,0,0))
        self.rect = self.sprite.get_rect()
        self.rect.bottom = bgLayerRect.top
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top

class StageObjective:
    def __init__(self, name, hitpoints):
        self.name = name
        self.IsObjective = True
        self.sprite = pygame.image.load(os.path.join(os.getcwd(), "resources", name + ".png"))
        self.rect = self.sprite.get_rect()
        self.rect.bottom = bgLayerRect.top
        self.hitpoints = hitpoints
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top
    
global Objectives
Objectives = []
formattedlevel = []

def ComposeStageLayer(stagenumber):
    stagenumber = str(stagenumber)
    formattedlevel = []
    Objectives = []
    level = open((os.path.join(os.getcwd(), "data", "level"+ stagenumber +".dat")), 'r')
    
    while True:
        buffer = level.read(1)

        if buffer == "0":
            formattedlevel.append(EmptyStageElement())
        elif buffer == "1":
            formattedlevel.append(StageElement("tree"))
        elif buffer == "2":
            formattedlevel.append(StageElement("antenna"))
        elif buffer == "3":
            formattedlevel.append(StageElement("cactus"))
        elif buffer =="4":
            formattedlevel.append(StageObjective("radar", 3))
        elif buffer == "5":
            formattedlevel.append(StageObjective("icbm", 6))
        elif buffer == "6":
            formattedlevel.append(StageObjective("hquarters", 12))
        
        if not buffer: break

    return formattedlevel

def RenderStageLayer(level):
    for i in range(len(level)):
        if level[i].rect.left <= width or level[i].rect.right >= 0:
            if i == 0:
                level[0].rect.left -= 10
                screen.blit(level[0].sprite, level[0].rect.topleft)
            else:
                level[i].rect.left = level[i-1].rect.right
                screen.blit(level[i].sprite, level[i].rect.topleft)
        else:
            if i == 0:
                level[i].rect.left -= 10
            else:
                level[i].rect.left = level[i-1].rect.right

    if level[0].rect.right <= 0:
        level.append(level[0])
        level.pop(0)
