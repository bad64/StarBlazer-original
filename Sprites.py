import pygame, os
from Background import width, height

pygame.init()
globalfont = pygame.font.Font(os.path.join(os.getcwd(), "resources", "menu", "ARCADECLASSIC.TTF"), 36)
spritepath = os.path.join(os.getcwd(), "resources")

#Couleurs
BLACK = (0,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
GREY = (160,160,160)
RED = (255,0,0)
DARKGREEN = (0,122,0)
SKYBLUE = (0, 200, 200)
LIGHTBROWN = (165,125,80)
DARKBROWN = (95,60,20)

#Vide
EmptySprite = pygame.Surface((50,50))
EmptySprite.fill(BLACK)
EmptySprite.set_colorkey(BLACK)

#Balles
laser = pygame.Surface((50, 2))
laser.fill((255,255,255))

#Bombes
bomb = pygame.Surface((15, 5))
pygame.draw.line(bomb, WHITE, (5,0), (13, 0))
pygame.draw.line(bomb, WHITE, (4,1), (14, 1))
pygame.draw.line(bomb, WHITE, (3,2), (14, 2))
pygame.draw.line(bomb, WHITE, (4,3), (14, 3))
pygame.draw.line(bomb, WHITE, (5,4), (13, 4))
pygame.draw.line(bomb, WHITE, (4,2), (0,0))
pygame.draw.line(bomb, WHITE, (4,2), (0,2))
pygame.draw.line(bomb, WHITE, (4,2), (0,4))
bomb.set_colorkey(BLACK)

#Truc qui ressemble à un ballon météo
balloon = pygame.Surface((30,30))
pygame.draw.ellipse(balloon, SKYBLUE, (5,0,20,20))
pygame.draw.line(balloon, SKYBLUE, (15,15), (15,30))
balloon.set_colorkey(BLACK)


#Explosions
ExplosionFrame1 = pygame.image.load(os.path.join(spritepath, "ExplosionFrame1.png"))
ExplosionFrame2 = pygame.image.load(os.path.join(spritepath, "ExplosionFrame2.png"))

#Navion
plane = pygame.Surface((50,50))

#Drop de munitions (avec caisse)
PackageWithCrate = pygame.Surface((10,15))
pygame.draw.line(PackageWithCrate, WHITE, (3,0), (6,0))
pygame.draw.line(PackageWithCrate, WHITE, (2,1), (7,1))
pygame.draw.line(PackageWithCrate, WHITE, (1,2), (8,2))
pygame.draw.line(PackageWithCrate, WHITE, (0,3), (9,3))
pygame.draw.line(PackageWithCrate, WHITE, (0,4), (9,4))
pygame.draw.line(PackageWithCrate, WHITE, (0,4), (4,10))
pygame.draw.line(PackageWithCrate, WHITE, (3,4), (4,10))
pygame.draw.line(PackageWithCrate, WHITE, (6,4), (5,10))
pygame.draw.line(PackageWithCrate, WHITE, (9,4), (5,10))

pygame.draw.rect(PackageWithCrate, DARKGREEN, (0,10,10,5))
pygame.draw.line(PackageWithCrate, BLACK, (1,12), (8,12))

PackageWithCrate = pygame.transform.scale(PackageWithCrate, ((30,45)))
PackageWithCrate.set_colorkey(BLACK)

#Drop de munitions (sans caisse)
##Plus ou moins inutilisé
PackageWithoutCrate = pygame.Surface((10,15))
pygame.draw.line(PackageWithoutCrate, WHITE, (3,0), (6,0))
pygame.draw.line(PackageWithoutCrate, WHITE, (2,1), (7,1))
pygame.draw.line(PackageWithoutCrate, WHITE, (1,2), (8,2))
pygame.draw.line(PackageWithoutCrate, WHITE, (0,3), (9,3))
pygame.draw.line(PackageWithoutCrate, WHITE, (0,4), (9,4))
pygame.draw.line(PackageWithoutCrate, WHITE, (0,4), (4,10))
pygame.draw.line(PackageWithoutCrate, WHITE, (3,4), (4,10))
pygame.draw.line(PackageWithoutCrate, WHITE, (6,4), (5,10))
pygame.draw.line(PackageWithoutCrate, WHITE, (9,4), (5,10))

PackageWithoutCrate = pygame.transform.scale(PackageWithoutCrate, ((30,45)))
PackageWithoutCrate.set_colorkey(BLACK)

#Tank
tank = pygame.Surface((50,30))
pygame.draw.line(tank, GREY, (18,0), (32,0))
pygame.draw.line(tank, GREY, (16,1), (34,1))
pygame.draw.line(tank, GREY, (15,2), (35,2))
pygame.draw.line(tank, GREY, (15,3), (35,3))
pygame.draw.rect(tank, GREY, (15, 4, 22, 8))

pygame.draw.rect(tank, GREY, (38, 5, 6, 3))
pygame.draw.rect(tank, GREY, (45, 4, 4, 5))

pygame.draw.line(tank, GREY, (3,13), (47,13))
pygame.draw.line(tank, GREY, (2,14), (48,14))
pygame.draw.line(tank, GREY, (1,15), (49,15))
pygame.draw.rect(tank, GREY, (0, 16, 50, 4))

pygame.draw.polygon(tank, DARKBROWN, [(0,21), (49,21), (44,29), (4,29)])
pygame.draw.circle(tank, LIGHTBROWN, (8,25), 3)
pygame.draw.circle(tank, LIGHTBROWN, (25,25), 3)
pygame.draw.circle(tank, LIGHTBROWN, (41,25), 3)

tank.set_colorkey(BLACK)

#Ecran titre
titlecard = globalfont.render("STAR BLAZER", True, DARKGREEN)
titlecardrect = titlecard.get_rect()
titlecardrect.center = (int(width/2), int(height/2))
titlecardwidth = titlecardrect.right - titlecardrect.left
titlecardheight = titlecardrect.bottom - titlecardrect.top
titlecard = pygame.transform.scale(titlecard, ((2*titlecardwidth), (2*titlecardheight)))
titlecardrect = titlecard.get_rect()
titlecardrect.center = (int(width/2), int(height/2))

#Messages pour le high score
msg1 = globalfont.render("WELL DONE !", True, WHITE)
msg1_rect = msg1.get_rect()
msg1_rect.top = 151
msg1_rect.right = width - 100
msg2 = globalfont.render("PLEASE ENTER YOUR NAME", True, WHITE)
msg2_rect = msg2.get_rect()
msg2_rect.topright = msg1_rect.bottomright
