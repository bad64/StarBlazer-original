import pygame, os, configparser
from pygame.locals import *

pygame.init()

cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.getcwd(), "config.ini"))

def MapControls(ctrl):
    buffer = str(cfg["CONTROLS"][ctrl])
    keys = pygame.key.get_pressed()

    for i in range(len(keys)):
        if buffer == pygame.key.name(i):
            ctrl = int(i)
            return ctrl

def JoyMapControls(joystick, buttons, ctrl):
    buffer = int(cfg["JOYSTICK"][ctrl])
    return buffer

controls_up = MapControls("up")
controls_down = MapControls("down")
controls_left = MapControls("left")
controls_right = MapControls("right")
controls_shoot = MapControls("shoot")

try:
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    buttons = joystick.get_numbuttons()

    jcontrols_escape = JoyMapControls(joystick, buttons, "j_escape")
    
except:
    jcontrols_escape = None
