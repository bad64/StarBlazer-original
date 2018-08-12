import pygame, os
from pygame.locals import *
from Entities import *

pygame.init()

HUDElementsList = []
globalfont = pygame.font.Font(os.path.join(os.getcwd(), "resources", "menu", "ARCADECLASSIC.TTF"), 36)

class HUDElement:
    def __init__(self, thingtype, value):
        self.value = value
        self.thingtype = thingtype
        if thingtype == 'score':
            self.surface = globalfont.render(self.value, True, DARKGREEN)
            self.Rect = self.surface.get_rect()
            self.Rect.topleft = ((5,5))
        elif thingtype == 'scoreint':
            self.surface = globalfont.render('%06d' % self.value, True, WHITE)
            self.Rect = self.surface.get_rect()
        elif thingtype == 'fuel':
            self.surface = globalfont.render(self.value, True, DARKGREEN)
            self.Rect = self.surface.get_rect()
        elif thingtype == 'fuelint':
            self.surface = globalfont.render('%06d' % self.value, True, WHITE)
            self.Rect = self.surface.get_rect()
        elif thingtype == 'bomb':
            self.surface = globalfont.render(self.value, True, DARKGREEN)
            self.Rect = self.surface.get_rect()
        elif thingtype == 'bombint':
            self.surface = globalfont.render('%02d' % self.value, True, WHITE)
            self.Rect = self.surface.get_rect()
        elif thingtype == 'mission':
            self.surface = globalfont.render(self.value, True, DARKGREEN)
            self.Rect = self.surface.get_rect()
            self.Rect.bottomleft = (5, height -5)
        elif thingtype == 'missionint':
            self.surface = globalfont.render('%02d' % self.value, True, WHITE)
            self.Rect = self.surface.get_rect()
        elif thingtype == 'secret':
            self.surface = globalfont.render(self.value, True, DARKGREEN)
            self.Rect = self.surface.get_rect()
            self.Rect.left = 50
            self.Rect.bottom = height - 53

def HUDLayerRender(stagenumber, debug):
    HUDElementsList = []
    HUDElementsList.append(HUDElement('score', "SCORE"))
    HUDElementsList.append(HUDElement('scoreint', Player.score))
    HUDElementsList.append(HUDElement('fuel', "FUEL"))
    HUDElementsList.append(HUDElement('fuelint', Player.fuel))
    HUDElementsList.append(HUDElement('bomb', "BOMBS"))
    HUDElementsList.append(HUDElement('bombint', Player.bombs))
    HUDElementsList.append(HUDElement('mission', "MISSION"))
    HUDElementsList.append(HUDElement('missionint', stagenumber))

    for i in range(len(HUDElementsList)):
        #HUDElementsList[i].surface = pygame.transform.scale(HUDElementsList[i].surface, (int(width/len(HUDElementsList)), 50))
        #HUDElementsList[i].Rect = HUDElementsList[i].surface.get_rect()
        if i > 0 and i != 6:
            HUDElementsList[i].Rect.topleft = HUDElementsList[i-1].Rect.topright
        screen.blit(HUDElementsList[i].surface, HUDElementsList[i].Rect)

    if debug == False:
        lives = globalfont.render("1UP " + str('%02d' % Player.lives), True, WHITE)
        livesRect = lives.get_rect()
        livesRect.top = 5
        livesRect.right = width
        screen.blit(lives, livesRect.topleft)


class LIFE:
    def __init__(self, hitpoints):
        self.type = "lifebar"
        self.surface = pygame.Surface((66, 11))
        self.surface.set_colorkey(BLACK)
        
        for i in range(hitpoints):
            pygame.draw.line(self.surface, RED, (i+1, 1), (i+1, 10))
        pygame.draw.rect(self.surface, WHITE, (0,0,66,11), 1)
        
        self.surface = pygame.transform.scale(self.surface, (width - 100, 30))
        self.Rect = self.surface.get_rect()
        self.Rect.centerx = int(width/2)
        self.Rect.bottom = height - 30

def SpecialHUDLayerRender(debug):
    HUDElementsList = []
    HUDElementsList.append(HUDElement('score', "SCORE"))
    HUDElementsList.append(HUDElement('scoreint', Player.score))
    HUDElementsList.append(HUDElement('fuel', "FUEL"))
    HUDElementsList.append(HUDElement('fuelint', Player.fuel))
    HUDElementsList.append(HUDElement('bomb', "BOMBS"))
    HUDElementsList.append(HUDElement('bombint', Player.bombs))
    try:
        HUDElementsList.append(LIFE(Enemies[0].hitpoints))
    except:
        pass
    HUDElementsList.append(HUDElement('secret', "BOSS"))

    for i in range(len(HUDElementsList)):
        #HUDElementsList[i].surface = pygame.transform.scale(HUDElementsList[i].surface, (int(width/len(HUDElementsList)), 50))
        #HUDElementsList[i].Rect = HUDElementsList[i].surface.get_rect()
        if i > 0 and i < 6:
            HUDElementsList[i].Rect.topleft = HUDElementsList[i-1].Rect.topright
        screen.blit(HUDElementsList[i].surface, HUDElementsList[i].Rect)

    if debug == False:
        lives = globalfont.render("1UP " + str('%02d' % Player.lives), True, WHITE)
        livesRect = lives.get_rect()
        livesRect.top = 5
        livesRect.right = width
        screen.blit(lives, livesRect.topleft)
