from curses import window
import pygame
import os
import math
import numpy as np

#from EdgeCollapsing import collapseRender

def render(V,E):

    pygame.init()
    os.environ["SDL_VIDEO_CENTERED"]='1'
    black, white, blue  = (20, 20, 20), (230, 230, 230), (0, 154, 255)
    width, height = 1920, 1080
    window = pygame.display.set_mode((width,height))
    pygame.init()
    pygame.display.set_caption("3D cube Projection")
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    fps = 240

    angleX = angleY = angleZ = 0
    
    #position = [width/2, height/2]
    #scale = 18 #scale for lowlaurana
    #scale = 2000 #scale for bunny
    scale = 40 #scale for face 2
    speed = 0.1
    run = True

    def connectV(i,j,V):
        pygame.draw.line(window,black,(V[i][0],V[i][1]),(V[j][0],V[j][1]))

    while run:
        clock.tick(fps)
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                angleY = angleX = angleZ = 0
            if keys[pygame.K_a]:
                angleY += speed
            if keys[pygame.K_d]:
                angleY -= speed     
            if keys[pygame.K_w]:
                angleX += speed
            if keys[pygame.K_s]:
                angleX -= speed
            if keys[pygame.K_q]:
                angleZ -= speed
            if keys[pygame.K_e]:
                angleZ += speed
            # if keys[pygame.K_c]:
            #     collapseRender()      

        projectionMatrix = np.matrix([[1,0,0],[0,1,0],[0,0,0]])

        rotationX = np.matrix([[1, 0, 0],
                    [0, math.cos(angleX), -math.sin(angleX)],
                    [0, math.sin(angleX), math.cos(angleX)]])

        rotationY = np.matrix([[math.cos(angleY), 0, -math.sin(angleY)],
                    [0, 1, 0],
                    [math.sin(angleY), 0, math.cos(angleY)]])

        rotationZ = np.matrix([[math.cos(angleZ), -math.sin(angleZ), 0],
                    [math.sin(angleZ), math.cos(angleZ), 0],
                    [0, 0 ,1]])
        
        projectedV = [0 for i in range(len(V))]
        index = 0
        for v in V:
            #rotateZ = np.matmul(rotationY,v) #rotar en y
            rotateX = np.matmul(rotationX,v)
            rotateY = np.matmul(rotationY,[rotateX[0,0],rotateX[0,1],rotateX[0,2]])
            rotateZ = np.matmul(rotationZ,[rotateY[0,0],rotateY[0,1],rotateY[0,2]])
            
            v2D = np.matmul(projectionMatrix,[rotateZ[0,0],rotateZ[0,1],rotateZ[0,2]])
            x = (v2D[0,0] * scale) + width/2
            y = (v2D[0,1] * scale) + height/2
            
            projectedV[index] = (x,y)
            index += 1

            pygame.draw.circle(window,blue,(x,y),2)

        for e in E:
            connectV(e[0],e[1],projectedV)    


        #angle += speed
        pygame.display.update()
    

    pygame.quit()