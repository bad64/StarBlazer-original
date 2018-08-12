import pygame, os, _thread
from pygame.locals import *
from Engine import *

pygame.init()

if fullscreen == 1:
    pygame.mouse.set_visible(False)

debug = True
main = True

while main:

    if Engine.state == "Title":
        TitleLoop(Engine.HiScoresOnTitle)
    elif Engine.state == "PreMission":
        PreMissionLoop()
    elif Engine.state == "Game":
        GameLoop()
    elif Engine.state == "Boss":
        Boss()
    elif Engine.state == "NameReg":
        NameRegLoop()

    elif Engine.state == "Quit":
        main = False

    _thread.start_new_thread(Engine.CollisionDetection, (Engine.frame, Engine.StageLayer, Engine.stage))
    
pygame.quit()
