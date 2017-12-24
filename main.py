#Packages
import pygame
import random
import time
from serial import *
from scipy.interpolate import interp1d

#Colors
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (135,206,250)
ORANGE = (255,165,0)
colors = [RED,BLUE,BLACK,WHITE,ORANGE]

#Screen Definitions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

#BLock Definitions
BLOCK_SIZE = 10

#Gesture Control Factors
SENSITIVITY_AND_STABILITY_FACTOR = 300

#Pygame Initializations
pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
t1 = time.time()

#Serial Input and Mapping
ser = Serial('COM4', 9600, timeout=0)
mapdistopix = interp1d([10,30],[0,SCREEN_WIDTH])

#Display
gameDisplay = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
pygame.display.set_caption("DX-Ball")

#Displaying message to screen
font = pygame.font.SysFont(None, 25)
def message_to_screen(msg, color,pos):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, pos)
    
#Class Definitions
def Paddle(lead_x,lead_y,factor):
    pygame.draw.rect(gameDisplay, BLACK, [lead_x,lead_y,factor*BLOCK_SIZE,BLOCK_SIZE])

class Block():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color

class Ball():
    def __init__(self,x,y,color,velocity):
        self.x = x
        self.y = y
        self.color = color
        self.vel = velocity
    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x,self.y,BLOCK_SIZE,BLOCK_SIZE])
        pygame.display.update()

class PowerUp():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
    
#Crete blocks
block_list =[]
for x in range(30):
    x = random.randrange(0,SCREEN_WIDTH-BLOCK_SIZE)
    y = random.randrange(0,SCREEN_HEIGHT-3*BLOCK_SIZE)
    color = RED
    #Create power up blocks
    pon = random.randint(0,15)
    if pon < 3:
        color = ORANGE
    p1 = Block(x,y,color)
    if (x,y) not in block_list:
        block_list.append(p1)


def MainMenu():
    #Background image
    img=pygame.image.load("Main_Menu.jpg")
    img=pygame.transform.scale(img,(SCREEN_WIDTH,SCREEN_HEIGHT))
    gameDisplay.blit(img,(0,0))
    
    global t1
    
    #Crete Bouncing balls
    BallList = []
    ball_vel_x = 5
    ball_vel_y = -5
    for x in range(10):
        ball_x = random.randrange(0,SCREEN_WIDTH-BLOCK_SIZE,10)
        ball_y = random.randrange(0,SCREEN_HEIGHT-BLOCK_SIZE,10)
        color = random.choice(colors)
        b1 = Ball(ball_x,ball_y,color,[ball_vel_x,ball_vel_y])
        BallList.append(b1)
        
    #Main Menu Event Handling
    StayInMenu = True
    while StayInMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                StayInMenu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
               if 90 < event.pos[0] < 136 and 317 < event.pos[1] < 327:
                   StayInMenu = False
                   #Display of pygame powered
                   gameDisplay.fill(WHITE)
                   img1 = pygame.image.load("pygame_powered.png")
                   gameDisplay.blit(img1,(SCREEN_WIDTH//4-40,SCREEN_HEIGHT//4))
                   pygame.display.update()
                   time.sleep(3)
                   
                   #Entering Game
                   t1 = time.time()
                   gameLoop()
                   
        #Update bouncing balls
        for ball in BallList:
            if ball.x == SCREEN_WIDTH-BLOCK_SIZE or ball.x == BLOCK_SIZE:
                ball.vel[0] = -ball.vel[0]
            if ball.y == BLOCK_SIZE or ball.y ==SCREEN_HEIGHT-BLOCK_SIZE:
                ball.vel[1] = -ball.vel[1]
            ball.x += ball.vel[0]
            ball.y += ball.vel[1]
            gameDisplay.blit(img,(0,0))
            ball.draw()
            pygame.display.update()

#Main Game Logic
def gameLoop():

    #Loading Sounds
    sounda = pygame.mixer.Sound("beep.wav")
    soundp = pygame.mixer.Sound("PowerUp.wav")

    #Game Over and Exit Variables
    gameExit = False
    gameOver = False
    
    #Paddle Initializations
    lead_x = SCREEN_WIDTH//2
    lead_y = SCREEN_HEIGHT-30
    lead_x_change = 0

    #Score Mainitainance
    scoreVal = 0
    
    #Power Up Variables
    PowerUpList = []
    paddle_size = 5
        
    #Ball Initializations
    ball_x = random.randrange(0,SCREEN_WIDTH-BLOCK_SIZE,10)
    ball_y = random.randrange(0,SCREEN_HEIGHT-BLOCK_SIZE,10)
    ball_vel_x = 1
    ball_vel_y = -1
    b1 = Ball(ball_x,ball_y,BLUE,[ball_vel_x,ball_vel_y])
    
    #Main Game Loop
    while not gameExit:
        
        #Game Over Handling
        while gameOver == True:
            gameDisplay.fill(WHITE)
            message_to_screen("Game Over, Press C to play again and Q to quit", BLACK,[100,SCREEN_HEIGHT//2])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
                        
        #Keyboard Control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -BLOCK_SIZE
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = BLOCK_SIZE
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    lead_x_change = 0
                
        #Bouncing ball
        if b1.x == SCREEN_WIDTH-BLOCK_SIZE or b1.x == BLOCK_SIZE:
            b1.vel[0] = -b1.vel[0]
        if b1.y == BLOCK_SIZE:
            b1.vel[1] = -b1.vel[1]

        #Paddle Bounce
        if lead_y == b1.y and lead_x-BLOCK_SIZE < b1.x < lead_x+paddle_size*BLOCK_SIZE+10:
            b1.vel[1] = - b1.vel[1]
            sounda.play()
            
        #Paddle and PowerUp
        for PowUp in PowerUpList:
            PowUp.y += 1
            if PowUp.y == lead_y and lead_x-4*BLOCK_SIZE < PowUp.x < lead_x+paddle_size*BLOCK_SIZE+BLOCK_SIZE:
                print("in")
                paddle_size += 1
                soundp.play()
            if PowUp.y == SCREEN_HEIGHT:
                PowerUpList.remove(PowUp)
       
        #Block Bounce
        for block in block_list:
            if block.x-10 < b1.x< block.x+10 and block.y-10< b1.y<block.y+10:
                if block.color == ORANGE:
                    p1 = PowerUp(block.x,block.y,BLACK)
                    PowerUpList.append(p1)
                block_list.remove(block)
                scoreVal+=5
        
        #Gesture Control
        try:
            if ser.inWaiting()>0:
                data = ser.readline().decode().strip()
                x=mapdistopix(float(data))
                print(data, x)
                if abs(lead_x - x) < SENSITIVITY_AND_STABILITY_FACTOR : 
                    lead_x = x
                    
        except ValueError:
            print("Out of sync")
            flag = True
        
        #Ball Update and Paddle Keyboard Update
        lead_x += lead_x_change
        b1.x += b1.vel[0]
        b1.y += b1.vel[1]

        #Game Over
        if b1.y == SCREEN_HEIGHT-20:
            b1.vel[1] = -b1.vel[1]
            scoreVal -=10
            
        t2 = time.time()
        if t2 - t1 > 60:
            gameOver = True
            message_to_screen("Time Up",RED,[SCREEN_WIDTH//2,SCREEN_HEIGHT//2])
                
        #Game Display Update        
        gameDisplay.fill(WHITE)
        
        #Score
        message_to_screen("Score: "+str(scoreVal),BLACK,[SCREEN_WIDTH//20,10])
        
        #Blocks
        for block in block_list:
            pygame.draw.rect(gameDisplay, block.color, [block.x,block.y,BLOCK_SIZE,BLOCK_SIZE])
        
        #Paddle
        Paddle(lead_x,lead_y,paddle_size)
        
        #Ball
        b1.draw()
        flag = False
        #PowerUp
        for PowUp in PowerUpList:
            print(paddle_size)
            pygame.draw.rect(gameDisplay,PowUp.color, [PowUp.x,PowUp.y,BLOCK_SIZE,BLOCK_SIZE])
        pygame.display.update()
        
        num = 60 
        clock.tick(num)
#        if flag and num < 100:
#            num+=1
#        elif flag and num <150:
#            num-=1

MainMenu()
pygame.quit()
quit()