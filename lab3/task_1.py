import pygame
from pygame.draw import *

pygame.init()
FPS = 30

def contageous_line (
    a_center, b_center,
    r, w,
    x_contact, y_contact,
    x_start, x_finish
    ):
    ang_coef = (x_contact - a_center) / (r**2 - (x_contact - a_center)**2)**0.5
    y_start = int (ang_coef * x_start + y_contact - ang_coef * x_contact)
    y_finish = int (ang_coef * x_finish + y_contact - ang_coef * x_contact)
    line(screen, (0, 0, 0), (x_start, y_start), (x_finish, y_finish), w)
    

x_size = 600
y_size = 600

screen = pygame.display.set_mode((x_size, y_size))
screen.fill((225, 225, 225))

x_center = x_size // 2
y_center = y_size // 2
R_face = 100
R_right_eye = R_face // 6
R_left_eye = R_face // 5
R_pupil = R_right_eye // 2

circle(screen, (0, 0, 0), (x_center, y_center), R_face + 2)
circle(screen, (255, 255, 0), (x_center, y_center), R_face)

circle(screen, (0, 0, 0), (x_center - R_face // 2, y_center - R_left_eye), R_left_eye + 1)
circle(screen, (255, 0, 0), (x_center - R_face // 2, y_center - R_left_eye), R_left_eye)
circle(screen, (0, 0, 0), (x_center - R_face // 2, y_center - R_left_eye), R_pupil)

circle(screen, (0, 0, 0), (x_center + R_face // 2, y_center - R_left_eye), R_right_eye + 1)
circle(screen, (255, 0, 0), (x_center + R_face // 2, y_center - R_left_eye), R_right_eye)
circle(screen, (0, 0, 0), (x_center + R_face // 2, y_center - R_left_eye), R_pupil)

line(screen, (0, 0, 0), (x_center - R_face // 2, y_center + R_face // 2), (x_center + R_face // 2, y_center + R_face // 2), 10)

brow_x_contact_left = (x_center - R_face // 2) + R_left_eye // 2
brow_y_contact_left = int ((y_center - R_left_eye) - (R_left_eye) * (3**0.5) / 2)
brow_x_start_left = x_center - R_face // 2 + R_left_eye + R_right_eye
brow_x_finish_left = int (x_center - R_face - R_face / 8)

brow_x_contact_right = (x_center + R_face // 2) - R_right_eye // 2
brow_y_contact_right = int ((y_center - R_left_eye) - (R_right_eye) * (3**0.5) / 2)
brow_x_start_right = x_center + R_face // 2 - 2 * R_left_eye
brow_x_finish_right = int (x_center + R_face + R_face / 15)

contageous_line (x_center - R_face // 2, y_center - R_left_eye,
                 R_left_eye, 7,
                 brow_x_contact_left, brow_y_contact_left,
                 brow_x_start_left, brow_x_finish_left
                 )

contageous_line (x_center + R_face // 2, y_center - R_left_eye,
                 R_right_eye, 7,
                 brow_x_contact_right, brow_y_contact_right,
                 brow_x_start_right, brow_x_finish_right
                 )

pygame.display.update()

finished = False
clock = pygame.time.Clock()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
