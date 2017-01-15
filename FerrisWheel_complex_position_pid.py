#-------------------------------------------------#
#                                                 #
#           Author:     Ethan Elliott             #
#           Project:    Animation                 #
#           Class:      ICS4U                     #
#           Date:       20/02/16                  #
#                                                 #
#-------------------------------------------------#
import pygame
import random
import math
import time
import ePID

pygame.init()

infoObject = pygame.display.Info()

class WIN_CON:
#-------Window Constants-------#
    width  = 1000
    height = 800
    title = ""
    fps = 60
    background = (0,0,0)
#------------------------------#
w = WIN_CON()

class TextPrint:
    def printf(self, screen, color, _size, _font, _x, _y, textString):
        self.font = pygame.font.SysFont(_font, _size)
        textBitmap = self.font.render(textString, True, color)
        _width = textBitmap.get_width()
        screen.blit(textBitmap, [(_x - (_width / 2)), _y])

def DegToRad(_deg):
    return ((_deg / 180) * math.pi)

screen = pygame.display.set_mode([w.width, w.height], pygame.RESIZABLE)

pygame.display.set_caption(w.title)

running = True

clock = pygame.time.Clock()

txt = TextPrint()

pygame.mixer.music.load('sound.ogg')
#pygame.mixer.music.play(1)

#pygame.event.set_grab(True)

deg = 1;
oldDeg = 0;
speed = 0
kDownPress = False
kUpPress = False
kWheelDirection = 0
kOldWheelDirection = 0

kp = 0.05;
ki = 0.0001;
kd = 0.01;
kepsilon = 0.0;
krampRate = 0.01;

velPID = ePID.ePID(kp,ki,kd,kepsilon);

velPID.setMaxOutput(1.0);
velPID.setRampRate(krampRate);
velPID.setDesiredValue(90);

while running:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            running = False # Flag that we are done so we exit this loop
    screen.fill(w.background)
    speed = velPID.calcPID(deg);
    deg += speed;

    txt.printf(screen, (0,100,255), 20, "monospace", ((w.width)/2), 10, "Rotation Count: {0:.{1}f}".format((deg / 360), 2))
    txt.printf(screen, (0,100,255), 20, "monospace", ((w.width)/2), 50, "Speed : {0:.{1}f}".format(speed, 5))


    arms = 12
    for num in range(0,arms):
        circlePosX = (int((math.cos(DegToRad(deg + ((360/arms)*num))) * ((w.height)/3)) + ((w.width)/2)))
        circlePosY = (int((math.sin(DegToRad(deg + ((360/arms)*num))) * ((w.height)/3)) + ((w.height)/2)))

        pygame.draw.line(screen, (100,100,100), (circlePosX, circlePosY), ((circlePosX,(circlePosY + 60))), 3)
        pygame.draw.line(screen, (100,100,100), (circlePosX - 15, circlePosY + 60), ((circlePosX + 15,circlePosY + 60)), 3)
        pygame.draw.line(screen, (100,100,100), (circlePosX - 15, circlePosY + 60), ((circlePosX - 25,circlePosY + 50)), 3)
        pygame.draw.line(screen, (100,100,100), (circlePosX + 15, circlePosY + 60), ((circlePosX + 25,circlePosY + 50)), 3)
        pygame.draw.line(screen, (100,100,100), (((w.width)/2), ((w.height)/2)), (circlePosX,circlePosY), 3)
        for i in range(1, ((w.height)/100)):
            circleLinePosX = (int((math.cos(DegToRad(deg + ((360/arms)*num))) * (i*((w.height)/24))) + ((w.width)/2)))
            circleLinePosY = (int((math.sin(DegToRad(deg + ((360/arms)*num))) * (i*((w.height)/24))) + ((w.height)/2)))
            c = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            pygame.draw.circle(screen, c, (circleLinePosX, circleLinePosY), 3)

    pygame.draw.circle(screen,(100,100,100), (((w.width)/2), ((w.height)/2)) ,((w.height)/3),4) #Outer Wheel
    lights = 45
    for num in range (0, lights):
        circlePosX = (int((math.cos(DegToRad(deg + ((360/lights)*num))) * ((w.height)/3)) + ((w.width)/2)))
        circlePosY = (int((math.sin(DegToRad(deg + ((360/lights)*num))) * ((w.height)/3)) + ((w.height)/2)))
        c = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        pygame.draw.circle(screen, c, (circlePosX, circlePosY) , 2)


    pygame.draw.line(screen,(100,100,100), ((((w.width)/2) - 250),(((w.height)/2) + 325)), (((w.width)/2),((w.height)/2)), 8)
    pygame.draw.line(screen,(100,100,100), ((((w.width)/2) + 250),(((w.height)/2) + 325)), (((w.width)/2),((w.height)/2)), 8)

    pygame.draw.rect(screen, (255, 255, 255), [(((w.width)/2)-100),(((w.height)/2)+100),200,30])
    pygame.draw.rect(screen, (0, 150, 10), [(0),(w.height-30),w.width,30])
    txt.printf(screen, (0,0,0), 30, "monospace", ((w.width)/2), (((w.height)/2)+100),"Giant Wheel")
    pygame.display.flip()
    clock.tick(w.fps)

pygame.quit()
