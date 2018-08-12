import pygame, os
from Entities import *

pygame.init()

globalfont = pygame.font.Font(os.path.join(os.getcwd(), "resources", "menu", "ARCADECLASSIC.TTF"), 36)

RED = ((255,0,0))
GREEN = ((0,255,0))
BLUE = ((0,0,255))
PINK = ((255,0,255))

class DebugHitbox:
    def __init__(self, width, height, color):
        self.sprite = pygame.Surface((width, height))
        self.sprite.fill(color)
        self.sprite.set_alpha(100)
        self.rect = self.sprite.get_rect()


def DisplayDebugInfo(frame, controls, StageLayer):
    Controlstate = globalfont.render(str(controls), True, DARKGREEN)
    ControlstateRect = Controlstate.get_rect()
    ControlstateRect.right = width
    screen.blit(Controlstate, ControlstateRect.topleft)

    Framestate = globalfont.render(str(frame), True, WHITE)
    FramestateRect = Controlstate.get_rect()
    FramestateRect.top = ControlstateRect.bottom + 2
    FramestateRect.right = width
    screen.blit(Framestate, FramestateRect.topleft)

    for i in range(len(StageLayer)):
        if StageLayer[i].name != "Empty" and StageLayer[i].name != "cactus":
            screen.blit(DebugHitbox(StageLayer[i].width, StageLayer[i].height, RED).sprite, StageLayer[i].rect.topleft)
        else: pass

    for i in range(len(Enemies)):
        screen.blit(DebugHitbox(Enemies[i].width, Enemies[i].height, BLUE).sprite, (Enemies[i].rect.left + 5, Enemies[i].rect.top))

    for i in range(len(Objectives)):
        screen.blit(DebugHitbox(Objectives[i].width, Objectives[i].height, BLUE).sprite, Objectives[i].rect.topleft)

    for i in range(len(Bombs)):
        screen.blit(DebugHitbox(Bombs[i].width, Bombs[i].height, GREEN).sprite, (Bombs[i].rect.left, Bombs[i].rect.top - 2))
        
    try:
        screen.blit(DebugHitbox(Player.rect.width, Player.rect.height, PINK).sprite, (Player.rect.left, Player.rect.top))
        screen.blit(DebugHitbox(Player.hitbox.width, Player.hitbox.height, GREEN).sprite, (Player.hitbox.left, Player.hitbox.top))
    except:
        pass
