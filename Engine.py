import pygame, os, time, _thread, shutil, platform
from Entities import *
from HUD import *
from Hiscores import *
from debug import *
from Controls import *

operatingsystem = platform.system()

fpsClock = pygame.time.Clock()
pygame.joystick.init()

#Sound engine
pygame.mixer.init(channels=8)
soundpath = os.path.join(os.getcwd(), "resources", "snd")

snd_debug = pygame.mixer.Sound(os.path.join(soundpath, "debug.ogg"))
snd_debug.set_volume(0.5*volume)
snd_cheat = pygame.mixer.Sound(os.path.join(soundpath, "cheat.ogg"))
snd_cheat.set_volume(0.5*volume)
snd_hiscore = pygame.mixer.Sound(os.path.join(soundpath, "hiscore.ogg"))
snd_hiscore.set_volume(0.5*volume)
snd_hiscore_cursor = pygame.mixer.Sound(os.path.join(soundpath, "hiscore_cursor.ogg"))
snd_hiscore_cursor.set_volume(0.5*volume)
snd_hiscore_select = pygame.mixer.Sound(os.path.join(soundpath, "hiscore_select.ogg"))
snd_hiscore_select.set_volume(0.5*volume)
snd_explosion = pygame.mixer.Sound(os.path.join(soundpath, "explosion.ogg"))
snd_explosion.set_volume(0.5*volume)
snd_laser = pygame.mixer.Sound(os.path.join(soundpath, "laser.ogg"))
snd_laser.set_volume(0.5*volume)
snd_refuel = pygame.mixer.Sound(os.path.join(soundpath, "refuel.ogg"))
snd_refuel.set_volume(0.5*volume)

def PlaySound(sound):
    #Existe juste pour le multithreading
    _thread.start_new_thread(pygame.mixer.Sound.play, (sound,))

class InputBuffer:
    def __init__(self):
        self.buffer = []
        self.frame = 0
        self.code1 = [controls_right, controls_left, controls_right, controls_left, controls_down, controls_down, controls_up, controls_up]
        self.code2 = [controls_up, controls_up, controls_down, controls_down, controls_left, controls_right, controls_left, controls_right]
    def CheckForEasterEgg(self):
        match = 0
        pathToData = os.path.join(os.getcwd(), "data")
        if len(self.code1) == len(self.buffer):
            for i in range(len(self.code1)):
                if self.buffer[i] == self.code1[i]:
                    match += 1
                if match == 8:
                    if Engine.debugmode == False:
                        PlaySound(snd_debug)
                        if operatingsystem == "Windows":
                            shutil.copy(pathToData+"\hiscores.bkp", pathToData+"\hiscores.dat")
                        elif operatingsystem == "Linux":
                            shutil.copy(pathToData+"/hiscores.bkp", pathToData+"/hiscores.dat")
                        Engine.debugmode = True
                    elif Engine.debugmode == True:
                        PlaySound(snd_debug)
                        Engine.debugmode = False
                    match = 0
                    
        if len(self.code2) == len(self.buffer):
            for i in range(len(self.code2)):
                if self.buffer[i] == self.code2[i]:
                    match += 1
                if match == 8:
                    if Engine.Cheater == False:
                        PlaySound(snd_cheat)
                        Engine.Cheater = True
        self.buffer = []

class GameEngineInstance:
    def __init__(self, debugmode, joymode):
        self.state = "Init"
        self.frame = 0
        self.realframe = 0
        self.stage = 6
        self.gameloop = 0
        self.StageLayer = []
        #Flags utiles
        self.debugmode = debugmode
        self.HiScoresOnTitle = False
        self.HasJoystick = joymode
        self.LevelComplete = False
        self.BGM = False
        self.Cheater = False
	
    def UpdateDisplay(self, frame, fpsClock):
        #MAJ du joueur
        if Engine.state == "NameReg":
            Player.x = -100
            Player.y = -100
        ##Traitement du respawn
        if Player.IsInvincible == True:
            Player.rect.topleft = (2*width, 2*height)
            Player.hitbox.center = Player.rect.center
            if Engine.frame % 10 == 0:
                pass
            else:
                screen.blit(Player.sprite, (Player.x, Player.y))
        else:
            screen.blit(Player.sprite, (Player.x, Player.y))
            Player.rect.topleft = (Player.x, Player.y)
            Player.hitbox.center = Player.rect.center

        if Player.IsRespawning == True:
            if Engine.frame < Player.DiedOnFrame + Player.RespawnDuration:
                Player.ControlsEnabled = False
                Player.x += 5
            
        #MAJ des balles:
        if len(Bullets) >= 1:
            for i in range(len(Bullets)-1,-1,-1):
                screen.blit(Bullets[i].sprite, (Bullets[i].x, Bullets[i].y))
                Bullets[i].x += 10
                Bullets[i].y += Bullets[i].vertspeed
                Bullets[i].rect.topleft = ((Bullets[i].x, Bullets[i].y))
                if Bullets[i].x >= width + 100 or Bullets[i].x <= -120:
                    Bullets.pop(i)
                    break
                if Bullets[i].rect.bottom == bgLayerRect.top:
                    Bullets.pop(i)
                    break
        if len(EnemyBullets) >= 1:
            for i in range(len(EnemyBullets)-1,-1,-1):
                screen.blit(EnemyBullets[i].sprite, (EnemyBullets[i].x, EnemyBullets[i].y))
                EnemyBullets[i].x += EnemyBullets[i].horizspeed
                EnemyBullets[i].y += EnemyBullets[i].vertspeed
                EnemyBullets[i].rect.topleft = ((EnemyBullets[i].x, EnemyBullets[i].y))
                if EnemyBullets[i].x >= width + 100 or EnemyBullets[i].x <= -120:
                    EnemyBullets.pop(i)
                    break
                if EnemyBullets[i].y >= bgLayerRect.top:
                    EnemyBullets.pop(i)
                    break
        if len(EnemyBalloons) >= 1:
            for i in range(len(EnemyBalloons)-1,-1,-1):
                if Engine.frame % 10 == 0:
                    if EnemyBalloons[i].vertspeed < EnemyBalloons[i].maxvertspeed:
                        EnemyBalloons[i].vertspeed -= 1
                EnemyBalloons[i].x += EnemyBalloons[i].horizspeed
                EnemyBalloons[i].y += EnemyBalloons[i].vertspeed
                screen.blit(EnemyBalloons[i].sprite, (EnemyBalloons[i].x, EnemyBalloons[i].y))
                EnemyBalloons[i].rect.topleft = ((EnemyBalloons[i].x, EnemyBalloons[i].y))
                if EnemyBalloons[i].rect.bottom < -1 or EnemyBalloons[i].rect.right < -1:
                    EnemyBalloons.pop(i)
                    break

        #MAJ des bombes
        if len(Bombs) >= 1:
            for i in range(len(Bombs)-1,-1,-1):
                screen.blit(Bombs[i].sprite, (Bombs[i].x, Bombs[i].y))
                if frame - Bombs[i].droppedOnFrame <= 10:
                    Bombs[i].x += 2
                Bombs[i].y += 2
                Bombs[i].rect.topleft = ((Bombs[i].x, Bombs[i].y))
                if Bombs[i].rect.bottom >= bgLayerRect.top:
                    PlaySound(snd_explosion)
                    SpawnExplosion(Bombs[i].x, Bombs[i].y, "Bomb", Engine.frame)
                    try:
                        Bombs.pop(i)
                    except:
                        pass
                    break
        if len(EnemyBombs) >= 1:
            for i in range(len(EnemyBombs)-1,-1,-1):
                screen.blit(EnemyBombs[i].sprite, (EnemyBombs[i].x, EnemyBombs[i].y))
                EnemyBombs[i].y += randint(2,6)
                EnemyBombs[i].rect.topleft = ((EnemyBombs[i].x, EnemyBombs[i].y))
                if EnemyBombs[i].rect.bottom >= bgLayerRect.top:
                    PlaySound(snd_explosion)
                    SpawnExplosion(EnemyBombs[i].x, EnemyBombs[i].y, "Bomb", Engine.frame)
                    EnemyBombs.pop(i)
                    break

        #MAJ des ennemis
        if len(Enemies) >= 1:
            for i in range(len(Enemies)):
                if Enemies[i].x < width + 51 and Enemies[i].x > -50:
                    screen.blit(Enemies[i].sprite, (Enemies[i].x, Enemies[i].y))
                else:
                    pass
                Enemies[i].x += Enemies[i].horizspeed
                Enemies[i].y += Enemies[i].vertspeed
                Enemies[i].rect.topleft = ((Enemies[i].x, Enemies[i].y))

        #MAJ des objectifs
        try:
            #Oui c'est bugué à ce point
            for i in range(len(Objectives)-1,-1,-1):
                if Player.y >= ((height*6) / 10):
                    if Objectives[i].x <= width - 55:
                        Objectives[i].speed = 6
                    else:
                        Objectives[i].speed = 0
                else:
                    if Objectives[i].rect.left >= int((width*2)/10):
                        Objectives[i].speed = -3
                    else:
                        Objectives[i].speed = 0
                Objectives[i].x += Objectives[i].speed
                Objectives[i].rect.topleft = ((Objectives[i].x, Objectives[i].y))
                screen.blit(Objectives[i].sprite, Objectives[i].rect.topleft)
        except:
            pass

        #EXPLOSIOOOOOOONS </MichaelBay>
        if len(Splosion) >= 1:
            for i in range(len(Splosion)-1,-1,-1):
                if frame == Splosion[i].StartOnFrame + 10:
                    Splosion[i].sprite = pygame.image.load(os.path.join(os.getcwd(), "resources", "ExplosionFrame2.png"))
                    Splosion[i].sprite = pygame.transform.scale(Splosion[i].sprite, (Splosion[i].width, Splosion[i].height))
                    screen.blit(Splosion[i].sprite, (Splosion[i].x, Splosion[i].y))
                elif frame == Splosion[i].StartOnFrame + 20:
                    Splosion[i].sprite = pygame.image.load(os.path.join(os.getcwd(), "resources", "ExplosionFrame3.png"))
                    Splosion[i].sprite = pygame.transform.scale(Splosion[i].sprite, (Splosion[i].width, Splosion[i].height))
                    screen.blit(Splosion[i].sprite, (Splosion[i].x, Splosion[i].y))
                elif frame >= Splosion[i].StartOnFrame + 30:
                    Splosion.pop(i)
                    break
                else:
                    screen.blit(Splosion[i].sprite, (Splosion[i].x, Splosion[i].y))

        Engine.frame += 1
        Engine.realframe +=1

        if Engine.debugmode == True:
            DisplayDebugInfo(Engine.frame, Player.ControlsEnabled, Engine.StageLayer)
        
        pygame.display.flip()
        fpsClock.tick(framerate)

    def CollisionDetection(self, frame, StageLayer, stage):
        #Balles/Everything
        for i in range(len(Bullets)-1,-1,-1):
            for j in range(len(Enemies)-1,-1,-1):
                if Bullets[i].rect.colliderect(Enemies[j]):
                    Enemies[j].hitpoints -= 1
                    Bullets.pop(i)
                    if Enemies[j].hitpoints == 0:
                        Enemies[j].Die()
                        PlaySound(snd_explosion)
                        SpawnExplosion(Enemies[j].x, Enemies[j].y, "Player", Engine.frame)
                        Enemies.pop(j)
                        break
        for i in range(len(Bullets)-1,-1,-1):
            for j in range(len(EnemyBalloons)-1,-1,-1):
                if Bullets[i].rect.colliderect(EnemyBalloons[j]):
                    Bullets.pop(i)
                    SpawnExplosion(EnemyBalloons[j].x, EnemyBalloons[j].y, "Player", Engine.frame)
                    EnemyBalloons.pop(j)
                    PlaySound(snd_explosion)
                    break
        for i in range(len(EnemyBullets)-1,-1,-1):
            if EnemyBullets[i].rect.colliderect(Player.hitbox):
                Player.Die(Engine.frame)
                PlaySound(snd_explosion)
                SpawnExplosion(Player.x, Player.y, "Player", Engine.frame)
                EnemyBullets.pop(i)
                break
        for i in range(len(EnemyBalloons)-1,-1,-1):
            if EnemyBalloons[i].rect.colliderect(Player.hitbox):
                Player.Die(Engine.frame)
                PlaySound(snd_explosion)
                SpawnExplosion(Player.x, Player.y, "Player", Engine.frame)
                EnemyBalloons.pop(i)
                break 

        #Joueur/Everything
        if Player.rect.bottom >= bgLayerRect.top - 100:
            for i in range(len(Engine.StageLayer)):
                if Engine.StageLayer[i].rect.colliderect(Player.rect) and Engine.StageLayer[i].name != "Empty":
                    Player.Die(Engine.frame)
                    PlaySound(snd_explosion)
                    SpawnExplosion(Player.x, Player.y, "Player", Engine.frame)
                    break
        for i in range(len(Enemies)):
            if Enemies[i].x < Player.x - 51 and Enemies[i].x > Player.x + 51:
                if Player.rect.colliderect(Enemies[i].rect):
                    Player.Die(Engine.frame)
                    PlaySound(snd_explosion)
                    SpawnExplosion(Player.x, Player.y, "Player", Engine.frame)
                    break
            else:
                pass
        if len(Friendlies) == 2:
            if Player.rect.colliderect(Friendlies[1].rect):
                PlaySound(snd_refuel)
                Player.fuel = 3000
                Player.bombs = 30
                Player.score += Friendlies[1].pointsawarded
                Friendlies.pop(1)
                Friendlies[0].WhereToDrop = 0
            elif Friendlies[1].rect.bottom == bgLayerRect.top:
                Friendlies[0].WhereToDrop = 0
                Friendlies.pop(1)
        if len(EnemyBombs) >= 1:
            for i in range(len(EnemyBombs)-1,-1,-1):
                if EnemyBombs[i].rect.colliderect(Player.rect):
                    PlaySound(snd_explosion)
                    SpawnExplosion(Player.x, Player.y, "Player", Engine.frame)
                    EnemyBombs.pop(i)
                    Player.Die(Engine.frame)
                    break
                if len(Bullets) > 0:
                    for j in range(len(Bullets)-1,-1,-1):
                        if EnemyBombs[i].rect.colliderect(Bullets[j].rect):
                           PlaySound(snd_explosion)
                           SpawnExplosion(EnemyBombs[i].x, EnemyBombs[i].y, "Bomb", Engine.frame)
                           EnemyBombs.pop(i)
                           Bullets.pop(j)
                           break

        #Bombes/Sol
        for i in range(len(Engine.StageLayer)-1,-1,-1):
            for j in range(len(Bombs)-1,-1,-1):
                if Engine.StageLayer[i].rect.colliderect(Bombs[j].rect):
                    if Engine.StageLayer[i].name != "Empty" and Engine.StageLayer[i].name != "cactus":
                        Engine.StageLayer[i].hitpoints -= 1
                        PlaySound(snd_explosion)
                        SpawnExplosion(Bombs[j].x, Bombs[j].y, "Bomb", Engine.frame)
                        Bombs.pop(j)
                        if Engine.StageLayer[i].hitpoints == 0 and Engine.StageLayer[i].IsObjective == False:
                            Engine.StageLayer[i].sprite = EmptySprite
                            Engine.StageLayer[i].name = "Empty"
                            break
                        elif Engine.StageLayer[i].hitpoints == 0  and Engine.StageLayer[i].IsObjective == True:
                            Engine.StageLayer[i].sprite = EmptySprite
                            Engine.StageLayer[i].name = "Empty"
                            Player.score += 750
                            Engine.LevelComplete = True
                            Player.ControlsEnabled = False
                            Player.IsInvincible = True
                            break
                        elif Engine.StageLayer[i].hitpoints > 0  and Engine.StageLayer[i].IsObjective == True:
                            Player.score += 100
                            break
                        else:
                            break
        for i in range(len(Objectives)):
            for j in range(len(Bombs)-1,-1,-1):
                if Objectives[i].rect.colliderect(Bombs[j].rect):
                    Objectives[i].hitpoints -= 1
                    PlaySound(snd_explosion)
                    SpawnExplosion(Bombs[j].x, Bombs[j].y, "Bomb", Engine.frame)
                    Bombs.pop(j)
                    Player.score += 100
                    if Objectives[i].hitpoints <= 0:
                        Objectives[i] = EmptyStageElement()
                        Player.score += 750
                        Engine.LevelComplete = True
                        Player.ControlsEnabled = False
                        Player.IsInvincible = True
                        break
                    else:
                        break
        for i in range(len(Bombs)-1,-1,-1):
            if Bombs[i].rect.bottom == bgLayerRect.top:
                PlaySound(snd_explosion)
                Bombs.pop(i)
                break

if pygame.joystick.get_count() > 0:
    Engine = GameEngineInstance(False, True)
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    buttons = joystick.get_numbuttons()
else:
    Engine = GameEngineInstance(False, False)

if Engine.HasJoystick == True:  
    pass

Input = InputBuffer()

def Reset():
    Engine.StageLayer = []
    Engine.StageLayer = ComposeStageLayer(Engine.stage)
    Engine.StageLayer[0].rect.left = width + 100

    x = 0
    y = 0

    Enemies.clear()
    Bullets.clear()
    EnemyBullets.clear()
    EnemyBalloons.clear()
    EnemyBombs.clear()
    Bombs.clear()
    Splosion.clear()
    Objectives.clear()

    if Engine.gameloop == 0:
        if Engine.Cheater == False:
            Player.lives = 3
        else:
            Player.lives = 30
        Player.score = 0
    else: pass

    Player.name = []
    Player.fuel = 3000
    Player.bombs = 30
    Player.IsRespawning = False
    Player.IsInvincible = False
    Player.x = - 100
    Player.y = int(height/2)
    
    Engine.frame = 0
    Engine.realframe = 0
    Engine.LevelComplete = False

    return Engine.StageLayer

if Engine.state == "Init":
    pressedkeys = pygame.key.get_pressed()
    Engine.StageLayer = Reset()
    Engine.state = "Title"

def TitleLoop(hiscore):
    Player.x = - 100
    Player.y = int(height/2)
    Player.fuel = 0
    Player.bombs = 0
    Player.score = 0
    if Engine.Cheater == False:
        Player.lives = 0
    else:
        Player.lives = 30
    screen.fill(BLACK)
    BackgroundLayerRender()
    HUDLayerRender(Engine.stage, Engine.debugmode)

    #Affichage du hiscore ou du titre
    if hiscore == False:
        screen.blit(titlecard, titlecardrect.topleft)
    elif hiscore == True:
        DisplayHiScores()

    #Scrolling du background
    RenderStageLayer(Engine.StageLayer)

    #Objectifs de mission
    if Engine.stage == 1:
        missionobjective = globalfont.render("BOMB THE RADAR", True, DARKGREEN)
    elif Engine.stage == 2:
        missionobjective = globalfont.render("ATTACK THE TANK", True, DARKGREEN)
    elif Engine.stage == 3:
        missionobjective = globalfont.render("BOMB THE ICBM", True, DARKGREEN)
    elif Engine.stage == 4:
        missionobjective = globalfont.render("ATTACK THE TANK", True, DARKGREEN)
    elif Engine.stage == 5:
        missionobjective = globalfont.render("BOMB THE HEADQUARTERS", True, DARKGREEN)
    else:
        missionobjective = globalfont.render("WAT", True, DARKGREEN)
        #Si vous voyez ça in-game, quelquechose a VRAIMENT merdé

    missionobjectiveRect = missionobjective.get_rect()
    missionobjectiveRect.bottomright = ((width - 50, height - 5))
    screen.blit(missionobjective, missionobjectiveRect.topleft)

    hubris = globalfont.render("PROGRAMMED BY LOU", True, WHITE)
    hubrisRect = hubris.get_rect()
    hubrisRect.bottomright = ((width - 1, bgLayerRect.top))
    screen.blit(hubris, hubrisRect.topleft)

    if Engine.HasJoystick == True:
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)
    else:
        axis_x = 0
        axis_y = 0
    #Evènements système
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                Engine.state = "PreMission"
                Engine.frame = 0
                Engine.gameloop = 0
                Engine.StageLayer = Reset()
            if event.key == K_ESCAPE:
                Engine.state = "Quit"
            if event.key == controls_up or axis_y == 1:
                #print("Up")
                Input.buffer.append(controls_up)
                if len(Input.buffer) == 1:
                    Input.frame = Engine.realframe
            if event.key == controls_down or axis_y == -1:
                #print("Down")
                Input.buffer.append(controls_down)
                if len(Input.buffer) == 1:
                    Input.frame = Engine.realframe
            if event.key == controls_left or axis_x == -1:
                #print("Left")
                Input.buffer.append(controls_left)
                if len(Input.buffer) == 1:
                    Input.frame = Engine.realframe
            if event.key == controls_right or axis_x == 1:
                #print("Right")
                Input.buffer.append(controls_right)
                if len(Input.buffer) == 1:
                    Input.frame = Engine.realframe
        if Engine.HasJoystick == True:
            if event.type == JOYBUTTONDOWN:
                if joystick.get_button(jcontrols_escape) == True:
                    Engine.state = "Quit"
                else:
                    Engine.state = "PreMission"
                    Engine.frame = 0
                    Engine.gameloop = 0
                    Engine.StageLayer = Reset()
            if event.type == JOYAXISMOTION:
                if axis_y < -0.5:
                    #print("Up")
                    Input.buffer.append(controls_up)
                    if len(Input.buffer) == 1:
                        Input.frame = Engine.realframe
                if axis_y > 0.5:
                    #print("Down")
                    Input.buffer.append(controls_down)
                    if len(Input.buffer) == 1:
                        Input.frame = Engine.realframe
                if axis_x < -0.5:
                    #print("Left")
                    Input.buffer.append(controls_left)
                    if len(Input.buffer) == 1:
                        Input.frame = Engine.realframe
                if axis_x > 0.5:
                    #print("Right")
                    Input.buffer.append(controls_right)
                    if len(Input.buffer) == 1:
                        Input.frame = Engine.realframe
        if event.type == QUIT:
            Engine.state = "Quit"

    if len(Input.buffer) == 8:
        Input.CheckForEasterEgg()

    if Engine.frame == (5 * framerate) and hiscore == False:
        Engine.HiScoresOnTitle = True
        Engine.frame = 0
    elif Engine.frame == (5 * framerate) and hiscore == True:
        Engine.HiScoresOnTitle = False
        Engine.frame = 0
        
    if Engine.realframe == Input.frame + (3 * framerate):
        Input.buffer = []
    
    Engine.UpdateDisplay(Engine.frame, fpsClock)

def PreMissionLoop():
    BackgroundLayerRender()
    HUDLayerRender(Engine.stage, Engine.debugmode)
    RenderStageLayer(Engine.StageLayer)
    
    if Engine.stage == 1:
        missionobjective = globalfont.render("BOMB THE RADAR", True, DARKGREEN)
        missionobjectivesprite = pygame.image.load(os.path.join(os.getcwd(), "resources", "radar.png"))
    elif Engine.stage == 2:
        missionobjective = globalfont.render("ATTACK THE TANK", True, DARKGREEN)
        missionobjectivesprite = tank
    elif Engine.stage == 3:
        missionobjective = globalfont.render("BOMB THE ICBM", True, DARKGREEN)
        missionobjectivesprite = pygame.image.load(os.path.join(os.getcwd(), "resources", "icbm.png"))
    elif Engine.stage == 4:
        missionobjective = globalfont.render("ATTACK THE TANK", True, DARKGREEN)
        missionobjectivesprite = tank
    elif Engine.stage == 5:
        missionobjective = globalfont.render("BOMB THE HEADQUARTERS", True, DARKGREEN)
        missionobjectivesprite = pygame.image.load(os.path.join(os.getcwd(), "resources", "hquarters.png"))
    elif Engine.stage == 6:
        missionobjective = globalfont.render("WARNING! ENEMY APPROACHING", True, DARKGREEN)
        missionobjectivesprite = EmptySprite
    else:
        missionobjective = globalfont.render("WAT", True, DARKGREEN)

    missionobjectiveRect = missionobjective.get_rect()
    missionobjectiveRect.center = (int(width/2), int(height/2))
    missionobjectivespriteRect = missionobjectivesprite.get_rect()
    missionobjectivespriteRect.top = missionobjectiveRect.bottom + 2
    missionobjectivespriteRect.centerx = int(width/2)
    screen.blit(missionobjective, missionobjectiveRect.topleft)
    screen.blit(missionobjectivesprite, missionobjectivespriteRect.topleft)

    if Engine.frame == 180:
        if Engine.stage < 6:
            Engine.state = "Game"
        elif Engine.stage == 6:
            Engine.state = "Boss"
        Engine.frame = 0
        Engine.StageLayer = Reset()

    for event in pygame.event.get():
        if event.type == QUIT:
            Engine.state = "Quit"
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                Engine.state = "Quit"
            if event.key == K_SPACE:
                if Engine.frame > 30:
                    if Engine.stage < 6:
                        Engine.state = "Game"
                    elif Engine.stage == 6:
                        Engine.state = "Boss"
                    Engine.frame = 0
                    Engine.StageLayer = Reset()
        if Engine.HasJoystick == True:
            if event.type == JOYBUTTONDOWN:
                if joystick.get_button(jcontrols_escape) == True:
                    Engine.state = "Quit"
                else:
                    if Engine.frame > 30:
                        if Engine.stage < 6:
                            Engine.state = "Game"
                        elif Engine.stage == 6:
                            Engine.state = "Boss"
                        Engine.frame = 0
                        Engine.StageLayer = Reset()

    Engine.UpdateDisplay(Engine.frame, fpsClock)
    
def GameLoop():
    if Engine.frame < 60:
        Player.x += 5
        Player.ControlsEnabled = False
        Player.IsRespawning = False
    elif Engine.frame == 60:
        Player.ControlsEnabled = True

    if Engine.stage == 2 and Engine.frame == 90 or Engine.stage == 4 and Engine.frame == 90:
        Objectives.append(ObjectiveTank())

    BackgroundLayerRender()
    HUDLayerRender(Engine.stage, Engine.debugmode)
        
    if Engine.stage == 1:
        missionobjective = globalfont.render("BOMB THE RADAR", True, DARKGREEN)
    elif Engine.stage == 2:
        missionobjective = globalfont.render("ATTACK THE TANK", True, DARKGREEN)
    elif Engine.stage == 3:
        missionobjective = globalfont.render("BOMB THE ICBM", True, DARKGREEN)
    elif Engine.stage == 4:
        missionobjective = globalfont.render("ATTACK THE TANK", True, DARKGREEN)
    elif Engine.stage == 5:
        missionobjective = globalfont.render("BOMB THE HEADQUARTERS", True, DARKGREEN)
    elif Engine.stage == 6:
        missionobjective = globalfont.render("WARNING! ENEMY APPROACHING", True, DARKGREEN)
    else:
        missionobjective = globalfont.render("WAT", True, DARKGREEN)

    missionobjectiveRect = missionobjective.get_rect()
    missionobjectiveRect.bottomright = ((width - 50, height - 5))
    screen.blit(missionobjective, missionobjectiveRect.topleft)

    RenderStageLayer(Engine.StageLayer)

    if Engine.HasJoystick == True:
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)
    else:
        axis_x = 0
        axis_y = 0
    
    #Evènements système
    for event in pygame.event.get():
        if event.type == QUIT:
            Engine.state = "Quit"
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                Engine.state = "Quit"
            if event.key == K_SPACE:
                if Player.ControlsEnabled == True and Player.IsInvincible == False:
                    if Player.rect.bottom <= bgLayerRect.top - 120:
                        if len(Bullets) <= 4:
                            Bullets.append(Bullet(Player.x + 50, Player.y + 25, 10, Player.vertspeed, "Player"))
                            PlaySound(snd_laser)
                    else:
                        if len(Bombs) <= 3 and Player.bombs > 0:
                            Bombs.append(PlayerBombs(Player.x + 25, Player.y + 50, Engine.frame))
                            Player.bombs -= 1
        if event.type == KEYUP:
            if event.key == controls_up or event.key == controls_down or event.key == K_w or event.key == K_s:
                Player.vertspeed = 0
        if Engine.HasJoystick == True:
            if event.type == JOYBUTTONDOWN:
                if joystick.get_button(jcontrols_escape) == True:
                    Engine.state = "Quit"
                else:
                    if Player.ControlsEnabled == True and Player.IsInvincible == False:
                        if Player.rect.bottom <= bgLayerRect.top - 120:
                            if len(Bullets) <= 4:
                                Bullets.append(Bullet(Player.x + 50, Player.y + 25, 10, Player.vertspeed, "Player"))
                                PlaySound(snd_laser)
                        else:
                            if len(Bombs) <= 3 and Player.bombs > 0:
                                Bombs.append(PlayerBombs(Player.x + 25, Player.y + 50, Engine.frame))
                                Player.bombs -= 1
            if event.type == JOYAXISMOTION:
                if Engine.HasJoystick == True:
                    if axis_y > -0.6 and axis_y < 0.6:
                        Player.vertspeed = 0
                else:
                    pass
                            
    #Boucle d'évènements du joueur
    if Player.ControlsEnabled == True:
        if pygame.key.get_pressed()[controls_up] or pygame.key.get_pressed()[pygame.K_w]:
            if Player.y >= 40:
                Player.y -= 5
                Player.vertspeed = -2
            else:
                Player.rect.top = 40
        if pygame.key.get_pressed()[controls_down] or pygame.key.get_pressed()[pygame.K_s]:
            if Player.y <= bgLayerRect.top - Player.rect.height:
                Player.y += 5
                Player.vertspeed = 2
            else:
                Player.rect.bottom = (height * 8/10)+10
        if pygame.key.get_pressed()[controls_right] or pygame.key.get_pressed()[pygame.K_d]:
            if Player.x <= int(width*6/10) - 5:
                Player.x += 5
            else:
                Player.rect.right = int(width*6/10)
        if pygame.key.get_pressed()[controls_left] or pygame.key.get_pressed()[pygame.K_a]:
            if Player.x >= 0:
                Player.x -= 5
            else:
                Player.rect.left = -5

        #Joystick
        if Engine.HasJoystick == True:      
            if axis_y < -0.5:
                if Player.y >= 40:
                    Player.y -= 5
                    Player.vertspeed = -2
                else:
                    Player.rect.top = 40
            if axis_y > 0.5:
                if Player.y <= bgLayerRect.top - Player.rect.height:
                    Player.y += 5
                    Player.vertspeed = 2
                else:
                    Player.rect.bottom = (height * 8/10)+10
            if axis_x > 0.5:
                if Player.x <= int(width*6/10) - 5:
                    Player.x += 5
                else:
                    Player.rect.right = int(width*6/10)
            if axis_x < -0.5:
                if Player.x >= 0:
                    Player.x -= 5
                else:
                    Player.rect.left = -5
            
    #Contrôle du spawn des ennemis
    if Engine.stage == 1 or Engine.stage == 3:
        if Engine.frame % 90 == 0 and Engine.frame >= 91:
            if len(Enemies)+1 <= Engine.stage:
                CreateEnemies(EnemyWeirdPlane(randint(110, int((height * 5.9)/ 10)), Engine.frame))
    elif Engine.stage == 2 or Engine.stage == 4:
        if Engine.frame % 60 == 0 and Engine.frame >= 61:
            if len(Enemies)+1 <= 5:
                CreateEnemies(EnemyPlane(randint(110, int((height * 5.9)/ 10)), Engine.frame))
    elif Engine.stage == 5:
        if Engine.frame % 90 == 0 and Engine.frame >= 91:
            if len(Enemies)+1 <= 8:
                random = randint(1,2)
                if random == 1:
                    CreateEnemies(EnemyWeirdPlane(randint(110, int((height * 5.9)/ 10)), Engine.frame))
                elif random == 2:
                    CreateEnemies(EnemyPlane(randint(110, int((height * 5.9)/ 10)), Engine.frame))
                
    for i in range(len(Enemies)):
        Enemies[i].Behave(Engine.frame)

    if Player.lives <= 0:
        lowestscore = CheckHiScore()
        if Player.score > lowestscore:
            Engine.state = "NameReg"
            if Engine.Cheater == True:
                Engine.Cheater = False
            screen.fill(BLACK)
            Player.x = -100
            Player.y = int(height/2)
        else:
            Engine.stage = 1
            Engine.gameloop = 0
            if Engine.Cheater == True:
                Engine.Cheater = False
            Engine.state = "Title"
            Engine.StageLayer = Reset()

    Player.fuel -= 1

    if Player.fuel <= 1700:
        if Friendlies[0].WhereToDrop == 0:
            Friendlies[0].WhereToDrop = randint(int(width/2),int((width*3)/4))
            #print(Friendlies[0].WhereToDrop)
        screen.blit(Friendlies[0].sprite, (Friendlies[0].x, Friendlies[0].y))
        Friendlies[0].x += 5
        if Friendlies[0].x >= Friendlies[0].WhereToDrop -2 and Friendlies[0].x <= Friendlies[0].WhereToDrop +3:
            if len(Friendlies) == 1:
                Friendlies.append(CarePackage(Friendlies[0].x, Friendlies[0].y, 2, PackageWithCrate, 175))
                #print("Package dropped at", Friendlies[0].x)
            elif len(Friendlies) == 2:
                #print("Package already present on screen at", Friendlies[1].x, Friendlies[1].y)
                pass
        if len(Friendlies) == 2:
            Friendlies[1].x -= 1
            Friendlies[1].y += Friendlies[1].vertspeed
            Friendlies[1].rect.topleft = (Friendlies[1].x, Friendlies[1].y)
            screen.blit(Friendlies[1].sprite, Friendlies[1].rect.topleft)
    else:
        Friendlies[0].x = -100
        if len(Friendlies) == 2:
            Friendlies.pop(1)
        Friendlies[0].WhereToDrop = 0
        screen.blit(Friendlies[0].sprite, (Friendlies[0].x, Friendlies[0].y))

    if Player.fuel == 0:
        Player.Die(Engine.frame)

    if Player.IsRespawning and Engine.frame == Player.DiedOnFrame + Player.RespawnDuration:
        Player.IsRespawning = False
        Player.ControlsEnabled = True

    if Player.IsInvincible and Engine.frame == Player.DiedOnFrame + Player.InvincibilityDuration:
        Player.IsInvincible = False

    if Player.ControlsEnabled == False and Player.IsInvincible == True and Engine.LevelComplete == True:
        Player.x += 5
        if Player.y > int(width/2) - 150:
            Player.y -= 5
        if Player.x > width:
            if Engine.stage + 1 >= 6:
                if Player.score >= 13000:
                    Engine.stage += 1
                    if Player.lives < 5:
                        Player.lives = 5
                    Engine.state = "PreMission"
                    Engine.frame = 0
                else:
                    Player.lives = 0
                    Engine.state = "NameReg"
                    if Engine.Cheater == True:
                        Engine.Cheater = False
                    Engine.frame = 0
            else:
                Engine.stage += 1
                Engine.state = "PreMission"
            Engine.gameloop += 1
            Engine.frame = 0
            Engine.StageLayer = Reset()

    Engine.UpdateDisplay(Engine.frame, fpsClock)

def Boss():
    if Engine.BGM == False:
        pygame.mixer.music.load(os.path.join(os.getcwd(), "resources", "secret", "bosstheme.ogg"))
        pygame.mixer.music.set_volume(0.5 * volume)
        pygame.mixer.music.play(loops=-1)
        Engine.BGM = True
    else:
        pass
    
    if Engine.frame < 60:
        Player.x += 5
        Player.ControlsEnabled = False
        Player.IsRespawning = False
    elif Engine.frame == 60:
        Player.ControlsEnabled = True

    BackgroundLayerRender()

    if Engine.frame >= 2:
        SpecialHUDLayerRender(Engine.debugmode)

    RenderStageLayer(Engine.StageLayer)

    if Engine.HasJoystick == True:
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)
    else:
        axis_x = 0
        axis_y = 0
    
    #Evènements système
    for event in pygame.event.get():
        if event.type == QUIT:
            Engine.state = "Quit"
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                Engine.state = "Quit"
            if event.key == K_SPACE:
                if Player.ControlsEnabled == True and Player.IsInvincible == False:
                    if len(Bullets) <= 4:
                        Bullets.append(Bullet(Player.x + 50, Player.y + 25, 10, Player.vertspeed, "Player"))
                        PlaySound(snd_laser)
        if event.type == KEYUP:
            if event.key == controls_up or event.key == controls_down or event.key == K_w or event.key == K_s:
                Player.vertspeed = 0
        if Engine.HasJoystick == True:
            if event.type == JOYBUTTONDOWN:
                if joystick.get_button(jcontrols_escape) == True:
                    Engine.state = "Quit"
                else:
                    if Player.ControlsEnabled == True and Player.IsInvincible == False:
                        if len(Bullets) <= 4:
                            Bullets.append(Bullet(Player.x + 50, Player.y + 25, 10, Player.vertspeed, "Player"))
                            PlaySound(snd_laser)
            if event.type == JOYAXISMOTION:
                if Engine.HasJoystick == True:
                    if axis_y > -0.6 and axis_y < 0.6:
                        Player.vertspeed = 0
                else:
                    pass
                            
    #Boucle d'évènements du joueur
    if Player.ControlsEnabled == True:
        if pygame.key.get_pressed()[controls_up] or pygame.key.get_pressed()[pygame.K_w]:
            if Player.y >= 40:
                Player.y -= 5
                Player.vertspeed = -2
            else:
                Player.rect.top = 40
        if pygame.key.get_pressed()[controls_down] or pygame.key.get_pressed()[pygame.K_s]:
            if Player.y <= bgLayerRect.top - Player.rect.height:
                Player.y += 5
                Player.vertspeed = 2
            else:
                Player.rect.bottom = (height * 8/10)+10
        if pygame.key.get_pressed()[controls_right] or pygame.key.get_pressed()[pygame.K_d]:
            if Player.x <=width - 5:
                Player.x += 5
            else:
                Player.rect.right = width - 5
        if pygame.key.get_pressed()[controls_left] or pygame.key.get_pressed()[pygame.K_a]:
            if Player.x >= 0:
                Player.x -= 5
            else:
                Player.rect.left = -5

        #Joystick
        if Engine.HasJoystick == True:      
            if axis_y < -0.5:
                if Player.y >= 40:
                    Player.y -= 5
                    Player.vertspeed = -2
                else:
                    Player.rect.top = 40
            if axis_y > 0.5:
                if Player.y <= bgLayerRect.top - Player.rect.height:
                    Player.y += 5
                    Player.vertspeed = 2
                else:
                    Player.rect.bottom = (height * 8/10)+10
            if axis_x > 0.5:
                if Player.x <= width - 5:
                    Player.x += 5
                else:
                    Player.rect.right = width - 5
            if axis_x < -0.5:
                if Player.x >= 0:
                    Player.x -= 5
                else:
                    Player.rect.left = -5
                    
    if Engine.frame == 1:
        CreateEnemies(TOPSECRET(Engine.frame))

    for i in range(len(Enemies)):
        Enemies[i].Behave(Engine.frame)

    if Player.lives <= 0:
        if Engine.BGM == True:
            pygame.mixer.music.stop()
            Engine.BGM = False
        lowestscore = CheckHiScore()
        if Player.score > lowestscore:
            Engine.state = "NameReg"
            if Engine.Cheater == True:
                Engine.Cheater = False
            Engine.frame = 0
            screen.fill(BLACK)
            Player.x = -100
            Player.y = int(height/2)
        else:
            Engine.frame = 0
            Engine.stage = 1
            Engine.gameloop = 0
            if Engine.Cheater == True:
                Engine.Cheater = False
            Engine.state = "Title"
            Engine.StageLayer = Reset()

    if len(Enemies) == 0 and Engine.frame >= 120:
        if Engine.BGM == True:
            pygame.mixer.music.stop()
            Engine.BGM = False
        Player.ControlsEnabled = False
        Player.IsInvincible = True
        Player.x += 5
        if Player.y > int(width/2) - 150 or Player.y < int(width/2):
            Player.y -= 5
        if Player.x >= width + 10:
            lowestscore = CheckHiScore()
            if Player.score > lowestscore:
                Engine.state = "NameReg"
                Engine.frame = 0
                screen.fill(BLACK)
                Player.x = -100
                Player.y = int(height/2)
            else:
                Engine.stage = 1
                Engine.gameloop = 0
                if Engine.Cheater == True:
                    Engine.Cheater = False
                Engine.frame = 0
                Engine.state = "Title"
                Engine.StageLayer = Reset()

    Player.fuel -= 1

    if Player.fuel <= 1700:
        if Friendlies[0].WhereToDrop == 0:
            Friendlies[0].WhereToDrop = randint(int(width/2),int((width*3)/4))
        screen.blit(Friendlies[0].sprite, (Friendlies[0].x, Friendlies[0].y))
        Friendlies[0].x += 5
        if Friendlies[0].x >= Friendlies[0].WhereToDrop -2 and Friendlies[0].x <= Friendlies[0].WhereToDrop +3:
            if len(Friendlies) == 1:
                Friendlies.append(CarePackage(Friendlies[0].x, Friendlies[0].y, 2, PackageWithCrate, 175))
            elif len(Friendlies) == 2:
                pass
        if len(Friendlies) == 2:
            Friendlies[1].x -= 1
            Friendlies[1].y += Friendlies[1].vertspeed
            Friendlies[1].rect.topleft = (Friendlies[1].x, Friendlies[1].y)
            screen.blit(Friendlies[1].sprite, Friendlies[1].rect.topleft)
    else:
        Friendlies[0].x = -100
        if len(Friendlies) == 2:
            Friendlies.pop(1)
        Friendlies[0].WhereToDrop = 0
        screen.blit(Friendlies[0].sprite, (Friendlies[0].x, Friendlies[0].y))

    if Player.fuel == 0:
        Player.Die(Engine.frame)

    if Player.IsRespawning and Engine.frame == Player.DiedOnFrame + Player.RespawnDuration:
        Player.IsRespawning = False
        Player.ControlsEnabled = True

    if Player.IsInvincible and Engine.frame == Player.DiedOnFrame + Player.InvincibilityDuration:
        Player.IsInvincible = False

    Engine.UpdateDisplay(Engine.frame, fpsClock)


def NameRegLoop():
    x = 0
    y = 0

    loop = True
    while loop:
        Player.fuel = 0
        Player.bombs = 0

        BackgroundLayerRender()
        HUDLayerRender(Engine.stage, Engine.debugmode)
        RenderStageLayer(Engine.StageLayer)
        Player.rect.topleft = ((-100, -100))

        PrintGrid()
        screen.blit(msg1, msg1_rect.topleft)
        screen.blit(msg2, msg2_rect.topleft)

        if len(Player.name) >= 1:
            if Engine.frame % 20 == 0:
                 pass
            else:
                screen.blit(globalfont.render("".join(Player.name[x] for x in range(len(Player.name))), True, WHITE), msg2_rect.midbottom)

        CursorRect.left = grid[x][y].rect.left
        CursorRect.top = grid[x][y].rect.top + 10
        screen.blit(Cursor, CursorRect.topleft)

        #Evènements système
        for event in pygame.event.get():
            if event.type == QUIT:
                Engine.state = "Quit"
                loop = False
            if event.type == KEYDOWN and Engine.frame >= 30:
                if event.key == K_SPACE:
                    PlaySound(snd_hiscore_select)
                    if grid[x][y].value == "endchar":
                        while len(Player.name) < 3:
                            Player.name.append(" ")
                        if Player.name[0] == Player.name[1] and Player.name[1] == Player.name[2] and Player.name[2] == " ":
                            Player.name[0] = "W"
                            Player.name[1] = "I"
                            Player.name[2] = "N"
                    elif grid[x][y].value == "delchar":
                        if len(Player.name) >= 1: 
                            Player.name.pop(len(Player.name)-1)
                            PlaySound(snd_hiscore_select)
                        else: pass
                    else:
                        Player.name.append(grid[x][y].value)
                if event.key == K_BACKSPACE:
                    if len(Player.name) >= 1: 
                        Player.name.pop(len(Player.name)-1)
                    else: pass
                if event.key == K_ESCAPE:
                    Engine.state = "Quit"
                    if Engine.Cheater == True:
                        Engine.Cheater = False
                    loop = False
                if event.key == controls_up or event.key == K_w:
                    if x - 1 >= 0:
                        x -= 1
                        PlaySound(snd_hiscore_cursor)
                    else:
                        x = x
                if event.key == controls_down or event.key == K_s:
                    if x + 1 <= 3:
                        x += 1
                        PlaySound(snd_hiscore_cursor)
                    else:
                        x = x
                if event.key == controls_left or event.key == K_a:
                    if y - 1 >= 0:
                        y -= 1
                        PlaySound(snd_hiscore_cursor)
                    else:
                        y = y
                if event.key == controls_right or event.key == K_d:
                    if y + 1 <= 6:
                        y += 1
                        PlaySound(snd_hiscore_cursor)
                    else:
                        y = y
            if Engine.HasJoystick == True:
                if event.type == JOYBUTTONDOWN and Engine.frame >= 30:
                    if joystick.get_button(jcontrols_escape) == True:
                        Engine.state = "Quit"
                        if Engine.Cheater == True:
                            Engine.Cheater = False
                        loop = False
                    else:
                        PlaySound(snd_hiscore_select)
                        if grid[x][y].value == "endchar":
                            while len(Player.name) < 3:
                                Player.name.append(" ")
                            if Player.name[0] == Player.name[1] and Player.name[1] == Player.name[2] and Player.name[2] == " ":
                                Player.name[0] = "W"
                                Player.name[1] = "I"
                                Player.name[2] = "N"
                        elif grid[x][y].value == "delchar":
                            if len(Player.name) >= 1: 
                                Player.name.pop(len(Player.name)-1)
                                PlaySound(snd_hiscore_select)
                            else: pass
                        else:
                            Player.name.append(grid[x][y].value)

                axis_x = joystick.get_axis(0)
                axis_y = joystick.get_axis(1)
                if axis_y < -0.5:
                    if x - 1 >= 0:
                        x -= 1
                        PlaySound(snd_hiscore_cursor)
                    else:
                        x = x
                if axis_y > 0.5:
                    if x + 1 <= 3:
                        x += 1
                        PlaySound(snd_hiscore_cursor)
                    else:
                        x = x
                if axis_x < -0.5:
                    if y - 1 >= 0:
                        y -= 1
                        PlaySound(snd_hiscore_cursor)
                    else:
                        y = y
                if axis_x > 0.5:
                    if y + 1 <= 6:
                        y += 1
                        PlaySound(snd_hiscore_cursor)
                    else:
                        y = y

        Engine.frame += 1

        #Ecriture du hiscore
        if len(Player.name) == 3:
            Player.name = "".join(Player.name[z] for z in range(3))
            WriteHiScore(Player.score, Player.name)
            PlaySound(snd_hiscore)
            if Engine.Cheater == True:
                Engine.Cheater = False
            loop = False
        else: pass

        Engine.UpdateDisplay(Engine.frame, fpsClock)
        
    Engine.stage = 1
    Engine.gameloop = 0
    Reset()
    Engine.state = "Title"
    Engine.HiScoresOnTitle = True
    pygame.display.flip()
    fpsClock.tick(framerate)
