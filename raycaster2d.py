import pygame
import math

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

map = [[1,1,1,1,1,1,1,1,1,1,1,1],
       [1,0,0,0,0,1,1,0,1,0,0,1],
       [1,0,1,1,0,0,0,0,1,0,0,1],
       [1,0,1,1,0,0,0,0,0,0,1,1],
       [1,0,0,0,0,0,1,1,0,0,0,1],
       [1,0,0,0,0,0,1,1,0,0,0,1],
       [1,0,1,1,0,0,0,0,0,1,0,1],
       [1,0,1,1,0,1,1,0,0,1,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,1],
       [1,1,1,1,1,1,1,1,1,1,1,1]]

def ifZero50(num):
    if num == 0:
        return 50
    else:
        return num



def castRay(playerX,playerY,playerAngle):
    x = playerX
    y = playerY

    while x > 0 and x < 600 and y > 0 and y < 600:
            
        if playerAngle > math.pi/4 and playerAngle < math.pi * 3/4:#right quater
            opposite = ((50 - (x % 50)) * math.tan(playerAngle - (math.pi * 1/2)))
            oppositeL = min((50-(y % 50)) ,max(-ifZero50(y % 50),opposite))
            y = y + oppositeL
            try:
                x = x + (50 - (x % 50)) * (oppositeL/opposite)
            except ZeroDivisionError:
                x = x + (50 - (x % 50))
                

        elif playerAngle > math.pi* 5/4 and playerAngle < math.pi * 7/4:#left quater
            opposite = (ifZero50(x % 50) * math.tan(playerAngle - (math.pi * 3/2)))
            oppositeL = min(ifZero50(y % 50) ,max(-(50-(y % 50)),opposite))
            y = y - oppositeL
            try:
                x = x - (ifZero50(x % 50)) * (oppositeL/opposite)
            except ZeroDivisionError:
                x = x - (ifZero50(x % 50))
        
        elif playerAngle > math.pi * 3/4 and playerAngle < math.pi * 5/4:#down quater
            opposite = ((50 - (y % 50)) * math.tan(playerAngle - (math.pi)))
            oppositeL = min(ifZero50((x % 50)) ,max(-(50-(x % 50)),opposite))
            x = x - oppositeL
            try:
                y = y + (50 - (y % 50)) * (oppositeL/opposite)
            except ZeroDivisionError:
                y = y + (50 - (y % 50))
        
        elif playerAngle > math.pi * 7/4 or playerAngle < math.pi * 1/4:#up quater
            opposite = (ifZero50(y % 50) * math.tan(playerAngle))
            oppositeL = min((50 - (x % 50)) ,max(-ifZero50(x % 50),opposite))
            x = x + oppositeL
            try:
                y = y - ifZero50(y % 50) * (oppositeL/opposite)
            except ZeroDivisionError:
                y =  y - ifZero50(y % 50) 
            
            
        #if line has reach solid block terminate loop
        if map[int(y//50)][int(x//50)] == 1 or map[int((y - 0.1)//50)][int(x//50)] == 1 or map[int(y//50)][int((x - 0.1)//50)] == 1:
            break
 
    return (x,y)


def movePlayer(keys,playerX,playerY,playerAngle,dt):
    #turning
    if keys[pygame.K_LEFT]:
        playerAngle -= dt * 2
    elif keys[pygame.K_RIGHT]:
        playerAngle += dt * 2

    #moving
    if keys[pygame.K_w]:
        if map[int((playerY - math.cos(playerAngle) * moveSpeed * dt)//50)][int((playerX)//50)] == 0:
            playerY -= math.cos(playerAngle) * moveSpeed * dt
        if map[int((playerY)//50)][int((playerX + math.sin(playerAngle) * moveSpeed * dt)//50)] == 0:
            playerX += math.sin(playerAngle) * moveSpeed * dt
            
    elif keys[pygame.K_s]:
        if map[int((playerY + math.cos(playerAngle) * moveSpeed * dt)//50)][int((playerX)//50)] == 0:
            playerY += math.cos(playerAngle) * moveSpeed * dt
        if map[int((playerY)//50)][int((playerX - math.sin(playerAngle) * moveSpeed * dt)//50)] == 0:
            playerX -= math.sin(playerAngle) * moveSpeed * dt
            
    elif keys[pygame.K_a]:
        if map[int((playerY)//50)][int((playerX - math.cos(playerAngle) * moveSpeed * dt)//50)] == 0:
            playerX -= math.cos(playerAngle) * moveSpeed * dt
        if map[int((playerY - math.sin(playerAngle) * moveSpeed * dt)//50)][int((playerX)//50)] == 0:
            playerY -= math.sin(playerAngle) * moveSpeed * dt

    elif keys[pygame.K_d]:
        if map[int((playerY)//50)][int((playerX + math.cos(playerAngle) * moveSpeed * dt)//50)] == 0:
            playerX += math.cos(playerAngle) * moveSpeed * dt
        if map[int((playerY + math.sin(playerAngle) * moveSpeed * dt)//50)][int((playerX)//50)] == 0:
            playerY += math.sin(playerAngle) * moveSpeed * dt
    
    return playerX, playerY, playerAngle


run = True

#inital postion and orientation of player
playerX = 75.0
playerY = 75.0
playerAngle = math.pi/2
dtime = 0
fov = 70
moveSpeed = 150

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #clears screen
    screen.fill("black")

    #draws map
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == 0:
                pygame.draw.rect(screen, "gray",pygame.Rect(x * 50,y * 50,50,50),1)
            else:
                pygame.draw.rect(screen, "gray",pygame.Rect(x * 50,y * 50,50,50))
    
    #draws player
    pygame.draw.line(screen, "yellow", (playerX, playerY),(playerX + math.sin(playerAngle) * 20, playerY - math.cos(playerAngle) * 20))
    pygame.draw.circle(screen, "yellow", (playerX, playerY),10)
    

    
    #draws rays throught the players fov 4 lines per degree
    playerAngle -= math.pi * fov/360
    for offset in range(0,fov * 4):  
        pygame.draw.line(screen, "yellow", (playerX, playerY),castRay(playerX,playerY,playerAngle),2)            
        playerAngle += math.pi/720   
    playerAngle -= math.pi * fov/360

    pygame.display.flip()#updates display surface to the screen

    #move player according to input
    keys = pygame.key.get_pressed()
    playerX, playerY,playerAngle = movePlayer(keys,playerX,playerY,playerAngle,dtime)
    
    playerAngle = playerAngle % (2 * math.pi)#resets angle with bound of 0 to 2pi

    dtime = clock.tick(30) / 1000#this isues 30 frames per second


