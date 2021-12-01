from gopigo import *
import pygame
import math
import os

def cart_to_screen (cart_list):
    screenList = []
    for tuple in cart_list:
        screen_x = tuple[0] + 300
        screen_y = 300 - tuple[1] 
        screenList.append((int(screen_x),int(screen_y)))
    return screenList

def gui_update(screen, robot_angle, obstacles):
    screen.fill((171,171,171,1))

    #rotate robot based on angle
    map = pygame.image.load(os.getcwd()+"/images/Map.png")
    screen.blit(map,(0,0))
    robot = pygame.image.load(os.getcwd()+"/images/robot.png")
    screen.blit(robot,(281,282))
    cart_x = 425* math.cos(math.radians(robot_angle))
    screen_x = cart_x + 300
    cart_y = 425 * math.sin(math.radians(robot_angle))
    screen_y = 300 - cart_y
    #pygame.draw.line(screen,(255, 93, 162), (300,300), (screen_x, screen_y), 3)

    #load images onto screen method
    battery_icon = pygame.image.load(os.getcwd()+"/images/Battery Icon.png")
    info_icon = pygame.image.load(os.getcwd()+"/images/Info icon.png")
    speed_icon = pygame.image.load(os.getcwd()+"/images/Speed Icon.png")
    layer = pygame.image.load(os.getcwd()+"/images/Layer.png")
    arrow_key = pygame.image.load(os.getcwd()+"/images/Arrow Keys.png")
    wasd = pygame.image.load(os.getcwd()+"/images/WASD.png")
    clear = pygame.image.load(os.getcwd()+"/images/clear.png")
    screen.blit(layer, (600,0))
    screen.blit(clear, (664, 307))
    screen.blit(battery_icon,(678,20))
    screen.blit(speed_icon,(664,152))
    screen.blit(info_icon,(664,245))
    screen.blit(arrow_key,(765,389))
    screen.blit(wasd,(605,375))

    #update battery voltage
    font = pygame.font.SysFont(None, 48)
    text = font.render(str(volt()), True, pygame.Color('black'))
    screen.blit(text, (780,54))

    #update robot speed
    currentSpeed = font.render(str(read_motor_speed()), True, pygame.Color('black'))
    screen.blit(currentSpeed, (780, 153))

    #for obstacle in obstacles.keys():
    screen_points = cart_to_screen(obstacles)
    for tuple in screen_points:
        pygame.draw.circle(screen,(255,0,0), tuple, 3)

    #update everything onto the screen
    pygame.display.update()
