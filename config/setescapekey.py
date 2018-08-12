import pygame, os, configparser
from pygame.locals import *

pygame.init()

cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.getcwd(), "..", "config.ini"))

screen = pygame.display.set_mode((100, 1))

main = True

while main:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    buttons = joystick.get_numbuttons()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            main = False
        if event.type == JOYBUTTONDOWN:
            for i in range(buttons):
                if joystick.get_button(i) == True:
                    cfg.set('JOYSTICK', 'j_escape', str(i))
                    main = False

with open(os.path.join(os.getcwd(), "..", "config.ini"), "w") as configfile:
    cfg.write(configfile)
    
pygame.quit()
