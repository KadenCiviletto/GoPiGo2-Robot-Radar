from gopigo import * #Basic functions for control the GoPiGo
import sys # to closign the running program
import pygame
import os
from math import atan
from encoder import * #encoder read methods 
from pygame.locals import *
#access to key press/release events 
from gui import *

# arrays for storing and returning servo angle and servo dist
global distance
distance = [0]
global anglelist
anglelist = [0]

# Initialize the game
trim_write(5)
pygame.init()
width, height = 930, 600
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('Robot Radar')
screen.fill((169,169,169,1))
clock = pygame.time.Clock()

def average_distance():
    i = 0
    j = 0
    readings = 3
    current_dist = [0]
    while (i < readings):
        current_dist.append(us_dist(15))
        i += 1
    current_dist.sort()
    mostcom = current_dist[1]
    if (current_dist[j] > mostcom +- 10):
        current_dist.remove(j)
        j += 1
    return sum(current_dist) / len(current_dist)

def obstacles_rotate(obstacles_list, angle_diff, servo_pos):
        updated_list = []
        for tuple in obstacles_list:
            temp_angle = tuple[2] + angle_diff
            #print("inpput angle: {}, updated angle: {}".format(angle_diff,temp_angle));
            distance = (abs(math.sqrt(tuple[0]**2+tuple[1]**2)))
            x = distance * math.cos(math.radians(temp_angle))
            y = distance * math.sin(math.radians(temp_angle))
            updated_list.append((x,y,temp_angle))
        return updated_list
    
def obstacles_translate(obstacles_list, distance_diff):
    if (distance_diff == 0):
        return obstacles_list
    else:
        update_list = []
        for tuple in obstacles_list:
            y = tuple[1] + distance_diff
            if(tuple[0] >= 0):
                update_list.append((tuple[0], y, math.degrees(math.atan(y/tuple[0]))))       
            elif(tuple[0] < 0 and y <= 0):
                hyp = math.sqrt((tuple[0]*tuple[0]) + (y*y))
                farangle = math.degrees(math.asin(tuple[0]/hyp))
                update_list.append((tuple[0], y, (-1)*(90-farangle)))
            else:
                hyp = math.sqrt((tuple[0]*tuple[0]) + (y*y))
                farangle = math.degrees(math.acos(y/hyp))
                update_list.append((tuple[0], y, (90+farangle)))
        return update_list

# main gui loop method
def gui_loop():
    global anglelist
    global distance
    totalDist = 0
    assignPrev()
    lastUpdateHappened = True
    # servo always start at 90 degree
    servo_pos=90 #when run make sure the servo start at the 90 degree or the start
    servo(servo_pos)
    
    enable_encoders()

    # initial robot speed = 100
    set_speed(70)

    # keys initialization for controller
    # key[0]= servo_left, key[1]= servo_right, keys[2]= Info Help,
    # key[4]=w key, key[5]=a key, key[6]=s key, key[7]= d key
    keys = [False,False,False,False,False,False,False,False]
    
    # list of obstacles initialized
    obstacles = []
    
    #for testing purposes only:
    #obstacles = [(30,-30,225),(60,-60,225),(90,-90,225),(-30,-30,315),(-60,-60,315),(-90,-90,315),(-30,30,45),(-60,60,45),(-90,90,45)]
    
    #obstacles = [(10,10,45),(20,20,45),(30,30,45),(40,40,45),(50,50,45),(10,10,135),(20,20,135),(30,30,135),(40,40,135),(50,50,135)]
    # give randome point of obstacles
    # obstacles = [(0,150,90), (-106,106,135), (-15,-250,220), (100,210,60), (200,-260,300)]
    old_angle = 90
    
    # Gui_Loop
    gui_exit = False
    while not gui_exit:
        for event in pygame.event.get():
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_w:
                    keys[4]=False;
                    lastUpdateHappened = False
                    stop();
                elif event.key==pygame.K_a:
                    keys[5]=False;
                    lastUpdateHappened = False
                    stop();
                elif event.key==pygame.K_s:
                    keys[6]=False;
                    lastUpdateHappened = False
                    stop();
                elif event.key==pygame.K_d:
                    keys[7]=False;
                    lastUpdateHappened = False
                    stop();
                elif event.key==pygame.K_UP:
                    continue;
                elif event.key==pygame.K_DOWN:
                    continue;
                elif event.key==pygame.K_LEFT:
                    keys[0]=False;
                elif event.key==pygame.K_RIGHT:
                    keys[1]=False;
                elif event.key==pygame.K_e:
                    keys[2]=False;
                elif event.key==pygame.K_c:
                    del obstacles[:];
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w:
                    
                    
                    # THE PURGE METHODS IN THIS SECTION IS EXPERIMENTAL
                    purge();
                    fwd();
                    keys[4]=True;
                    #below line is experimental
                    #keys[5] = False;
                    #keys[6] = False;
                    #keys[7] = False;
                elif event.key==pygame.K_a:
                    purge();
                    left_rot();
                    keys[5]=True;
                    #below line is experimental
                    #keys[4] = False;
                    #keys[6] = False;
                    #keys[7] = False;
                elif event.key==pygame.K_s:
                    purge();
                    bwd();
                    keys[6]=True;
                    #below line is epxerimental
                    #keys[4] = False;
                    #keys[5] = False;
                    #keys[7] = False;
                elif event.key==pygame.K_d:
                    purge();
                    right_rot();
                    keys[7]=True;
                    #below line is experimental
                    #keys[4] = False;
                    #keys[6] = False;
                    #keys[7] = False;
                elif event.key==pygame.K_UP:
                    increase_speed();
                elif event.key==pygame.K_DOWN:
                    decrease_speed();
                elif event.key==pygame.K_LEFT:
                    keys[0]=True;
                elif event.key==pygame.K_RIGHT:
                    keys[1]=True;
                elif event.key==pygame.K_e:
                    keys[2]=True;
                elif event.key==pygame.K_z:
                    print('exiting')
                    stop();
                    disable_encoders;
                    sys.exit();
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        if keys[0]:
            servo_pos = servo_pos+10
            if servo_pos >170:
                servo_pos=170;
                enable_servo()
            servo(servo_pos);
            ob_dis = average_distance()
            if (ob_dis<200):
                ydis = math.sin(math.radians(servo_pos))*ob_dis
                xdis = math.cos(math.radians(servo_pos))*ob_dis
                obstacles.append((xdis,ydis,servo_pos))

        elif keys[1]:
            servo_pos = servo_pos-10
            if servo_pos<20:
                servo_pos=20;
            servo(servo_pos);
            ob_dis = average_distance()
            if (ob_dis<200):
                xdis = math.cos(math.radians(servo_pos))*ob_dis
                ydis = math.sin(math.radians(servo_pos))*ob_dis
                obstacles.append((xdis,ydis,servo_pos))
    
        if keys[4]: #fwd
            enc_data_write(4)
        elif keys[5]: #left
            enc_data_write(5)
        elif keys[6]: #bwd
            enc_data_write(6)
        elif keys[7]: #right
            enc_data_write(7);
       # else:
      #      if (lastUpdateHappened == False):
     #           callval = getLastCall();
    #            enc_data_write(callval)
   #             lastUpdateHappened = True;
                
        if keys[2]:
            # repaint everything 
            screen.fill((171,171,171,1))
            pop_up = pygame.image.load(os.getcwd()+"/images/Info Pop Up.png")
            screen.blit(pop_up,(0,0))
            pygame.display.update()
        else:
            #ob_dis = us_dist(15)
            #print(ob_dis)
            #if (ob_dis<300):
            #    obstacles.append((0,ob_dis,servo_pos))
            angletemp = getAngle()
            angletemp2 = angletemp
            angle_diff = old_angle - angletemp
            old_angle = angletemp2
            #angletemp = getAngle()
            #angle_diff = old_angle - angletemp
            #old_angle = getAngle()
            if angle_diff != 0:
                obstacles = obstacles_rotate(obstacles,angle_diff,servo_pos)
            testthing = getTotalDist()                
            distUpdate = (testthing - totalDist)
            #distUpdate = (getTotalDist() - totalDist)
            totalDist = getTotalDist()
            if distUpdate != 0:
                #print("input distance: {} totaldist: {} output distance: {}".format(testthing,totalDist,((-1)*distUpdate)));
                obstacles = obstacles_translate(obstacles,(-1)*distUpdate)
            #if(getLastDist() != 0):
            #1    setZero()
            gui_update(screen,getAngle(),obstacles)

        clock.tick(120)
            

gui_loop()
pygame.quit()
sys.exit()


