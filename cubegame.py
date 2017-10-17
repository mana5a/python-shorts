#a game with lots of cubes coming at you in 3d, avoid them

import pygame
from pygame.locals import * #?? what did i import

from OpenGL.GL import *
from OpenGL.GLU import * #advanced functions

import random

vertices=(            #defines vertices of a cube in order
     (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges=(       #defines the connections of vertices to each other
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

surfaces=(            #defines the vertices that make up a surface
        (0,1,2,3),
        (3,2,7,6),
        (6,7,5,4),
        (4,5,1,0),
        (1,5,7,2),
        (4,0,3,6)
        )

colors=(      #defines a list of colors to cycle through
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,0,0),
    (1,1,7),
    (0,1,1),
    (1,0,3),
    (0,1,0),
    (0,0,1),
    (3,0,0),
    (1,1,1),
    (0,1,1),
    )


ground_vertices=(    #defines a plane for the ground, not using it here
    (-50,-0.1,20),
    (50,-0.1,20),
    (-50,-0.1,-300),
    (50,-0.1,-300),
    )

def ground():
    glBegin(GL_QUADS)   #use this when you're drawing surfaces
    for vertex in ground_vertices:
        glColor3fv((0,0.5,0.5))  #defines a color for the gl functions to follow
        glVertex3fv(vertex)  #takes a vertex as a parameter and connects each one?? in the loop I think
    glEnd() #always close gl

    
def set_vertices(max_distance,min_distance=-20,camera_x=0,camera_y=0):

    camera_x=-1*int(camera_x)
    camera_y=-1*int(camera_y)
    
    x_value_change=random.randrange(camera_x-75,camera_x+75)  #defining the field of view, so that the cubes never go out of range
    y_value_change=random.randrange(camera_y-75,camera_y+75)
    z_value_change=random.randrange(-1*max_distance,min_distance)
    new_vertices=[]
    for vert in vertices:  #generating new vertices randomly in the field of view
        new_vert=[]
        new_x=vert[0]+x_value_change
        new_y=vert[1]+y_value_change
        new_z=vert[2]+z_value_change
        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)
    return new_vertices

        
        
def cube(vertices):
    glBegin(GL_QUADS) 
   
    for surface in surfaces:
        x=0        
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])  #picking a color from the list for each vertex
            glVertex3fv(vertices[vertex])   #connecting a surface
    glEnd()
    glBegin(GL_LINES) #use this if you're drawing only lines
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])    #connecting edges        
    glEnd()

def main():
    pygame.init()
    display=(800,600)
    pygame.display.set_mode(display,DOUBLEBUF|OPENGL) #double buffer for rastering, both are the modes that you are opening in
    max_distance=100
    gluPerspective(45,(display[0]/display[1]),0.1,max_distance) #angle,aspect ratio, near clipping plane, far clipping plane
    glTranslatef(0,0,-40) #defines the camera distance from the object just defined
    #object_passed=False

    x_move=0
    y_move=0

    cur_x=0
    cur_y=0

    game_speed=2
    direction_speed=2
    
    cube_dict={}

    for x in range(75):
        cube_dict[x]=set_vertices(max_distance)


    #glRotatef(40,2,1,0) #3d rotation probably a quaternion

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: #pygame calls to close the window
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN: #checks for keypress
                if event.key== pygame.K_RIGHT:
                    x_move=direction_speed
                if event.key== pygame.K_LEFT:
                    x_move=-direction_speed                  
                if event.key== pygame.K_DOWN:
                    y_move=direction_speed
                if event.key== pygame.K_UP:
                    y_move=-direction_speed
                    
            if event.type==pygame.KEYUP: #checks for release of key press
                if event.key== pygame.K_RIGHT or event.key== pygame.K_LEFT:
                    x_move=-0.3                 #this val is not direction_speed bc you don't want it to move just as fast when you're not pressing, just a light bump
                if event.key== pygame.K_DOWN or event.key== pygame.K_UP:
                    y_move=-0.3
                    
##            if event.type==pygame.MOUSEBUTTONDOWN: #for zoom in and zoom out
##                if event.button==4: #zoom in val=4
##                    glTranslate(0,0,1)
##                if event.button==5: #zoom out val =5
##                    glTranslate(0,0,-1)
                
                    
        #glRotatef(1,3,2,1)

        x=glGetDoublev(GL_MODELVIEW_MATRIX) #wtf???
        #print(x)
        camera_x= x[3][0]
        camera_y= x[3][1]
        camera_z= x[3][2]

##        if camera_z<-1:
##            object_passed=True
            


        cur_x+=x_move
        cur_y+=y_move
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #clear both buffers before rendering each frame to avoid flickering etc
        glTranslate(x_move,y_move,game_speed)
        #ground()
        
        for each_cube in cube_dict:
            cube(cube_dict[each_cube])

        #delete_list=[]

        for each_cube in cube_dict:
            if camera_z<=cube_dict[each_cube][0][2]:
                #print("passed a cube")
                #delete_list.appen(each_cube)
                new_max=int(-1*(camera_z-(max_distance*2)))
                
                cube_dict[each_cube]=set_vertices(new_max,int(camera_z-max_distance),cur_x,cur_y)
            
            
        pygame.display.flip() #pygame.display.update should also work but idk why it doesnt
        #pygame.time.wait(10)

main()
pygame.quit()
quit()

