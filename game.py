import numpy as np
import cv2
from collections import deque
import pygame

pygame.init()

display_width=430
display_height=360
gameDisplay=pygame.display.set_mode((display_width,display_height))
gameDisplay.fill((255, 255, 255))
black=(0,0,0)

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 360)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)


pts = deque(maxlen=128)

Lower_green = np.array([110,50,50])
Upper_green = np.array([130,255,255])

smallfont=pygame.font.SysFont('comicsans',25)


def text_objects(text,color,size):
    if size=='small':
        textSurface=smallfont.render(text,True,color)

    return textSurface,textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size='small'): #the message and the color of the message
    textSurf,textRect = text_objects(msg,color,size)
    #screen_text=font.render(msg,True,color)
    #gameDisplay.blit(screen_text,[display_width/2,display_height/2]) #updates the screen
    textRect.center=(display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf,textRect)

def circleDraw(x, y):

    pygame.draw.line(gameDisplay, black, x, y, 4)
    pygame.draw.circle(gameDisplay, (0, 255, 0), (360,180),10)
    print(x)

    if(x == (360 + 4,180 + 4) or x == (360 -4, 180 - 4) or y == (360 + 4, 180 + 4) or y == (360 - 4, 180 + 4 ) ):
        pygame.draw.line(gameDisplay, (0, 255, 0), x, y, 4)
    #pygame.draw.circle(gameDisplay, (0, 0, 255), x, 3)
    #pygame.draw.circle(gameDisplay, (0, 0, 255), (int(x-1), int(y-1)), 3)
    pygame.display.update()

#message_to_screen("Press c to clear", black, 50)
def gameIntro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pygame.quit()
                    quit()
                    break

while True:

    if pygame.KEYDOWN:
        if pygame.key == pygame.K_c:
            pygame.quit()
            quit()
    ret, img = video_capture.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3,3), np.uint)
    mask = cv2.inRange(hsv, Lower_green, Upper_green)
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=5)
    #res = cv2.bitwise_and(img, img, mask = mask)
    cnts, heir = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 0.5:
            #cv2.circle(img, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(img, center, 5, (0, 0, 255), -1)

    pts.appendleft(center)
    for i in range(1, len(pts)):

        if pts[i -1] is None or pts[i] is None:
            continue
        thick = int(np.sqrt(len(pts) / float(i + 1)) * 2.5)
        cv2.line(img, pts[i - 1], pts[i], (0, 0, 255), thick)
        #print(pts[i -1], pts[i])
        circleDraw(pts[i-1], pts[i])


    cv2.imshow('cnts',img)




    k = cv2.waitKey(30) % 0xFF
    if k == 32:
        break

gameIntro()
cap.release()
cv2.destroyAllWindows()