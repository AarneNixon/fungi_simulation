import pygame, sys, time, math, random
from pygame.locals import *
framesPerSecond = 30
windowWidth = 600
windowHeight = 600
halfWindowWidth = int(windowWidth/2)
halfWindowHeight = int(windowHeight/2)
marbleDark = (25,0,0)
blocksLength = 50
blocksDepth = 50
playerSpeed = 3
defaultHealth = 5
gamePaused = False
colIndex = 0
rowIndex = 0
waveList = []
wormList = []
shieldList = []
fractalList = []
utilityIndex = 1
blocks = [[0 for x in range(blocksDepth)] for y in range(blocksLength)]
def main():
    global frameCycle, marbleTextures, surface1
    fractalList.append(fractalDaemon((300,300),0))
##velocity = 0
    #colIndex = 0
    #print(colIndex)
    #rowIndex = 0
    surface1 = pygame.display.set_mode((windowWidth,windowHeight))
    pygame.init()
    frameCycle = pygame.time.Clock()
#for i in range(1,5):
#    marbleTextures.append(pygame.image.load('marble%s.png' % i))
    for i in range(1,blocksLength+1):
        for j in range(1,blocksDepth):
            randomizedColor = (random.randrange(0,250),0,15)
            blocks[i-1][j] = randomizedColor
    while True:
        loopMeBoi()
    
def loopMeBoi():
    if (random.random()<0.01):
        if (len(wormList) < 3):
#            print("wormsign")
            wormList.append(wormSign(5,100,False,(random.randrange(0,windowWidth),random.randrange(0,windowHeight)),750))
    for myEvent in pygame.event.get():
        if myEvent.type == QUIT:
            lv()
        elif myEvent.type == KEYDOWN:
            global colIndex
            global rowIndex
            global utilityIndex
            if myEvent.key in(K_RIGHT,K_d):
                #colIndex
                colIndex += 10
                #colIndex %= windowWidth
            if myEvent.key in(K_LEFT,K_a):
                #colIndex
                colIndex -= 10
                colIndex %= windowWidth
            if myEvent.key in(K_DOWN,K_s):
                #rowIndex
                rowIndex -= 10
                rowIndex %= windowHeight
            if myEvent.key in(K_UP,K_w):
                #rowIndex
                rowIndex += 10
                rowIndex %= windowHeight
            if myEvent.key == K_p:
                #paused
                paused = True
            if myEvent.key == K_l:
                lv()
            if myEvent.key == K_1:
                utilityIndex = 1
            if myEvent.key == K_2:
                utilityIndex = 2
            if myEvent.key == K_3:
                utilityIndex = 3
        elif myEvent.type == pygame.MOUSEBUTTONDOWN:
            if utilityIndex == 1:
                vertVar = 50
                horVar = 50
                for every in range(0,6):
                    spawnPos = list(pygame.mouse.get_pos())
                    spawnPos[0] += random.randrange(-horVar,horVar)
                    spawnPos[1] += random.randrange(-vertVar,vertVar)
                    #print(spawnPos)
                    waveList.append(vineWave(25,150,(0,0,0),spawnPos))
            elif utilityIndex == 3:
                shieldList.append(forceField(pygame.mouse.get_pos(),50))
    drawColumns()
def drawColumns():
    for i in range(1, blocksLength):
        for j in range(1, blocksDepth):
            #print
            pygame.Surface.set_at(surface1,(random.randrange(0,550)+i,random.randrange(0,550)+j),blocks[(i+colIndex)%len(blocks)][(j+rowIndex)%len(blocks[1][:])])
            #pygame.Surface.set_at(surface1,(random.randrange(0,550)+i,random.randrange(0,550)+j),blocks[(i+colIndex)%len(blocks)][(j+rowIndex)%len(blocks[1][:])])
    if(len(waveList)>0):
        for k in range(0,len(waveList)):
##            print("last one")
##            print(len(waveList))
##            print(k)
##            print(waveList[k].myMaturity)     
            #print(waveList[k].myMaturity)
            if(k != len(waveList) and k != len(waveList)-1):
                waveList[k].myMaturity += 1
                drawWave(surface1,waveList[k].myPosition,waveList[k].myMaturity,waveList[k].myColor)
        for l in range(-1 * len(waveList),-1):
            #print(-1 * len(waveList))
            #print()
            if(waveList[l].myMaturity >= waveList[l].mySpan):
                del waveList[l]
                #print("delled")
                if (l == -2):
                    del waveList[0]
    if(len(wormList)>0):
        for m in range(0,len(wormList)):
            if(m != len(wormList) and m != len(wormList)-1):#worm movement crawling
                wormList[m].myMaturity += 1
                newPosition = list(wormList[m].myPosition)
                if (random.random() < 0.05):#fraction of hor moves successful
                    newPosition[0] += wormList[m].xVel
                    newPosition[0] %= windowWidth
                if (random.random() < 0.05):#fraction of ver moves successful
                    newPosition[1] += wormList[m].yVel
                    newPosition[1] %= windowWidth
                wormList[m].myPosition = tuple(newPosition)
                if (random.random() < 0.25):
                    randIndex = math.floor(random.random()*len(wormList[m].positions))
                    wormList[m].positions[randIndex] = tuple(newPosition)
                drawWorm(surface1,wormList[m].positions,wormList[m].myMaturity,wormList[m].myDarkness)
        for n in range(-1 * len(wormList),-1):
            #print(-1 * len(wormList))
            #print()
            if(wormList[n].myMaturity >= wormList[n].myLifetime):
                del wormList[n]
                #print("delled")
                if (n == -2):
                    del wormList[0]
    if(len(shieldList)>0 and random.random() < 1):
        for o in range(0,len(shieldList)):
            if (o != len(shieldList) and o != len(shieldList)-1):
                if (shieldList[o].life):
                    drawShield(surface1,shieldList[o].center,shieldList[o].radius,shieldList[o].center)
##    if(random.random() < 0.01):
##        print("daemon")
##        drawFractal((random.randrange(0,windowWidth),random.randrange(0,windowHeight)),0)
    if(len(fractalList)>0):
        for p in range(0,len(fractalList)):
            drawFractal(fractalList[p].spawnAt,0)
    pygame.display.update()
def drawWave(drawOn,centerAt,radius,color):
    for xPos in range(-radius,radius):
        pixelY1 = (centerAt[1] + int(round(3 * math.sqrt(abs(radius^2-(xPos^2))))))%windowHeight
        pixelY2 = (centerAt[1] + (-3 * int(round(math.sqrt(abs(radius^2-(xPos^2)))))))%windowHeight
        pixelColor = blocks[(centerAt[0]+xPos+1)%50][pixelY1%50]
        pixelColor2 = blocks[(centerAt[0]+xPos+1)%50][pixelY2%50]
        try:
            pygame.Surface.set_at(drawOn,((centerAt[0]+xPos+1)%windowWidth,pixelY1),tuple([color[0]+pixelColor[0]/4,color[1]+pixelColor[1]/4,color[2]+pixelColor[2]/4]))
            pygame.Surface.set_at(drawOn,((centerAt[0]+xPos+1)%windowWidth,pixelY2),tuple([color[0]+pixelColor2[0]/4,color[1]+pixelColor2[1]/4,color[2]+pixelColor2[2]/4]))
        except TypeError:
            pass
        #blocks[(centerAt[0]+xPos+1)%blocksDepth][(math.floor(centerAt[1]+math.sqrt(abs(radius-(xPos^2))))%blocksLength)] = (0,250,250)
        #for xPos in range(-radius,radius):
         #   pygame.Surface.set_at(surface1,centerAt + (xPos,sqrt(radius-(xPos^2))),color)
def drawWorm(drawOn,positions,length,darkness):
    #colAtEnt = pygame.Surface.get_at(surface1,entrance)#colorAtEntrance
    #pygame.Surface.set_at(surface1,entrance,(50,0,15))
    #pygame.Surface.set_at(surface1,(entrance[0],entrance[1]),(0,0,0))
    #print("worm drawn")
    if darkness:
        wormColor = (0,0,15)
    else:
        wormColor = (random.randrange(200,250),0,15)
    for pastPos in positions:
        for altXIndex in range(pastPos[0]-2,pastPos[0]+2):
            for altYIndex in range(pastPos[1]-2,pastPos[1]+2):
                pygame.Surface.set_at(surface1,(pastPos[0]+altXIndex,pastPos[1]+altYIndex),wormColor)
def drawShield(drawOn,inCenter,inRadius,color):
    for vS in range(1,0): #vertical shift
        for tempRad in range(inRadius,-inRadius):
            for xPos in range(-tempRad,tempRad):
                pixelY1 = (inCenter[1] + int(round(3 * math.sqrt(abs(inRadius^2-(xPos^2))))))%windowHeight
                pixelY2 = (inCenter[1] + (-3 * int(round(math.sqrt(abs(inRadius^2-(xPos^2)))))))%windowHeight
                pixelColor = blocks[(inCenter[0]+xPos+1)%50][pixelY1%50]
                pixelColor2 = blocks[(inCenter[0]+xPos+1)%50][pixelY2%50]
                try:
                    pygame.Surface.set_at(drawOn,(int((inCenter[0]+xPos+1)),vS + inCenter[1] + int(round(3 * math.sqrt(abs(tempRad^2-(xPos^2)))))),(pixelColor[0]/5,250,pixelColor[2]/5))
                    pygame.Surface.set_at(drawOn,(int((inCenter[0]+xPos+1)),vS + inCenter[1] + (-3 * int(round(math.sqrt(abs(tempRad^2-(xPos^2))))))),(pixelColor2[0]/5,250,pixelColor2[2]/5))
                except TypeError:
                    pass
def drawFractal(inPosition,fractalCode):
    for xIter in range((inPosition[1]-25)%50,(inPosition[0]+25)%50):
        for yIter in range((inPosition[1]-25)%50,(inPosition[1]+25)%50):
            inColor = blocks[xIter][yIter]
            inRed = inColor[1]
            outRed = 0
            nextRed = 0
            while (nextRed < 250):
                outRed = nextRed
                nextRed = inRed^2
            pygame.Surface.set_at(surface1,(xIter,yIter),tuple([inColor[0],outRed,inColor[2]]))
def lv():#leave
    pygame.quit()
    sys.exit()
class vineWave:
    mySpan = 200
    myShape = 0
    myColor = (0,0,0)
    myPosition = (0,0)
    myMaturity = 0
    def __init__(self,span,shape,color,position):
        self.mySpan = span
        self.myShape = shape
        self.myColor = color
        self.myPosition = position
class wormSign:
    myWidth = 3
    myLength = 15
    myDarkness = True
    myPosition = (0,0)
    positions = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
    myLifetime = 5000
    myMaturity = 0
    yVel = 1
    xVel = 1
    def __init__(self,width,length,darkness,position,lifetime):
        self.myWidth = width
        self.myLength = length
        self.myDarkness = darkness
        self.myPosition = (random.randrange(0,windowWidth),random.randrange(0,windowHeight))
        self.myLifetime = lifetime
class forceField:
    center = (0,0)
    radius = 15
    life = 100
    def __init__(self,inCenter,inRadius):
        #print("initted")
        self.center = inCenter
        self.radius = inRadius
class fractalDaemon:
    spawnAt = (0,0)
    fractal = 0
    def __init__(self,spawnPoint,fractalCode):
        print("initted")
        self.spawnAt = spawnPoint
        self.fractal = fractalCode
main()
'''if not gamePaused:
            if velocity == 1:
                colIndex += 1
                print("right")
            if velocity == -1:
                colIndex -= 1
                print("left")
        else:
            print("paused")
'''
