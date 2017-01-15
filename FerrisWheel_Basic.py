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

pygame.init()


class WIN_CON:
#-------Window Constants-------#
    width  = 1000
    height = 700
    title = ""
    fps = 60
    background = (0,0,0)
#------------------------------#
w = WIN_CON()

class TextPrint:
    def __init__(self):
        self.reset()
        #self.font = pygame.font.SysFont("monospace", 20)

    def printf(self, screen, color, _size, _font, _x, _y, textString):
        self.font = pygame.font.SysFont(_font, _size)
        textBitmap = self.font.render(textString, True, color)
        _width = textBitmap.get_width()
        screen.blit(textBitmap, [(_x - (_width / 2)), _y])

    def reset(self):
        self.y = 0

def Limit(value, _max, _min):
    if(value > _max):
        return _max
    elif (value < _min):
        return _min
    else:
        return value

def DegToRad(_deg):
    return ((_deg / 180) * math.pi)

screen = pygame.display.set_mode([w.width, w.height])

pygame.display.set_caption(w.title)

running = True

clock = pygame.time.Clock()

txt = TextPrint()

deg = 0

while running:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            running = False # Flag that we are done so we exit this loop
    screen.fill(w.background)
    deg += 0.5
    txt.printf(screen, (0,100,255), 20, "monospace", ((w.width)/2), 10, "Rotation Count: {0:.{1}f}".format((deg / 360), 2))
    pygame.draw.circle(screen,(100,100,100), (((w.width)/2), ((w.height)/2)) ,100,2)
    pygame.draw.circle(screen,(100,100,100), (((w.width)/2), ((w.height)/2)) ,250,2)

    arms = 12
    for num in range(0,arms):
        circlePosX = (int((math.cos(DegToRad(deg + ((360/arms)*num))) * 250) + ((w.width)/2)))
        circlePosY = (int((math.sin(DegToRad(deg + ((360/arms)*num))) * 250) + ((w.height)/2)))

        pygame.draw.line(screen, (100,100,100), (((w.width)/2), ((w.height)/2)), (circlePosX,circlePosY), 3)
        pygame.draw.line(screen, (100,100,100), (circlePosX, circlePosY), ((circlePosX,(circlePosY + 60))), 3)
        pygame.draw.line(screen, (100,100,100), (circlePosX - 15, circlePosY + 60), ((circlePosX + 15,circlePosY + 60)), 3)
        pygame.draw.line(screen, (100,100,100), (circlePosX - 15, circlePosY + 60), ((circlePosX - 25,circlePosY + 50)), 3)
        pygame.draw.line(screen, (100,100,100), (circlePosX + 15, circlePosY + 60), ((circlePosX + 25,circlePosY + 50)), 3)
        for i in range(1, 13):
            circleLinePosX = (int((math.cos(DegToRad(deg + ((360/arms)*num))) * (i*20)) + ((w.width)/2)))
            circleLinePosY = (int((math.sin(DegToRad(deg + ((360/arms)*num))) * (i*20)) + ((w.height)/2)))
            c = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            pygame.draw.circle(screen, c, (circleLinePosX, circleLinePosY), 3)

    pygame.draw.line(screen,(100,100,100), ((((w.width)/2) - 250),(((w.height)/2) + 325)), (((w.width)/2),((w.height)/2)), 8)
    pygame.draw.line(screen,(100,100,100), ((((w.width)/2) + 250),(((w.height)/2) + 325)), (((w.width)/2),((w.height)/2)), 8)
    pygame.draw.rect(screen, (255, 255, 255), [(((w.width)/2)-100),(((w.height)/2)+100),200,30])
    txt.printf(screen, (0,0,0), 30, "monospace", ((w.width)/2), (((w.height)/2)+100),"Giant Wheel")
    pygame.display.flip()
    clock.tick(w.fps)

pygame.quit()