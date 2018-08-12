import pygame, os, time
from Stage import *
from Sprites import *
from random import randint

class PlayerPlane:
    def __init__(self, x, y):
        self.sprite = pygame.image.load(os.path.join(os.getcwd(), "resources", "player.png"))
        self.x = x
        self.y = y
        self.fuel = 3000
        self.bombs = 30
        self.score = 0
        self.lives = 0
        self.rect = self.sprite.get_rect()
        self.rect.topleft = ((self.x, self.y))
        self.name = []
        self.vertspeed = 0
        self.DiedOnFrame = 0
        #Flags
        self.ControlsEnabled = True
        self.IsRespawning = False
        self.IsInvincible = False
        #Hitbox p/r lasers
        self.hitbox = pygame.Rect((0,0), (50,20))
        self.hitbox.center = self.rect.center
        #Valeurs pour le respawn:
        self.RespawnDuration = 150
        self.InvincibilityDuration = 210
    def Die(self, frame):
        self.lives -= 1
        self.fuel = 3000
        self.bombs = 30
        self.x = -380
        self.y = int(height/2)
        self.ControlsEnabled = False
        self.IsRespawning = True
        self.IsInvincible = True
        self.DiedOnFrame = frame

Player = PlayerPlane(-100, int(height/2))

Bullets = []
EnemyBullets = []

class Bullet:
    def __init__(self, x, y, horizspeed, vertspeed, firedby):
        self.sprite = laser
        self.rect = self.sprite.get_rect()
        self.x = x
        self.y = y
        self.horizspeed = horizspeed
        self.vertspeed = vertspeed
        self.firedby = firedby

EnemyBalloons = []

class WeatherBalloon:
    #SANS RIRE C'EST QUOI CE TRUC. On dirait des mines flottantes plus légères que l'air
    def __init__(self, x, y, horizspeed):
        self.sprite = balloon
        self.rect = self.sprite.get_rect()
        self.x = x
        self.y = y
        self.vertspeed = -1
        self.horizspeed = horizspeed
        self.maxvertspeed = randint(-5, -1)
        self.firedby = "Enemy"

Bombs = []
EnemyBombs = []

class PlayerBombs:
    def __init__(self, x, y, frame):
        self.sprite = bomb
        self.sprite = pygame.transform.scale(self.sprite, ((30,10)))
        self.rect = self.sprite.get_rect()
        self.x = x
        self.y = y
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top
        self.droppedOnFrame = frame

class EnemyBomb:
    def __init__(self, x, y, frame):
        self.sprite = bomb
        self.sprite = pygame.transform.flip(self.sprite, True, False)
        self.sprite = pygame.transform.scale(self.sprite, ((30,10)))
        self.rect = self.sprite.get_rect()
        self.x = x
        self.y = y
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top
        self.droppedOnFrame = frame

class ResupplyPlane:
    def __init__(self):
        self.sprite = pygame.image.load(os.path.join(os.getcwd(), "resources", "friendlyplane.png"))
        self.x = -100
        self.y = 50
        self.WhereToDrop = 0

Friendlies = [ResupplyPlane()]

class CarePackage:
    def __init__(self, x, y, vertspeed, sprite, points):
        self.x = x
        self.y = y
        self.vertspeed = 2
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
        self.pointsawarded = points

Enemies = []

class EnemyPlane:
    def __init__(self, y, frame):
        self.sprite = pygame.image.load(os.path.join(os.getcwd(), "resources", "enemytest.png"))
        self.rect = self.sprite.get_rect()
        self.x = width + 100
        self.y = y
        self.horizspeed = -5
        self.vertspeed = 0
        self.rect.topleft = ((self.x, self.y))
        self.width = self.rect.width
        self.height = self.rect.height
        self.FireOnFrame = frame + randint(60, 120)
        self.hitpoints = 1
        self.name = "Enemy"
    def Behave(self, frame):
        if self.x <= -100:
            self.x = width + 100
            self.y = randint(110, int((height * 5.9)/ 10))
        if frame == self.FireOnFrame:
            self.Fire(frame)
    def Fire(self, frame):
        EnemyBullets.append(Bullet(self.rect.left - 50, self.rect.centery -1, -10, 0, self.name))
        self.FireOnFrame = frame + randint(60, 120)
    def Die(self):
        Player.score += 150

class EnemyWeirdPlane:
    def __init__(self, y, frame):
        self.sprite = pygame.image.load(os.path.join(os.getcwd(), "resources", "enemytest.png"))
        self.sprite = pygame.transform.flip(self.sprite, True, False)
        self.x = width + 100
        self.y = y
        self.horizspeed = 0
        self.vertspeed = -3
        self.rect = self.sprite.get_rect()
        self.rect.topleft = ((self.x, self.y))
        self.width = self.rect.width
        self.height = self.rect.height
        self.FireOnFrame = frame + randint(60, 120)
        self.hitpoints = 1
        self.name = "Enemy"
    def Behave(self, frame):
        if self.x >= width - 121:
            if self.horizspeed >= -3 and frame % 10 == 0:
                self.horizspeed -=1 
            elif self.horizspeed == -3:
                pass
        if self.x <= int(width/2) + 100:
            if self.horizspeed <= 3 and frame % 10 == 0:
                self.horizspeed += 1

        if self.y <= 100 or self.y <= Player.y - 50:
            if self.vertspeed <= 3 and frame % 10 == 0:
                self.vertspeed += 1
        if self.y >= bgLayerRect.top - 200 or self.y >= Player.y + 75:
            if self.vertspeed >= -3 and frame % 10 == 0:
                self.vertspeed -= 1

        if frame == self.FireOnFrame:
            self.Fire(frame)
    def Fire(self, frame):
        EnemyBalloons.append(WeatherBalloon(self.rect.left - 50, self.rect.centery -1, randint(-5, -1)))
        self.FireOnFrame = frame + randint(30, 90)
    def Die(self):
        Player.score += 150
        
def CreateEnemies(ClassObject):
    Enemies.append(ClassObject)

class ObjectiveTank:
    def __init__(self):
        self.sprite = tank
        self.rect = self.sprite.get_rect()
        self.rect.bottom = bgLayerRect.top
        self.x = width + 100
        self.y = self.rect.top
        self.hitpoints = 5
        self.speed = 0
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top

Splosion = []

class Explosion:
    def __init__(self, x, y, who, frame):
        self.StartOnFrame = frame
        self.x = x
        self.y = y
        self.who = who
        self.width = 0
        self.height = 0
        self.sprite = pygame.image.load(os.path.join(os.getcwd(), "resources", "ExplosionFrame1.png"))
        if who == "Bomb": 
            self.width = 30
            self.height = 30
        elif who == "Player":
             self.width = 50
             self.height = 50
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

def SpawnExplosion(x, y, who, frame):
    Splosion.append(Explosion(x, y, who, frame))


class TOPSECRET:
    def __init__(self, frame):
        #self.sprite = vicviper
        self.sprite = pygame.image.load(os.path.join(os.getcwd(), "resources", "secret", "vicviper.png"))
        self.sprite = pygame.transform.flip(self.sprite, True, False)
        self.name = "Vic Viper"
        self.hitpoints = 64
        self.horizspeed = 0
        self.vertspeed = 0
        self.x = -1000
        self.y = 150
        self.rect = self.sprite.get_rect()
        self.rect.topleft = ((self.x, self.y))
        self.width = self.rect.width
        self.height = self.rect.height
        #Flags
        self.status = "Spawning"
        self.Cooldown = False
        #Chrono
        self.Timer = 0
        self.BombOnFrame = 0
        self.ShootOnFrame = 0
        self.CooldownActivatedOnFrame = 0
        self.Pattern = 0
        self.ChargeASecondTime = False
    def Behave(self, frame):
        if self.status == "Spawning":
            self.x += 10
            if self.x >= width + 100:
                self.status = "Idle"
                self.horizspeed = -5
                self.TimeAlive = 0
                self.ShootOnFrame = frame + randint(20,30)
        elif self.status == "Idle":
            if self.x >= Player.rect.x + 25:
                if self.horizspeed >= -5 and frame % 5 == 0:
                    self.horizspeed -= 1 
                elif self.horizspeed == -5:
                    pass
            if self.x <= Player.x + 25:
                if self.horizspeed <= 5 and frame % 5 == 0:
                    self.horizspeed += 1

            if self.y <= int(height/2) or self.y <= Player.y + 25:
                if self.vertspeed <= 6 and frame % 8 == 0:
                    self.vertspeed += 2
            if self.y >= int(height/2) or self.y >= Player.y +25:
                if self.vertspeed >= -6 and frame % 8 == 0:
                    self.vertspeed -= 2

            if self.rect.bottom >= bgLayerRect.top:
                self.rect.bottom = bgLayerRect.top

            if self.status == "Idle" and Player.x >= self.x:
                if frame == self.ShootOnFrame:
                    if self.hitpoints >= 50:
                        self.FireForwards(frame)
                    elif self.hitpoints < 50 and self.hitpoints >= 20:
                        self.FireDoubleForwards(frame)
                    elif self.hitpoints < 20:
                        self.FireTripleForwards(frame)
            elif self.status == "Idle" and Player.x <= self.x:
                if frame == self.ShootOnFrame:
                    if self.hitpoints >= 50:
                        self.FireBackwards(frame)
                    elif self.hitpoints < 50 and self.hitpoints >= 20:
                        self.FireDoubleBackwards(frame)
                    elif self.hitpoints < 20:
                        self.FireTripleBackwards(frame)
        elif self.status == "Bombing":
            self.y = 40
            self.horizspeed = -5
            if self.x <= width and self.x >= width - 6 and self.BombOnFrame == 0:
                self.BombOnFrame = frame + 10
            if self.x <= -100:
                self.status = "Idle"
                self.horizspeed = 5
                self.y = Player.y + 25
                Splosion.clear()
                self.Timer = 0
                self.BombOnFrame = 0
                self.ShootOnFrame = frame + randint(20,35)
                self.sprite = pygame.transform.flip(self.sprite, True, False)
        elif self.status == "Charging":
            if self.y == 0:
                self.y = Player.y
            else:
                pass
            self.vertspeed = 0
            self.horizspeed = -20
            if self.x <= -100:
                self.status = "Idle"
                self.horizspeed = 5
                self.y = Player.y
                Splosion.clear()
                self.Timer = 0
                self.BombOnFrame = 0
                self.ShootOnFrame = frame + randint(20,35)
                self.sprite = pygame.transform.flip(self.sprite, True, False)
        elif self.status == "DoubleCharge":
            if self.y == 0:
                self.y = Player.y
            else:
                pass
            self.vertspeed = 0
            if self.ChargeASecondTime == False:
                self.horizspeed = -20
            else:
                self.horizspeed = 20
            if self.x < -150:
                self.ChargeASecondTime = True
                self.x = -100
                self.y = Player.y
                self.sprite = pygame.transform.flip(self.sprite, True, False)

            if self.x >= width + 100 and self.ChargeASecondTime == True:
                self.status = "Idle"
                self.horizspeed = -5
                self.y = Player.y
                Splosion.clear()
                self.Timer = 0
                self.BombOnFrame = 0
                self.ShootOnFrame = frame + randint(20,35)
                self.ChargeASecondTime = False
   
        self.Timer += 1

        if self.Timer % 480 == 0 and self.status == "Idle":
            self.status = "ExitScreen"
            self.vertspeed = 0

        if self.status == "ExitScreen" and self.x < width + 100:
            self.horizspeed = 10
        elif self.status == "ExitScreen" and self.x >= width + 100:
            self.Pattern = randint(1, 3)
            if self.Pattern == 1:
                self.status = "Bombing"
                self.x = width
                self.sprite = pygame.transform.flip(self.sprite, True, False)
            elif self.Pattern == 2:
                self.status = "Charging"
                self.y = 0
                self.x = width
                self.sprite = pygame.transform.flip(self.sprite, True, False)
            elif self.Pattern == 3:
                self.status = "DoubleCharge"
                self.y = 0
                self.x = width
                self.sprite = pygame.transform.flip(self.sprite, True, False)

        if self.status == "Bombing" and frame == self.BombOnFrame:
            self.FireBombs(frame)

        if frame >= self.CooldownActivatedOnFrame + 30:
            self.Cooldown = False
            
    def FireForwards(self, frame):
        if Player.IsInvincible == False:
            EnemyBullets.append(Bullet(self.rect.left + 50, self.rect.centery -1, 10, int(self.vertspeed/2), self.name))
        else: pass
        self.ShootOnFrame = frame + 30
    def FireDoubleForwards(self, frame):
        if Player.IsInvincible == False:
            EnemyBullets.append(Bullet(self.rect.left + 50, self.rect.centery -1, 10, 2, self.name))
            EnemyBullets.append(Bullet(self.rect.left + 50, self.rect.centery -1, 10, -2, self.name))
        else: pass
        self.ShootOnFrame = frame + 38
    def FireTripleForwards(self, frame):
        if Player.IsInvincible == False:
            EnemyBullets.append(Bullet(self.rect.left + 50, self.rect.centery -1, 10, 5, self.name))
            EnemyBullets.append(Bullet(self.rect.left + 50, self.rect.centery -1, 10, 0, self.name))
            EnemyBullets.append(Bullet(self.rect.left + 50, self.rect.centery -1, 10, -5, self.name))
        else: pass
        self.ShootOnFrame = frame + 45
        
    def FireBackwards(self, frame):
        if Player.IsInvincible == False:
            EnemyBullets.append(Bullet(self.rect.left - 50, self.rect.centery -1, -10, int(self.vertspeed/2), self.name))
        else: pass
        self.ShootOnFrame = frame + 30
    def FireDoubleBackwards(self, frame):
        if Player.IsInvincible == False:
            EnemyBullets.append(Bullet(self.rect.left - 50, self.rect.centery -1, -10, 2, self.name))
            EnemyBullets.append(Bullet(self.rect.left - 50, self.rect.centery -1, -10, -2, self.name))
        else: pass
        self.ShootOnFrame = frame + 38
    def FireTripleBackwards(self, frame):
        if Player.IsInvincible == False:
            EnemyBullets.append(Bullet(self.rect.left - 50, self.rect.centery -1, -10, 5, self.name))
            EnemyBullets.append(Bullet(self.rect.left - 50, self.rect.centery -1, -10, 0, self.name))
            EnemyBullets.append(Bullet(self.rect.left - 50, self.rect.centery -1, -10, -5, self.name))
        else: pass
        self.ShootOnFrame = frame + 45
        
    def FireBombs(self, frame):
        EnemyBombs.append(EnemyBomb(self.rect.left, self.rect.bottom, frame))
        self.BombOnFrame = frame + 13
    def Die(self):
        Player.score += 10000
