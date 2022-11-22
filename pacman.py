from board import boards
import copy
import pygame
import math


pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont('Comic Sans', 20)
level = copy.deepcopy(boards)
color = 'blue'
pi = math.pi

#player set up
playerImages = []
for i in range(1, 5):
    playerImages.append(pygame.transform.scale(pygame.image.load(f'player/{i}.png'), (45,45)))
playerX = 450
playerY = 663
playerSpeed = 2

#ghost set ups
blinkyIMG = pygame.transform.scale(pygame.image.load(f'Ghosts/Red.png'), (45, 45))
blinkyX = 56
blinkyY = 58
blinkyDirection = 0
blinkyDead = False
blinkyBox = False
inkyIMG = pygame.transform.scale(pygame.image.load(f'Ghosts/Blue.png'), (45, 45))
inkyX = 440
inkyY = 388
inkyDirection = 2
inkyDead = False
inkyBox = False
pinkyIMG = pygame.transform.scale(pygame.image.load(f'Ghosts/Pink.png'), (45, 45))
pinkyX = 390
pinkyY = 438
pinkyDirection = 2
pinkyDead = False
pinkyBox = False
clydeIMG = pygame.transform.scale(pygame.image.load(f'Ghosts/Orange.png'), (45, 45))
clydeX = 440
clydeY = 438
clydeDirection = 2
clydeDead = False
clydeBox = False
fearGhost = pygame.transform.scale(pygame.image.load(f'Ghosts/PowerUP.png'), (45, 45))
deadGhost = pygame.transform.scale(pygame.image.load(f'Ghosts/Dead.png'), (45, 45))

target = [(playerX, playerY), (playerX, playerY), (playerX, playerY), (playerX, playerY)]
ghostSpeeds = [2, 2, 2, 2]



powerUp = False 
powerUpTime = 0
eatenGhost = [False, False, False, False]
moving = False
startUpTimer = 0

direction = 0
directionCommand = 0
counter = 0
flicker = False

score = 0
lives = 3
gameOver = False
gameWin = False

class Ghost:
    def __init__(self, coordX, coordY, target, speed, img, direction, dead, box, id):
        self.posX = coordX
        self.posY = coordY
        self.centerX = self.posX + 22
        self.centerY = self.posY + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direction
        self.dead = dead
        self.inBox = box
        self.id = id
        self.turns, self.inBox = self.checkCollisions()
        self.rect = self.draw()
    
    def draw(self):
        if (not powerUp and not self.dead) or (eatenGhost[self.id] and powerUp and not self.dead):
            screen.blit(self.img, (self.posX, self.posY))
        elif powerUp and not self.dead and not eatenGhost[self.id]:
            screen.blit(fearGhost, (self.posX, self.posY))
        else:
            screen.blit(deadGhost, (self.posX, self.posY))
        ghostRect = pygame.rect.Rect((self.centerX - 18, self.centerY - 18), (36, 36))
        return ghostRect

    def checkCollisions(self):
        num1 = ((HEIGHT-50)//32)
        num2 = (WIDTH//30)
        num3 = 20
        self.turns = [False, False, False, False]
        if 0 < self.centerX // 30 < 29:
            if level[(self.centerY - num3)//num1][self.centerX//num2] == 9:
                self.turns[2] = True
            if level[self.centerY//num1][(self.centerX-num3)//num2 ]< 3 or level[self.centerY//num1][(self.centerX-num3)//num2] == 9 and (self.inBox or self.dead):
                self.turns[1] = True
            if level[self.centerY//num1][(self.centerX+num3)//num2 ]< 3 or level[self.centerY//num1][(self.centerX+num3)//num2] == 9 and (self.inBox or self.dead):
                self.turns[0] = True
            if level[(self.centerY + num3)//num1][self.centerX//num2 ] < 3 or level[(self.centerY+num3)//num1][self.centerX//num2] == 9 and (self.inBox or self.dead):
                self.turns[3] = True
            if level[(self.centerY - num3)//num1][self.centerX//num2] <3 or level[(self.centerY-num3)//num1][self.centerX//num2] == 9 and (self.inBox or self.dead):
                self.turns[2] = True
            
            if self.direction == 2 or self.direction == 3:
                if 12 <= self.centerX % num2 <=18:
                    if level[(self.centerY + num3)//num1][self.centerX//num2] < 3 or level[(self.centerY + num3)//num1][self.centerX//num2] == 9 and (self.inBox or self.dead):
                        self.turns[3] = True
                if 12 <= self.centerX % num2 <=18:
                    if level[(self.centerY - num3)//num1][self.centerX//num2] < 3 or level[(self.centerY - num3)//num1][self.centerX//num2] == 9 and (self.inBox or self.dead):
                        self.turns[2] = True
                if 12 <= self.centerY % num1 <=18:
                    if level[self.centerY//num1][(self.centerX + num2)//num2] < 3 or level[self.centerY//num1][(self.centerX + num2)//num2] == 9 and (self.inBox or self.dead):
                        self.turns[0] = True
                if 12 <= self.centerY % num1 <=18:
                    if level[self.centerY//num1][(self.centerX - num2)//num2] < 3 or level[self.centerY//num1][(self.centerX - num2)//num2] == 9 and (self.inBox or self.dead):
                        self.turns[1] = True
            
            if self.direction == 1 or self.direction == 0:
                if 12 <= self.centerX % num2 <=18:
                    if level[(self.centerY + num3)//num1][self.centerX//num2] < 3 or level[(self.centerY + num3)//num1][self.centerX//num2] == 9 and (self.inBox or self.dead):
                        self.turns[3] = True
                if 12 <= self.centerX % num2 <=18:
                    if level[(self.centerY - num3)//num1][self.centerX//num2] < 3 or level[(self.centerY - num3)//num1][self.centerX//num2] == 9 and (self.inBox or self.dead):
                        self.turns[2] = True

                if 12 <= self.centerY % num1 <=18:
                    if level[self.centerY//num1][(self.centerX + num3)//num2] < 3 or level[self.centerY//num1][(self.centerX + num3)//num2] == 9 and (self.inBox or self.dead):
                        self.turns[0] = True
                if 12 <= self.centerY % num1 <=18: 
                    if level[self.centerY//num1][(self.centerX - num3)//num2] < 3 or level[self.centerY//num1][(self.centerX - num3)//num2] == 9 and (self.inBox or self.dead):
                        self.turns[1] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        
        if 350 < self.posX < 545 and 370 < self.posY < 480:
            self.inBox = True
        else:
            self.inBox = False
        return self.turns, self.inBox

    def moveClyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.posX and self.turns[0]:
                self.posX += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                if self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                else:
                    self.posX += self.speed
        elif self.direction == 1:
            if self.target[1] > self.posY and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.posX and self.turns[1]:
                self.posX -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
            elif self.turns[1]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                if self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                else:
                    self.posX -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.posX and self.turns[1]:
                self.direction = 1
                self.posX -= self.speed
            elif self.target[1] < self.posY and self.turns[2]:
                self.direction = 2
                self.posY -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
            elif self.turns[2]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                else:
                    self.posY -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.posY and self.turns[3]:
                self.posY += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
            elif self.turns[3]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                else:
                    self.posY += self.speed
        if self.posX < -30:
            self.posX = 900
        elif self.posX > 900:
            self.posX = -30
        return self.posX, self.posY, self.direction

    def moveBlinky(self):
        if self.direction == 0:
            if self.target[0] > self.posX and self.turns[0]:
                self.posX += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
            elif self.turns[0]:
                self.posX += self.speed
        elif self.direction == 1:
            if self.target[0] < self.posX and self.turns[1]:
                self.posX -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
            elif self.turns[1]:
                self.posX -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.posY and self.turns[2]:
                self.direction = 2
                self.posY -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
            elif self.turns[2]:
                self.posY -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.posY and self.turns[3]:
                self.posY += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
            elif self.turns[3]:
                self.posY += self.speed
        if self.posX < -30:
            self.posX = 900
        elif self.posX > 900:
            self.posX =- 30
        return self.posX, self.posY, self.direction

    def moveInky(self):
        if self.direction == 0:
            if self.target[0] > self.posX and self.turns[0]:
                self.posX += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                if self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                else:
                    self.posX += self.speed
        elif self.direction == 1:
            if self.target[1] > self.posY and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.posX and self.turns[1]:
                self.posX -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
            elif self.turns[1]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                if self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                else:
                    self.posX -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.posY and self.turns[2]:
                self.direction = 2
                self.posY -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
            elif self.turns[2]:
                self.posY -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.posY and self.turns[3]:
                self.posY += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
            elif self.turns[3]:
                self.posY += self.speed
        if self.posX < -30:
            self.posX = 900
        elif self.posX > 900:
            self.posX = -30
        return self.posX, self.posY, self.direction

    def movePinky(self):
        if self.direction == 0:
            if self.target[0] > self.posX and self.turns[0]:
                self.posX += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
            elif self.turns[0]:
                self.posX += self.speed
        elif self.direction == 1:
            if self.target[1] > self.posY and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.posX and self.turns[1]:
                self.posX -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
            elif self.turns[1]:
                self.posX -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.posX and self.turns[1]:
                self.direction = 1
                self.posX -= self.speed
            elif self.target[1] < self.posY and self.turns[2]:
                self.direction = 2
                self.posY -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.target[1] > self.posY and self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.posY += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
            elif self.turns[2]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                else:
                    self.posY -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.posY and self.turns[3]:
                self.posY += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.target[1] < self.posY and self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.posY -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
            elif self.turns[3]:
                if self.target[0] > self.posX and self.turns[0]:
                    self.direction = 0
                    self.posX += self.speed
                elif self.target[0] < self.posX and self.turns[1]:
                    self.direction = 1
                    self.posX -= self.speed
                else:
                    self.posY += self.speed
        if self.posX < -30:
            self.posX = 900
        elif self.posX > 900:
            self.posX = -30
        return self.posX, self.posY, self.direction

def drawScoreBoard():
    scoreText = font.render(f'Score: {score}', True, 'white')
    screen.blit(scoreText, (10, 920))
    if powerUp:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(playerImages[0], (30,30)), [650 + i*40, 915])
    if gameOver:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 780, 280], 0, 10)
        overText = font.render('Game Over! Press spacebar to restart!', True, 'red')
        screen.blit(overText, (100, 300))
    if gameWin:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 780, 280], 0, 10)
        overText = font.render('Congratioulations, you Won! Press spacebar to restart!', True, 'green')
        screen.blit(overText, (100, 300))
        

def checkCollision(score, buff, buffTime, eatenGhost):
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    if 0 < playerX < 870:
        if level[centerY//num1][centerX//num2] == 1:
            level[centerY//num1][centerX//num2] = 0
            score += 10
        if level[centerY//num1][centerX//num2] == 2:
            level[centerY//num1][centerX//num2] = 0
            score += 50
            buff = True
            buffTime = 0
            eatenGhost = [False, False, False, False]

    return score, buff, buffTime, eatenGhost

def drawBoard():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):         #goes through rows
        for j in range(len(level[i])):  #goes through collumns in each row
            if level[i][j] == 1:   
                pygame.draw.circle(screen, 'white', [(j * num2 + (0.5 * num2)), (i * num1 + (0.5 * num1))], 4)  #small dot
            
            elif level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', [(j * num2 + (0.5 * num2)), (i * num1 + (0.5 * num1))], 10) #big dot
            
            elif level[i][j] == 3:
                pygame.draw.line(screen, color, [j*num2+(0.5*num2), i*num1], [j*num2+(0.5*num2), i*num1+num1], 3)   #vertical blue          
            
            elif level[i][j] == 4:
                pygame.draw.line(screen, color, [j*num2, i*num1 +(0.5*num1)], [j*num2+num2, i*num1+(0.5*num1)], 3)  #horizontal blue        
            
            elif level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j*num2 - (num2 *0.4)) - 2, (i*num1 + (0.5*num1)), num2, num1], 0, pi/2, 3)  #type: ignore      #top right corners
            
            elif level[i][j] == 6:
                pygame.draw.arc(screen, color, [(j*num2 + (num2 *0.5)), (i*num1 + (0.5*num1)), num2, num1], pi/2, pi, 3)  #type: ignore     #top left corners
            
            elif level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j*num2 + (num2 *0.5)), (i*num1 - (0.4*num1)), num2, num1], pi, 3*pi/2, 3)  #type: ignore   #lower left corners
            
            elif level[i][j] == 8:
                pygame.draw.arc(screen, color, [(j*num2 - (num2 *0.4))-2, (i*num1 - (0.4*num1)), num2, num1], 3*pi/2, 2*pi, 3)  #type: ignore #lower right corners
            
            elif level[i][j] == 9:
                pygame.draw.line(screen, 'white', [j*num2, i*num1 +(0.5*num1)], [j*num2+num2, i*num1+(0.5*num1)], 3)

def drawPlayer():
    if direction == 0:  #right
        screen.blit(playerImages[counter // 5], (playerX, playerY))
    elif direction == 1:  #lef
        screen.blit(pygame.transform.flip(playerImages[counter // 5], True, False), (playerX, playerY))
    elif direction == 2:  #up
        screen.blit(pygame.transform.rotate(playerImages[counter // 5], 90), (playerX, playerY))
    elif direction == 3:  #dow
        screen.blit(pygame.transform.rotate(playerImages[counter // 5], -90), (playerX, playerY))

def checkPosition(centerx, centery):
    turns = [False, False, False, False]
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    num3 = 15
    if centerx//30 < 29:
        if direction == 0:
            if level[centery//num1][(centerx - num3)// num2] <3:
                turns[1] = True
        if direction == 1:
            if level[centery//num1][(centerx + num3)// num2] <3:
                turns[0] = True
        if direction == 2:
            if level[(centery+num3)//num1][centerx// num2] <3:
                turns[3] = True
        if direction == 3:
            if level[(centery-num3)//num1][centerx// num2] <3:
                turns[2] = True
        
        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery+num3)//num1][centerx// num2] < 3:
                    turns[3] = True
                if level[(centery-num3)//num1][centerx// num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery//num1][(centerx-num2)// num2] < 3:
                    turns[1] = True
                if level[centery//num1][(centerx+num2)// num2] < 3:
                    turns[0] = True
        
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery+num1)//num1][centerx// num2] < 3:
                    turns[3] = True
                if level[(centery-num1)//num1][centerx// num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery//num1][(centerx-num3)// num2] < 3:
                    turns[1] = True
                if level[centery//num1][(centerx+num3)// num2] < 3:
                    turns[0] = True
            
    else:
        turns[0] = True
        turns[1] = True
    return turns

def movePlayer(X, Y):
    if direction == 0 and validTurns[0]:
        X += playerSpeed
    elif direction == 1 and validTurns[1]:
        X -= playerSpeed
    elif direction == 2 and validTurns[2]:
        Y -= playerSpeed
    elif direction == 3 and validTurns[3]:
        Y += playerSpeed
    return X, Y

def getTargets(blinkyX, blinkyY, inkyX, inkyY, pinkyX, pinkyY, clydeX, clydeY):
    if playerX < 450:
        runawayX = 900
    else:
        runawayX = 0
    if playerY < 450:
        runawayY = 900
    else:
        runawayY = 0
    returnTarget = (380,400)
    if powerUp:
        if not blinkyDead and not eatenGhost[0]:
            blinkyTarget = (runawayX, runawayY)
        elif not blinky.dead and eatenGhost[0]:
            if blinky.inBox:
                blinkyTarget = (400, 100)
            else: 
                blinkyTarget = (playerX, playerY)
        else:
            blinkyTarget = returnTarget
        if not inkyDead and not eatenGhost[1]:
            inkyTarget = (runawayX, playerY)
        elif not inky.dead and eatenGhost[1]:
            if inky.inBox:
                inkyTarget = (400, 100)
            else: 
                inkyTarget = (playerX, playerY)
        else:
            inkyTarget = returnTarget
        if not pinkyDead and not eatenGhost[2]:
            pinkyTarget = (playerX, runawayY)
        elif not pinky.dead and eatenGhost[2]:
            if pinky.inBox:
                pinkyTarget = (400, 100)
            else: 
                pinkyTarget = (playerX, playerY)
        else:
            pinkyTarget = returnTarget
        if not clydeDead and not eatenGhost[3]:
            clydeTarget = (450, 450)
        elif not clyde.dead and eatenGhost[3]:
            if clyde.inBox:
                clydeTarget = (400, 100)
            else: 
                clydeTarget = (playerX, playerY)
        else:
            clydeTarget = returnTarget
    else:
        if not blinkyDead:
            if 340 < blinkyX < 560 and 340 < blinkyY < 500:
                blinkyTarget = (400,100)
            else:
                blinkyTarget = (playerX, playerY)
        else:
            blinkyTarget = returnTarget
        if not inkyDead:
            if 340 < inkyX < 560 and 340 < inkyY < 500:
                inkyTarget = (400,100)
            else:
                inkyTarget = (playerX, playerY)
        else:
            inkyTarget = returnTarget
        if not pinkyDead:
            if 340 < pinkyX < 560 and 340 < pinkyY < 500:
                pinkyTarget = (400,100)
            else:
                pinkyTarget = (playerX, playerY)
        else:
            pinkyTarget = returnTarget
        if not clydeDead:
            if 340 < clydeX < 560 and 340 < clydeY < 500:
                clydeTarget = (400,100)
            else:
                clydeTarget = (playerX, playerY)
        else:
            clydeTarget = returnTarget
    
    return [blinkyTarget, inkyTarget, pinkyTarget, clydeTarget]

run = True
while run:
    gameWin = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            gameWin = False
            

    screen.fill('black')
    drawBoard()
    timer.tick(fps)

    if counter < 19:
        counter += 1
        if counter > 10:
            flicker = False
    else:
        counter = 0
        flicker = True
    targets = getTargets(blinkyX, blinkyY, inkyX, inkyY, pinkyX, pinkyY, clydeX, clydeY)
    blinky = Ghost(blinkyX, blinkyY, targets[0], ghostSpeeds[0], blinkyIMG, blinkyDirection, blinkyDead, blinkyBox, 0)
    inky = Ghost(inkyX, inkyY, targets[1], ghostSpeeds[1], inkyIMG, inkyDirection, inkyDead, inkyBox, 1)
    pinky = Ghost(pinkyX, pinkyY, targets[2], ghostSpeeds[2], pinkyIMG, pinkyDirection, pinkyDead, pinkyBox, 2)
    clyde = Ghost(clydeX, clydeY, targets[3], ghostSpeeds[3], clydeIMG, clydeDirection, clydeDead, clydeBox, 3)
    
    if powerUp and powerUpTime < 600:
        powerUpTime += 1
    elif powerUp and powerUpTime >= 600:
        powerUp = False
        eatenGhost = [False, False, False, False]

    if startUpTimer < 180 and not gameOver and not gameWin:
        moving = False
        startUpTimer += 1
    else:
        moving = True
    
    centerX = playerX + 23
    centerY = playerY + 24
    for i in range(4):
        if powerUp and not eatenGhost[i]:
            ghostSpeeds[i] = 1
        else:
            ghostSpeeds[i] = 2
    if blinky.dead:
        ghostSpeeds[0] = 4
    if inky.dead:
        ghostSpeeds[1] = 4
    if pinky.dead:
        ghostSpeeds[2] = 4
    if clyde.dead:
        ghostSpeeds[3] = 4
    
    
    
    playerCircle = pygame.draw.circle(screen, 'black', (centerX, centerY), 20, 2)
    drawPlayer()
    
    drawScoreBoard()

    validTurns = checkPosition(centerX, centerY)
    if moving:
        playerX, playerY = movePlayer(playerX, playerY)
        if not blinkyDead and not blinky.inBox:
            blinkyX, blinkyY, blinkyDirection = blinky.moveBlinky()
        else:
            blinkyX, blinkyY, blinkyDirection = blinky.moveClyde()
        if not inkyDead and not inky.inBox:
            inkyX, inkyY, inkyDirection = inky.moveInky()
        else:
            inkyX, inkyY, inkyDirection = inky.moveClyde()
        if not pinkyDead and not pinky.inBox:
            pinkyX, pinkyY, pinkyDirection = pinky.movePinky()
        else:
            pinkyX, pinkyY, pinkyDirection = pinky.moveClyde()
        clydeX, clydeY, clydeDirection = clyde.moveClyde()
    score, powerUp, powerUpTime, eatenGhost = checkCollision(score, powerUp, powerUpTime, eatenGhost)

    if not powerUp:
        if (playerCircle.colliderect(blinky.rect) and not blinky.dead) or (playerCircle.colliderect(inky.rect) and not blinky.dead) \
            or (playerCircle.colliderect(pinky.rect) and not pinky.dead) or (playerCircle.colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:
                lives -= 1
                powerUp = False
                powerUpTime = 0
                startUpTimer = 0
                playerX = 450
                playerY = 663
                direction = 0
                directionCommand = 0
                blinkyX = 56
                blinkyY = 58
                blinkyDirection = 0
                inkyX = 440
                inkyY = 388
                inkyDirection = 2
                pinkyX = 440
                pinkyY = 438
                pinkyDirection = 2
                clydeX = 440
                clydeY = 438
                clydeDirection = 2
                eatenGhost = [False, False, False, False]
                blinkyDead = False
                inkyDead = False
                pinkyDead = False
                clydeDead = False
            else:
                gameOver = True
                moving = False
                startUpTimer = 0
    if powerUp and playerCircle.colliderect(blinky.rect) and eatenGhost[0] and not blinky.dead:
        if lives > 0:
            lives -= 1
            powerUp = False
            powerUpTime = 0
            startUpTimer = 0
            playerX = 450
            playerY = 663
            direction = 0
            directionCommand = 0
            blinkyX = 56
            blinkyY = 58
            blinkyDirection = 0
            inkyX = 440
            inkyY = 388
            inkyDirection = 2
            pinkyX = 440
            pinkyY = 438
            pinkyDirection = 2
            clydeX = 440
            clydeY = 438
            clydeDirection = 2
            eatenGhost = [False, False, False, False]
            blinkyDead = False
            inkyDead = False
            pinkyDead = False
            clydeDead = False
        else:
            gameOver = True
            moving = False
            startUpTimer = 0
    if powerUp and playerCircle.colliderect(inky.rect) and eatenGhost[1]and not inky.dead:
        if lives > 0:
            lives -= 1
            powerUp = False
            powerUpTime = 0
            startUpTimer = 0
            playerX = 450
            playerY = 663
            direction = 0
            directionCommand = 0
            blinkyX = 56
            blinkyY = 58
            blinkyDirection = 0
            inkyX = 440
            inkyY = 388
            inkyDirection = 2
            pinkyX = 440
            pinkyY = 438
            pinkyDirection = 2
            clydeX = 440
            clydeY = 438
            clydeDirection = 2
            eatenGhost = [False, False, False, False]
            blinkyDead = False
            inkyDead = False
            pinkyDead = False
            clydeDead = False
        else:
            gameOver = True
            moving = False
            startUpTimer = 0
    if powerUp and playerCircle.colliderect(pinky.rect) and eatenGhost[2]and not pinky.dead:
        if lives > 0:
            lives -= 1
            powerUp = False
            powerUpTime = 0
            startUpTimer = 0
            playerX = 450
            playerY = 663
            direction = 0
            directionCommand = 0
            blinkyX = 56
            blinkyY = 58
            blinkyDirection = 0
            inkyX = 440
            inkyY = 388
            inkyDirection = 2
            pinkyX = 440
            pinkyY = 438
            pinkyDirection = 2
            clydeX = 440
            clydeY = 438
            clydeDirection = 2
            eatenGhost = [False, False, False, False]
            blinkyDead = False
            inkyDead = False
            pinkyDead = False
            clydeDead = False
        else:
            gameOver = True
            moving = False
            startUpTimer = 0
    if powerUp and playerCircle.colliderect(clyde.rect) and eatenGhost[3]and not clyde.dead:
        if lives > 0:
            lives -= 1
            powerUp = False
            powerUpTime = 0
            startUpTimer = 0
            playerX = 450
            playerY = 663
            direction = 0
            directionCommand = 0
            blinkyX = 56
            blinkyY = 58
            blinkyDirection = 0
            inkyX = 440
            inkyY = 388
            inkyDirection = 2
            pinkyX = 440
            pinkyY = 438
            pinkyDirection = 2
            clydeX = 440
            clydeY = 438
            clydeDirection = 2
            eatenGhost = [False, False, False, False]
            blinkyDead = False
            inkyDead = False
            pinkyDead = False
            clydeDead = False
        else:
            gameOver = True
            moving = False
            startUpTimer = 0
    if powerUp and playerCircle.colliderect(blinky.rect) and not blinky.dead and not eatenGhost[0]:
        blinkyDead = True
        eatenGhost[0] = True
        score += (2** eatenGhost.count(True)) * 100
    if powerUp and playerCircle.colliderect(inky.rect) and not inky.dead and not eatenGhost[1]:
        inkyDead = True
        eatenGhost[1] = True
        score += (2** eatenGhost.count(True)) * 100
    if powerUp and playerCircle.colliderect(pinky.rect) and not pinky.dead and not eatenGhost[2]:
        pinkyDead = True
        eatenGhost[2] = True
        score += (2** eatenGhost.count(True)) * 100
    if powerUp and playerCircle.colliderect(clyde.rect) and not clyde.dead and not eatenGhost[3]:
        clydeDead = True
        eatenGhost[3] = True
        score += (2** eatenGhost.count(True)) * 100
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                directionCommand = 0
            if event.key == pygame.K_LEFT:
                directionCommand = 1
            if event.key == pygame.K_UP:
                directionCommand = 2
            if event.key == pygame.K_DOWN:
                directionCommand = 3
            if event.key == pygame.K_SPACE and (gameOver or gameWin):
                lives = 3
                powerUp = False
                powerUpTime = 0
                startUpTimer = 0
                playerX = 450
                playerY = 663
                direction = 0
                directionCommand = 0
                blinkyX = 56
                blinkyY = 58
                blinkyDirection = 0
                inkyX = 440
                inkyY = 388
                inkyDirection = 2
                pinkyX = 440
                pinkyY = 438
                pinkyDirection = 2
                clydeX = 440
                clydeY = 438
                clydeDirection = 2
                eatenGhost = [False, False, False, False]
                blinkyDead = False
                inkyDead = False
                pinkyDead = False
                clydeDead = False
                score = 0
                level = copy.deepcopy(boards)
                gameOver = False
                gameWin = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and directionCommand == 0:
                directionCommand = direction
            if event.key == pygame.K_LEFT and directionCommand == 1:
                directionCommand = direction
            if event.key == pygame.K_UP and directionCommand == 2:
                directionCommand = direction
            if event.key == pygame.K_DOWN and directionCommand == 3:
                directionCommand = direction
    for i in range(4):
        if directionCommand == i and validTurns[i]:
            direction = i
    
    if playerX > 900:
        playerX = -47
    elif playerX < -50:
        playerX = 897
    
    if blinky.dead and blinky.inBox:
        blinkyDead = False
    if inky.dead and inky.inBox:
        inkyDead = False
    if pinky.dead and pinky.inBox:
        pinkyDead = False
    if clyde.dead and clyde.inBox:
        clydeDead = False

    pygame.display.flip()
pygame.quit()