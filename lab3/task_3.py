import math as m
import random as r
import pygame
from pygame.draw import *

pygame.init()

x_size = 500
y_size = 650

screen = pygame.display.set_mode((x_size, y_size))
screen.fill((225, 225, 225))

def background (a_size, b_size):
    rect(screen, (0, 70, 100), (0, b_size // 2, a_size, b_size))
    rect(screen, (255, 150, 100), (0, b_size // 2 - b_size // 10, a_size, b_size // 10))
    rect(screen, (255, 100, 150), (0, b_size // 2 - 2 *  b_size // 10 - b_size // 20, a_size, b_size // 10 + b_size // 20))
    rect(screen, (200, 100, 225), (0, b_size // 10 + b_size // 20, a_size, b_size // 10 + 2))
    rect(screen, (150, 100, 225), (0, b_size // 10, a_size, b_size // 20))
    rect(screen, (50, 0, 150), (0, 0, a_size, b_size // 10))

def seagull_position_color (y):
    if y < y_size // 10:
        return (50, 0, 150)
    if y > y_size // 10 and y < y_size // 10 + y_size // 20:
        return (150, 100, 225)
    if y > y_size // 10 + y_size // 20 and y < y_size // 5 + y_size // 20:
        return (200, 100, 225)
    if y > y_size // 5 + y_size // 20 and y < 2 * y_size // 5:
        return (255, 100, 150)
    if y > y_size // 2 - y_size // 10:
        return (255, 150, 100)

def seagull (x, y, r, angle):
    surf = pygame.Surface((2 * r, int (r * (1 - 3 ** 0.5 / 2))), pygame.SRCALPHA)
    surf.fill(seagull_position_color (y))
    surf.set_alpha(0)
    arc(surf, (255, 255, 255), (- r // 2, 0, r * 2, r * 2), m.pi / 3, 2 * m.pi / 3, 2)
    arc(surf, (255, 255, 255), (r // 2, 0, r * 2, r * 2), m.pi / 3, 2 * m.pi / 3, 2)
    surf = pygame.transform.rotate(surf, angle)
    screen.blit(surf, (x - r, y - int (r * (1 - 3 ** 0.5 / 2))))


def fish (x, y, size):

    polygon(screen, (200, 100, 50),[(x - size // 3, y - size // 3), (x + size // 5, y - size // 3), (x, y)], 0)
    aalines(screen, (0, 0, 0), True,
            [(x - size // 3, y - size // 3), (x + size // 5, y - size // 3), (x, y)])
    

    polygon(screen,
            (200, 100, 50),
            [(x, y), (x - 3 * size // 8, y + size // 4), (x - size // 2 - size // 8, y + size // 4)],
            0)
    aalines(screen, (0, 0, 0), True,
            [(x, y), (x - 3 * size // 8, y + size // 4), (x - size // 2 - size // 8, y + size // 4)])
   

    polygon(screen, (200, 100, 50), [(x - size // 8, y), (x, y + size // 3), (x + size // 2, y + size // 3)], 0)
    aalines(screen, (0, 0, 0), True,
            [(x - size // 8, y), (x, y + size // 3), (x + size // 2, y + size // 3)])
    

    ellipse(screen, (0, 100, 100), (x - size // 2, y - size // 4, size, size // 2))
    ellipse(screen, (0, 0, 0), (x - size // 2, y - size // 4, size, size // 2), 1)
    x01 = x + size // 4
    x02 = x - size // 4
    y01 = y + size // 5
    y02 = y - size // 5
    polygon(screen, (0, 100, 100),[(x01, y01), (x + 3 * size // 4, y), (x01, y02)], 0)
    line(screen, (0, 0, 0), (x01, y01), (x + 3 * size // 4, y), 1)
    line(screen, (0, 0, 0), (x01, y02), (x + 3 * size // 4, y), 1)

    polygon(screen, (0, 100, 100),[(x02, y01), (x - 3 * size // 4, y), (x02, y02)], 0)
    line(screen, (0, 0, 0), (x02, y01), (x - 3 * size // 4, y), 1)
    line(screen, (0, 0, 0), (x02, y02), (x - 3 * size // 4, y), 1)

    x_front_tail = x - 3 * size // 4
    tail_width = size // 5
    tail_height = size // 7
    polygon(screen,
            (0, 100, 100),
            [(x_front_tail, y), (x_front_tail - tail_width, y - tail_height),(x_front_tail - tail_width, y + tail_height)],
            0)
    aalines(screen, (0, 0, 0), True,
            [(x_front_tail, y), (x_front_tail - tail_width, y - tail_height), (x_front_tail - tail_width, y + tail_height)])
    
    r_eye = size // 15
    ellipse(screen, (0, 0, 255), (x + size // 4 - r_eye, y - r_eye, r_eye * 2, r_eye * 2))
    ellipse(screen, (0, 0, 0), (x + size // 4 - r_eye, y - r_eye, r_eye * 2, r_eye * 2), 1)

def big_bird (x, y, size, right_or_left):
    x_torso = x
    y_torso = y
    torso_size = size
    
    neck_size = torso_size // 2
    y_neck = y_torso - torso_size // 10
    if right_or_left == 'right':
        x_neck = x_torso + torso_size // 2
    else:
        x_neck = x_torso - torso_size // 2
    
    head_size_x = size // 3
    head_size_y = int (2 * head_size_x // 3)
    y_head = y_neck - neck_size // 4
    if right_or_left == 'right':
        x_head = x_neck + neck_size // 2
    else:
        x_head = x_neck - neck_size // 2
    
    eye_size_x = head_size_x // 5
    eye_size_y = head_size_y // 5
    y_eye = y_head - head_size_y // 6
    if right_or_left == 'right':
        x_eye = x_head + head_size_x // 4
    else:
        x_eye = x_head - head_size_x // 4
    
    beak_height = head_size_y // 3
    beak_length = head_size_x
    y_beak_upper = y_head - beak_height // 2
    y_beak_lower = y_head + beak_height // 2
    y_beak_middle = y_head
    if right_or_left == 'right':
        x_beak_right = x_head + head_size_x // 4
        x_beak_left = x_beak_right + beak_length
    else:
        x_beak_right = x_head - head_size_x // 4
        x_beak_left = x_beak_right - beak_length
    
    thigh_size = neck_size
    y_thigh_upper = y_torso
    x_thigh_right = x_torso + torso_size // 6
    x_thigh_left = x_torso - torso_size // 6

    calf_size = thigh_size // 4
    x_calf_left = x_thigh_left
    x_calf_right = x_thigh_right
    y_calf = y_thigh_upper + thigh_size - thigh_size // 8

    claw_length = calf_size
    y_claws = y_calf + calf_size
    y_upper_claw = y_claws - claw_length // 2
    y_lower_claw = y_claws + claw_length // 2
    if right_or_left == 'right':
        x_claws_right = x_calf_right + calf_size
        x_upper_and_lower_claws_right = x_claws_right + int (claw_length * 3**0.5 / 2)
        x_claws_left = x_calf_left + calf_size
        x_upper_and_lower_claws_left = x_claws_left + int (claw_length * 3**0.5 / 2)
    else:
        x_claws_right = x_calf_right - calf_size
        x_upper_and_lower_claws_right = x_claws_right - int (claw_length * 3**0.5 / 2)
        x_claws_left = x_calf_left - calf_size
        x_upper_and_lower_claws_left = x_claws_left - int (claw_length * 3**0.5 / 2)

    y_tail_front = y_torso
    y_tail_middle = y_tail_front - torso_size // 2
    y_tail_back = y_tail_front - torso_size // 5
    if right_or_left == 'right':
        x_tail_front = x_torso - torso_size // 3
        x_tail_middle = x_tail_front - torso_size // 5
        x_tail_back = x_tail_front - torso_size // 2
    else:
        x_tail_front = x_torso + torso_size // 3
        x_tail_middle = x_tail_front + torso_size // 5
        x_tail_back = x_tail_front + torso_size // 2

    y_wings_lower = y_torso
    y_wing_front_upper = y_torso - int ((torso_size // 3) * 3**0.5)
    if right_or_left == 'right':
        x_wing_front_lower = x_torso + torso_size // 8
        x_wing_front_upper_right = x_wing_front_lower - torso_size // 4
        x_wing_front_upper_left = x_wing_front_upper_right - 5 * torso_size // 6
    else:
        x_wing_front_lower = x_torso - torso_size // 8
        x_wing_front_upper_right = x_wing_front_lower + torso_size // 4
        x_wing_front_upper_left = x_wing_front_upper_right + 5 * torso_size // 6

    y_wing_back_middle = y_wings_lower - 2 * torso_size // 3
    y_wing_back_upper = y_wing_back_middle - torso_size // 10
    if right_or_left == 'right':
        x_wing_back_lower = x_torso + torso_size // 4
        x_wing_back_middle = x_wing_back_lower - torso_size // 4
        x_wing_back_upper = x_wing_back_middle - 3 * torso_size // 4
    else:
        x_wing_back_lower = x_torso - torso_size // 4
        x_wing_back_middle = x_wing_back_lower + torso_size // 4
        x_wing_back_upper = x_wing_back_middle + 3 * torso_size // 4

    polygon(screen, (255, 255, 255),
            [(x_tail_front, y_tail_front), (x_tail_middle, y_tail_middle), (x_tail_back, y_tail_back)])
    aalines(screen, (0, 0, 0), True,
            [(x_tail_front, y_tail_front), (x_tail_middle, y_tail_middle), (x_tail_back, y_tail_back)])
    
    polygon(screen, (255, 255, 255),
            [(x_wing_back_lower, y_wings_lower), (x_wing_back_middle, y_wing_back_middle), (x_wing_back_upper, y_wing_back_upper)])
    aalines(screen, (0, 0, 0), True,
            [(x_wing_back_lower, y_wings_lower), (x_wing_back_middle, y_wing_back_middle), (x_wing_back_upper, y_wing_back_upper)])
    
    polygon(screen, (255, 255, 255),
            [(x_wing_front_lower, y_wings_lower), (x_wing_front_upper_right, y_wing_front_upper), (x_wing_front_upper_left, y_wing_front_upper)])
    aalines(screen, (0, 0, 0), True,
            [(x_wing_front_lower, y_wings_lower), (x_wing_front_upper_right, y_wing_front_upper), (x_wing_front_upper_left, y_wing_front_upper)])

    aalines(screen, (255, 255, 0), True,
            [(x_beak_right, y_beak_upper), (x_beak_left, y_beak_middle), (x_beak_right, y_beak_lower)])
    polygon(screen, (255, 255, 0),
            [(x_beak_right, y_beak_upper), (x_beak_left, y_beak_middle), (x_beak_right, y_beak_lower)])
    line(screen, (0, 0, 0), (x_beak_right, y_beak_middle), (x_beak_left, y_beak_middle), 1)
    
    ellipse(screen, (255, 255, 255), (x_torso - torso_size // 2, y_torso - torso_size // 4, torso_size, torso_size // 2))
    ellipse(screen, (255, 255, 255), (x_neck - neck_size // 2, y_neck - neck_size // 4, neck_size, neck_size // 2))
    ellipse(screen, (255, 255, 255), (x_head - head_size_x // 2, y_head - head_size_y // 2, head_size_x, head_size_y))
    ellipse(screen, (0, 0, 0), (x_eye - eye_size_x // 2, y_eye - eye_size_y // 2, eye_size_x, eye_size_y))
    ellipse(screen, (255, 255, 255), (x_thigh_right - thigh_size // 8, y_thigh_upper, thigh_size // 4, thigh_size))
    ellipse(screen, (255, 255, 255), (x_thigh_left - thigh_size // 8, y_thigh_upper, thigh_size // 4, thigh_size))

    if right_or_left == 'right':
        line(screen, (255, 255, 255), (x_calf_left, y_calf), (x_calf_left + calf_size, y_calf + calf_size), thigh_size // 6)
        line(screen, (255, 255, 255), (x_calf_right, y_calf), (x_calf_right + calf_size, y_calf + calf_size), thigh_size // 6)
    else:
        line(screen, (255, 255, 255), (x_calf_left, y_calf), (x_calf_left - calf_size, y_calf + calf_size), thigh_size // 6)
        line(screen, (255, 255, 255), (x_calf_right, y_calf), (x_calf_right - calf_size, y_calf + calf_size), thigh_size // 6)

    
    line(screen, (255, 255, 0), (x_claws_right, y_claws), (x_upper_and_lower_claws_right, y_upper_claw), 2)
    line(screen, (255, 255, 0), (x_claws_right, y_claws), (x_upper_and_lower_claws_right, y_lower_claw), 2)
    line(screen, (255, 255, 0), (x_claws_right, y_claws), (x_claws_right, y_claws + claw_length), 2)
    if right_or_left == 'right':
        line(screen, (255, 255, 0), (x_claws_right, y_claws), (x_claws_right + claw_length, y_claws), 2)
    else:
        line(screen, (255, 255, 0), (x_claws_right, y_claws), (x_claws_right - claw_length, y_claws), 2)

    line(screen, (255, 255, 0), (x_claws_left, y_claws), (x_upper_and_lower_claws_left, y_upper_claw), 2)
    line(screen, (255, 255, 0), (x_claws_left, y_claws), (x_upper_and_lower_claws_left, y_lower_claw), 2)
    line(screen, (255, 255, 0), (x_claws_left, y_claws), (x_claws_left, y_claws + claw_length), 2)
    if right_or_left == 'right':
        line(screen, (255, 255, 0), (x_claws_left, y_claws), (x_claws_left + claw_length, y_claws), 2)
    else:
        line(screen, (255, 255, 0), (x_claws_left, y_claws), (x_claws_left - claw_length, y_claws), 2)
        
        
    
background(x_size, y_size)

fish_size = (x_size * y_size) // 4700
fish (3 * x_size // 4, y_size - y_size // 10, fish_size)
fish (x_size // 6, y_size - y_size // 12, fish_size)
fish (5 * x_size // 6, y_size - y_size // 5, fish_size)

seagull_size_big = (x_size * y_size) // 4600
seagull_size_medium = 2 * seagull_size_big // 3
seagull_size_small = seagull_size_medium // 2

seagull (x_size // 6, y_size // 2 - y_size // 5, seagull_size_big, -15)
seagull (2 * x_size // 3, y_size // 4 - y_size // 15, seagull_size_big, 0)
seagull (x_size // 4, y_size // 30, seagull_size_big, 15)


a = r.randint (x_size // 2, x_size // 2 + x_size // 8)
b = r.randint (y_size // 20 + y_size // 40, y_size // 10 - y_size // 40)
seagull (a, b, seagull_size_small, - 15)

a = r.randint (x_size // 2 + x_size // 8, x_size // 2 + x_size // 4)
b = r.randint (y_size // 20 + y_size // 40, y_size // 10 - y_size // 40)
seagull (a, b, seagull_size_small, - 15)

a = r.randint (x_size // 2, x_size // 2 + x_size // 8)
b = r.randint (y_size // 10 + y_size // 40, y_size // 20 + y_size // 10 - y_size // 40)
seagull (a, b, seagull_size_small, - 15)

a = r.randint (x_size // 2 + x_size // 8, x_size // 2 + x_size // 4)
b = r.randint (y_size // 10 + y_size // 40, y_size // 20 + y_size // 10 - y_size // 40)
seagull (a, b, seagull_size_small, - 15)

for i in range (3):
    a = r.randint (x_size // 2 - x_size // 6, x_size // 2 + x_size // 4)
    b = r.randint (y_size // 2 - y_size // 5 + y_size // 40, y_size // 2 - y_size // 10 - y_size // 40)
    seagull (a, b, seagull_size_small, 0)

for i in range (3):
    a = r.randint (x_size // 2 - x_size // 3, x_size // 2 + x_size // 5)
    b = r.randint (y_size // 2 - y_size // 4 + y_size // 40, y_size // 2 - y_size // 5 - y_size // 40)
    seagull (a, b, seagull_size_small, 15)
    
for i in range (2):
    a = r.randint (x_size // 2 - x_size // 3, x_size // 2 + x_size // 5)
    b = r.randint (y_size // 5 + y_size // 40, y_size // 2 - y_size // 4 - y_size // 40)
    seagull (a, b, seagull_size_small, 15)

for i in range (4):
    a = r.randint (x_size // 2 + x_size // 6, x_size - seagull_size_medium)
    b = r.randint (y_size // 2 - 3 * y_size // 10, y_size // 2 - y_size // 10)
    seagull (a, b, seagull_size_medium, 0)

big_bird (x_size // 4, y_size // 2 + y_size // 4, (x_size * y_size) // 2700, 'right')
big_bird (x_size // 2, y_size // 2 + y_size // 15, (x_size * y_size) // 6500, 'right')
big_bird (5 * x_size // 6, y_size // 2 + y_size // 6, (x_size * y_size) // 4800, 'left')

FPS = 30

pygame.display.update()

finished = False
clock = pygame.time.Clock()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
