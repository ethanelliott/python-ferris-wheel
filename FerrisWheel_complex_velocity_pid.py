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

pygame.init()
running = True

infoObject = pygame.display.Info()

class Timer:
    def __init__(self):
        self.startTime = 0;

    def Start(self):
        self.startTime = time.time();

    def Reset(self):
        self.startTime = time.time();

    def Get(self):
        return float(time.time() - self.startTime);

class ePID:
    def __init__(self, p, i, d, errorEpsilon, maxOutput, rampRate):
        self.m_p = p;
        self.m_i = i;
        self.m_d = d;
        self.m_errorEpsilon = errorEpsilon;
        self.m_errorSum = 0;
        self.m_errorIncrement = 1;
        self.m_oldDesiredValue = 0;
        self.m_maxOutput = maxOutput;
        self.m_previousValue = 0;
        self.m_output = 0;
        self.m_desiredValue = 0;
        self.m_originalDesiredValue = 0;
        self.m_rampRate = rampRate;
        self.m_rampSum = 0;
        self.m_isRamping = True;
        self.m_calcP = 0;
        self.m_calcI = 0;
        self.m_calcD = 0;
        self.m_error = 0;
        self.m_firstCycle = True;
        self.velocityTime = Timer();
        self.pid_output = "";
        self.pid_output = "pVal, iVal, dVal, Output, Error\n";

    def setDesiredValue(self, desiredValue):
        self.m_desiredValue = desiredValue;

    def calcPID(self, currentValue):

        if(self.m_firstCycle):
            self.m_firstCycle = False;
            self.m_errorSum = 0;
            self.m_originalDesiredValue = self.m_desiredValue;
            self.m_isRamping = True;
            self.m_rampSum = (self.m_maxOutput/self.m_rampRate);
            print self.m_rampSum

        #calculate Error
        self.m_error = self.m_desiredValue - currentValue;

        #calculate P value
        self.m_calcP = self.m_error * self.m_p;

        #calculate I value
        # Error is positive and outside the epsilon band.
    	if (self.m_error >= self.m_errorEpsilon):
       	    if (self.m_errorSum < 0):
    			self.m_errorSum = 0;

            if (self.m_error < self.m_errorIncrement):
    			self.m_errorSum += self.m_error;
            else:
                self.m_errorSum += self.m_errorIncrement;

    	elif (self.m_error <= -self.m_errorEpsilon) :
    		if (self.m_errorSum > 0):
                	self.m_errorSum = 0;

    		if (self.m_error > -self.m_errorIncrement):
    			self.m_errorSum += self.m_error;
    		else:
    			self.m_errorSum -= self.m_errorIncrement;
        else:
    		self.m_errorSum = 0;

    	self.m_calcI = self.m_i * float(self.m_errorSum);


        #calculate D value
        if(not self.m_firstCycle and self.velocityTime.Get() > 0):
            velocity = ((currentValue - self.m_previousValue) / self.velocityTime.Get());
            self.m_calcD = self.m_d * float(velocity);
    	else:
    		self.m_calcD = 0;

        self.m_previousValue = currentValue;
        self.m_oldDesiredValue = self.m_desiredValue;
        #calculate output
        if(self.m_isRamping):
            print (self.m_rampSum * self.m_rampRate);
            self.m_output = self.m_maxOutput - (self.m_rampSum * self.m_rampRate);
            if (self.m_rampSum == 0 or self.m_error <= (self.m_originalDesiredValue/2)):
                self.m_isRamping = False;
            else:
                self.m_rampSum -= 1;
        else:
            self.m_output = self.m_calcP + self.m_calcI - self.m_calcD;


        #ensure the value is inside the max_output
        if (self.m_output > self.m_maxOutput):
            self.m_output = self.m_maxOutput;
        elif (self.m_output < -self.m_maxOutput):
            self.m_output = -self.m_maxOutput;

        #return the calculated value
        self.m_output = round(self.m_output, 4);
        if (self.m_output != 0):
            buff = str(self.m_calcP) + ", " + str(self.m_calcI) + ", " + str(self.m_calcD) + ", " + str(self.m_output) + ", " + str(self.m_error) + "\n"
            self.pid_output += str(buff);
        else:
            self.f = open("pid.csv", 'w');
            self.f.write(self.pid_output);
            running = False;

        return self.m_output;

class WIN_CON:
#-------Window Constants-------#
    width  = 800
    height = 600
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

clock = pygame.time.Clock()

txt = TextPrint()

pygame.mixer.music.load('sound.ogg')
pygame.mixer.music.play(1)

pid_output = "";

#pygame.event.set_grab(True)

deg = 0.1
speed = 0
kDownPress = False
kUpPress = False
kWheelDirection = 0
kOldWheelDirection = 0

kp = 0.04;
ki = 0.0001;
kd = 0.1;
kepsilon = 0;
max_output = 1.0;
ramp_Rate = 0.01;

velPID = ePID(kp,ki,kd,kepsilon,max_output, ramp_Rate);

while running:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            running = False # Flag that we are done so we exit this loop
    screen.fill(w.background)

    velPID.setDesiredValue(3600);

    vel = velPID.calcPID(deg);
    deg += vel;
    txt.printf(screen, (0,100,255), 20, "monospace", ((w.width)/2), 10, "Rotation Count: {0:.{1}f}".format((deg / 360), 2))
    txt.printf(screen, (0,100,255), 20, "monospace", ((w.width)/2), 30, "Speed: {0:.{1}f}".format(vel, 4))

    arms = 12;

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
    pygame.draw.circle(screen,(100,100,100), (((w.width)/2), ((w.height)/2)) ,((w.height)/38),0) #Outer Wheel
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