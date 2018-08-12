import pygame, os
from pygame.locals import *
from HUD import *

ScreenVertCenter = int(width/2)

#Lecture

def ReadHiScores():
    hiscorefile = open((os.path.join(os.getcwd(), "data", "hiscores.dat")), 'r')

    hiscore_line_1 = []
    hiscore_line_2 = []
    hiscore_line_3 = []
    hiscore_line_4 = []
    hiscore_line_5 = []

    while True:
        buffer = hiscorefile.read(1)
        if not buffer or buffer == '\n': break
        else: hiscore_line_1.append(buffer)

    while True:
        buffer = hiscorefile.read(1)
        if not buffer or buffer == '\n': break
        else: hiscore_line_2.append(buffer)

    while True:
        buffer = hiscorefile.read(1)
        if not buffer or buffer == '\n': break
        else: hiscore_line_3.append(buffer)

    while True:
        buffer = hiscorefile.read(1)
        if not buffer or buffer == '\n': break
        else: hiscore_line_4.append(buffer)

    while True:
        buffer = hiscorefile.read(1)
        if not buffer or buffer == '\n': break
        else: hiscore_line_5.append(buffer)

    hiscorefile.close()

    str1 = "".join(hiscore_line_1)
    str2 = "".join(hiscore_line_2)
    str3 = "".join(hiscore_line_3)
    str4 = "".join(hiscore_line_4)
    str5 = "".join(hiscore_line_5)

    return str1, str2, str3, str4, str5

class HiScoreElement:
    def __init__(self, value):
        self.sprite = globalfont.render(value, True, WHITE)
        self.rect = self.sprite.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.sprite = pygame.transform.scale(self.sprite, (int(1.5*self.width), int(1.5*self.height)))
        self.rect = self.sprite.get_rect()

def CreateHiScoreSprites():
    hiscores = ["","","","",""]
    hiscorepanel = [HiScoreElement("HIGH SCORES")]
    
    hiscores[0:5] = ReadHiScores()

    for i in range(len(hiscores)):
        hiscorepanel.append(HiScoreElement(hiscores[i]))
        if i == 0:
            hiscorepanel[i].rect.center = ((ScreenVertCenter, 105))
        else:
            hiscorepanel[i].rect.centerx = ScreenVertCenter
            hiscorepanel[i].rect.top = hiscorepanel[i-1].rect.bottom +5
            hiscorepanel[i+1].rect.centerx = ScreenVertCenter
            hiscorepanel[i+1].rect.top = hiscorepanel[i].rect.bottom +5
    
    return hiscorepanel

def DisplayHiScores():
    hiscorepanel = CreateHiScoreSprites()

    for i in range(len(hiscorepanel)):
        screen.blit(hiscorepanel[i].sprite, hiscorepanel[i].rect.topleft)
    
#Ecriture

def SplitHiScores():
    hiscorefile = open((os.path.join(os.getcwd(), "data", "hiscores.dat")), 'r')

    scoreboard = ["","","","",""]
    nameboard = ["","","","",""]

    hiscore_int_1 = []
    hiscore_int_2 = []
    hiscore_int_3 = []
    hiscore_int_4 = []
    hiscore_int_5 = []

    hiscore_name_1 = []
    hiscore_name_2 = []
    hiscore_name_3 = []
    hiscore_name_4 = []
    hiscore_name_5 = []

    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    numbers = list("0123456789")

    while True:
        buffer = hiscorefile.read(1)
        if not buffer or buffer == '\n': break
        else:
            if buffer in numbers:
                hiscore_int_1.append(buffer)
            elif buffer in letters:
                hiscore_name_1.append(buffer)

    while True:
        buffer = hiscorefile.read(1)
        if not buffer or buffer == '\n': break
        else:
            if buffer in numbers:
                hiscore_int_2.append(buffer)
            elif buffer in letters:
                hiscore_name_2.append(buffer)

    while True:
        buffer = hiscorefile.read(1)
        if not buffer or buffer == '\n': break
        else:
            if buffer in numbers:
                hiscore_int_3.append(buffer)
            elif buffer in letters:
                hiscore_name_3.append(buffer)

    while True:
        buffer = hiscorefile.read(1)
        if not buffer or buffer == '\n': break
        else:
            if buffer in numbers:
                hiscore_int_4.append(buffer)
            elif buffer in letters:
                hiscore_name_4.append(buffer)

    while True:
        buffer = hiscorefile.read(1)
        if not buffer or buffer == '\n': break
        else:
            if buffer in numbers:
                hiscore_int_5.append(buffer)
            elif buffer in letters:
                hiscore_name_5.append(buffer)

    hiscorefile.close()

    scoreboard[0] = int("".join(hiscore_int_1))
    nameboard[0] = "".join(hiscore_name_1)

    scoreboard[1] = int("".join(hiscore_int_2))
    nameboard[1] = "".join(hiscore_name_2)

    scoreboard[2] = int("".join(hiscore_int_3))
    nameboard[2] = "".join(hiscore_name_3)

    scoreboard[3] = int("".join(hiscore_int_4))
    nameboard[3] = "".join(hiscore_name_4)

    scoreboard[4] = int("".join(hiscore_int_5))
    nameboard[4] = "".join(hiscore_name_5)

    return scoreboard, nameboard

def WriteHiScore(score, name):
    to_be_written = ["","","","",""]
    scoreboard, nameboard = SplitHiScores()

    if score >= scoreboard[4] and score <= scoreboard[3]:
        scoreboard.insert(4, score)
        nameboard.insert(4, name)
    elif score >= scoreboard[3] and score <= scoreboard[2]:
        scoreboard.insert(3, score)
        nameboard.insert(3, name)
    elif score >= scoreboard[2] and score <= scoreboard[1]:
        scoreboard.insert(2, score)
        nameboard.insert(2, name)
    elif score >= scoreboard[1] and score <= scoreboard[0]:
        scoreboard.insert(1, score)
        nameboard.insert(1, name)
    elif score >= scoreboard[0]:
        scoreboard.insert(0, score)
        nameboard.insert(0, name)

    scoreboard.pop(5)
    nameboard.pop(5)

    for i in range(len(to_be_written)):
        scoreboard[i] = str('%06d' % scoreboard[i])
        to_be_written[i] = (scoreboard[i] + "    " +nameboard[i])

    hiscorefile = open((os.path.join(os.getcwd(), "data", "hiscores.dat")), 'w')
    hiscorefile.write("")
    hiscorefile.close()
    hiscorefile = open((os.path.join(os.getcwd(), "data", "hiscores.dat")), 'a')

    for i in range(len(to_be_written)):
        if i < len(to_be_written) -1:
            hiscorefile.write(to_be_written[i] + "\n")
        elif i == len(to_be_written) -1:
            hiscorefile.write(to_be_written[i])
            
    hiscorefile.close()

#Check

def CheckHiScore():
    scoreboard, nameboard = SplitHiScores()
    lowestscore = scoreboard[4]
    return lowestscore

#Entrée du nom

class Letter:
    def __init__(self, value):
        self.value = value
        self.sprite = globalfont.render(value, True, WHITE)
        self.rect = self.sprite.get_rect()
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top
        self.sprite = pygame.transform.scale(self.sprite, (2*self.width,2*self.height))
        self.rect = self.sprite.get_rect()

lettres = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

line1 = list("ABCDEFG")
line2 = list("HIJKLMN")
line3 = list("OPQRSTU")
line4 = list("VWXYZ .")

endchar = pygame.image.load(os.path.join(os.getcwd(), "resources", "endchar.png"))
delchar = pygame.image.load(os.path.join(os.getcwd(), "resources", "delchar.png"))

def ClassesIntoList(line):
    for i in range(len(line)):
        line[i] = Letter(line[i])
        if line[i].value == " ":
            line[i].value = "delchar"
            line[i].sprite = pygame.transform.scale(delchar, (line[i-1].rect.width, line[i-1].rect.height))
            line[i].rect = line[i].sprite.get_rect()
        if line[i].value == ".":
            line[i].value = "endchar"
            line[i].sprite = pygame.transform.scale(endchar, (line[i-1].rect.width, line[i-1].rect.height))
            line[i].rect = line[i].sprite.get_rect()
        if i == 0:
            line[i].rect.left = 100
        else:
            line[i].rect.left = line[i-1].rect.right + 20
        line[i].sprite.get_rect()
    return line

line1 = ClassesIntoList(line1)
line2 = ClassesIntoList(line2)
line3 = ClassesIntoList(line3)
line4 = ClassesIntoList(line4)

grid = [line1, line2, line3, line4]

def PrintGridAsText():
    #Seulement pour le debug
    for i in range(4):
        for j in range(len(grid[i])):
            print(grid[i][j].value, end="")
        print("")

def PrintGrid():
    for i in range(4):
        for j in range(len(grid[i])):
            grid[i][j].rect.top = (100 + i*51)
            screen.blit(grid[i][j].sprite, grid[i][j].rect.topleft)
            grid[i][j].sprite.get_rect()

Cursor = pygame.Surface((50,50))
pygame.draw.line(Cursor, DARKGREEN, (0,0), (48,0))
pygame.draw.line(Cursor, DARKGREEN, (48,0), (48,48))
pygame.draw.line(Cursor, DARKGREEN, (48,48), (0,48))
pygame.draw.line(Cursor, DARKGREEN, (0,48), (0,0))
Cursor = pygame.transform.scale(Cursor, (2*grid[0][0].width,int(1.3*grid[0][0].height)))
CursorRect = Cursor.get_rect()
Cursor.set_colorkey(BLACK)
