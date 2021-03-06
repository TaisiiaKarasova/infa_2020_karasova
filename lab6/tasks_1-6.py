import pygame
from pygame.draw import *
import random
pygame.init()

FPS = 15
display_height = 600
display_width = 1200
screen = pygame.display.set_mode((display_width, display_height))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

balls_number = 10
balls = []
balls_velocities = []
logos_number = 4
logos = []
logos_velocities = []
logos_names = ['LOGO_AstroFights.png',
                'LOGO_AstroSandbox.png',
                'LOGO_Kvanta.png',
                'LOGO_KvantaProga.png']

deleted_logos = [0] * logos_number

def main ():
    demonstrate_start_screen()
    demonstrate_game()
    
    if points > last_record():
       save_score_and_name()

    else:
        demonstrate_game_over_screen()   
    
    pygame.quit()


def generate_logos_velocities ():
    for i in range (logos_number):
        velocity_x = random.randint (20, 30)
        velocity_y = random.randint (20, 30)
        logos_velocities.append ([velocity_x, velocity_y])

def generate_logos (screen_width, screen_height):
    for i in range (logos_number):
        x_logo = random.randint(screen_width // 10, 9 * screen_width // 10)
        y_logo = random.randint(screen_height // 10, 9 * screen_height // 10)
        logo_rotation_angle = random.randint (0, 360)
        LOGO = pygame.image.load(logos_names[i])
        LOGO = pygame.transform.scale(LOGO,
                                      (LOGO.get_width()//2, LOGO.get_height()//2))
        logo_radius = LOGO.get_width()//2
        logos.append([x_logo, y_logo, logo_rotation_angle, logo_radius])
    generate_logos_velocities()

def draw_logos ():
    for i in range (logos_number):
        x_logo = logos[i][0]
        y_logo = logos[i][1]
        logos.append([x_logo, y_logo])
        LOGO = pygame.image.load(logos_names[i])
        LOGO = pygame.transform.scale(LOGO,
                                      (LOGO.get_width()//2, LOGO.get_height()//2))
        logo_rotation_angle = logos [i][2]
        logos [i][2] = logo_rotation_angle + 10
        logo_rotation_angle += 10
        LOGO = pygame.transform.rotate(LOGO, logo_rotation_angle)
        LOGO_rect = LOGO.get_rect(center = (x_logo, y_logo))
        if deleted_logos[i] != "deleted":
           screen.blit(LOGO, LOGO_rect)

def logos_move_and_reflect (screen_width, screen_height):
    for i in range (logos_number):
        logos[i][0] += logos_velocities[i][0]
        logos[i][1] += logos_velocities[i][1]
        x_logo = logos[i][0]
        y_logo = logos[i][1]
        LOGO = pygame.image.load(logos_names[i])
        LOGO = pygame.transform.scale(LOGO,
                                      (LOGO.get_width()//2, LOGO.get_height()//2))
        radius_logo = LOGO.get_width() // 2
        logo_radius = balls [i][2]
        if (x_logo <= radius_logo) or (x_logo >= screen_width - radius_logo):
            logos_velocities[i][0] = -logos_velocities[i][0]
        if (y_logo <= radius_logo) or (y_logo >= screen_height - radius_logo):
            logos_velocities[i][1] = -logos_velocities[i][1]   

def generate_balls_velocities ():
    for i in range (balls_number):
        velocity_x = random.randint (1, 10)
        velocity_y = random.randint (1, 10)
        balls_velocities.append ([velocity_x, velocity_y])


def balls_move_and_reflect (screen_width, screen_height):
    for i in range (balls_number):
        balls[i][0] += balls_velocities[i][0]
        balls[i][1] += balls_velocities[i][1]
        ball_x = balls[i][0]
        ball_y = balls[i][1]
        ball_radius = balls [i][2]
        if (ball_x <= ball_radius) or (ball_x >= screen_width - ball_radius):
            balls_velocities[i][0] = -balls_velocities[i][0]
        if (ball_y <= ball_radius) or (ball_y >= screen_height - ball_radius):
            balls_velocities[i][1] = -balls_velocities[i][1]
        
def generate_balls(screen_width, screen_height):
    for i in range (balls_number):
        x = random.randint(screen_width * 0.1, screen_width * 0.9)
        y = random.randint(screen_height * 0.1, screen_height * 0.9)
        radius = random.randint(30,50)
        color = COLORS[random.randint(0, 5)]
        balls.append([x, y, radius, color])
    generate_balls_velocities ()

def draw_balls():
    for i in range (balls_number):
        ball_coords = (balls[i][0], balls[i][1])
        ball_radius = balls[i][2]
        ball_color = balls[i][3]
        circle(screen, ball_color, ball_coords, ball_radius)

def delete_ball (ball_number):
    radius_ball = 0
    balls[ball_number][2] = radius_ball
    color_ball = BLACK
    balls[ball_number][3] = color_ball
    velocity_ball_x = 0
    balls_velocities[ball_number][0] = velocity_ball_x
    velocity_ball_y = 0
    balls_velocities[ball_number][1] = velocity_ball_y

def delete_logo (logo_number):
    deleted_logos[logo_number] = "deleted"

def hitting_the_targets(event, hittings_number):
    for i in range (balls_number):
        x_target = balls[i][0]
        y_target = balls[i][1]
        radius_target = balls[i][2]
        x_click = event.pos[0]
        y_click = event.pos[1]
        distance_click_target = ((x_click - x_target) ** 2
                                 + (y_click - y_target) ** 2) ** 0.5
        if distance_click_target <= radius_target:
           hittings_number += 1
           delete_ball(i)
        
    for i in range (logos_number):
        x_target = logos[i][0]
        y_target = logos[i][1]
        radius_target = logos[i][3]
        x_click = event.pos[0]
        y_click = event.pos[1]
        distance_click_target = ((x_click - x_target) ** 2
                                 + (y_click - y_target) ** 2) ** 0.5
        if distance_click_target <= radius_target:
           hittings_number += 10
           delete_logo(i)
        
    return hittings_number
        
def print_number_up_right_corner (number):
    font = pygame.font.SysFont('arial', 36)
    string_number = 'Points:' + str (number)
    text_number = font.render(string_number, 0, WHITE)
    screen.blit(text_number, (0, 0))
    
def print_time (time, screen_width):
    font = pygame.font.SysFont('arial', 30)
    string_number = 'Time left:' + str (time)
    text_number = font.render(string_number, 0, WHITE)
    screen.blit(text_number, (8 * screen_width // 10, 0))
    
def draw_start_screen (screen_width, screen_height):
    screen.fill(MAGENTA)

    font = pygame.font.SysFont('arial', 72)
    greeting_string = 'Welcome to Catch The LOGO game!'
    greeting_text = font.render(greeting_string, 0, RED)
    screen.blit(greeting_text, (screen_width // 10, screen_height // 10))

    font = pygame.font.SysFont('arial', 32)
    instruction_string = 'You will receive 1 point for catching a ball and 10 points for catching a logo'
    instruction_text = font.render(instruction_string, 0, BLUE)
    screen.blit(instruction_text, (screen_width // 6, screen_height // 4))

    font = pygame.font.SysFont('arial', 32)
    instruction_string = 'You will have 200 seconds. Try to receive as much scores as you can!'
    instruction_text = font.render(instruction_string, 0, BLUE)
    screen.blit(instruction_text, (screen_width // 10, 3 * screen_height // 8))

    font = pygame.font.SysFont('arial', 32)
    instruction_string = 'Click BEGIN to start playing'
    instruction_text = font.render(instruction_string, 0, BLUE)
    screen.blit(instruction_text, (screen_width // 3, screen_height // 2))

    rect (screen, RED, (3 * screen_width // 8, 2 * screen_height // 3,
                        screen_width // 4, screen_height // 4))
    font = pygame.font.SysFont('arial', 100)
    button_string = 'BEGIN '
    button_text = font.render(button_string, 0, BLUE)
    screen.blit(button_text, (19 * screen_width // 48, 17 * screen_height // 24))


def demonstrate_start_screen ():
    global finished
    global start
    start = False
    finished = False
    while not start and not finished:
        draw_start_screen (display_width, display_height)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if click_button (display_width, display_height, event):
                    start = True
    
def show_winner_screen (screen_width, screen_height, new_number, old_number):
    screen.fill(MAGENTA)

    font = pygame.font.SysFont('arial', 72)
    congrats_string = 'You are the best player so far!'
    congrats_text = font.render(congrats_string, 0, RED)
    screen.blit(congrats_text, (screen_width // 10, screen_height // 10))

    font = pygame.font.SysFont('arial', 32)
    result_string = 'You scored ' + str(new_number) + ' while the previous best score was ' + str(old_number)
    result_text = font.render(result_string, 0, BLUE)
    screen.blit(result_text, (screen_width // 6, screen_height // 4))

    font = pygame.font.SysFont('arial', 32)
    ask_string = 'Please click OK and than enter your name into the console'
    ask_text = font.render(ask_string, 0, BLUE)
    screen.blit(ask_text, (screen_width // 10, 3 * screen_height // 8))


    rect (screen, RED, (3 * screen_width // 8, 2 * screen_height // 3,
                        screen_width // 4, screen_height // 4))
    font = pygame.font.SysFont('arial', 100)
    button_string = 'OK '
    button_text = font.render(button_string, 0, BLUE)
    screen.blit(button_text, (43 * screen_width // 96, 17 * screen_height // 24))

def draw_game_over_screen (screen_width, screen_height):
    screen.fill(MAGENTA)

    font = pygame.font.SysFont('arial', 72)
    greeting_string = 'GAME OVER'
    greeting_text = font.render(greeting_string, 0, RED)
    screen.blit(greeting_text, (screen_width // 10, screen_height // 10))

def click_button (screen_width, screen_height, event):
    click_x = event.pos[0]
    click_y = event.pos[1]
    begin_button_x = 3 * screen_width // 8
    begin_button_y = 2 * screen_height // 3
    begin_button_width = screen_width // 4
    begin_button_height = screen_height // 4
    if ((click_x <= begin_button_x + begin_button_width)
        and (click_x >= begin_button_x)
        and (click_y >= begin_button_y)
        and (click_y <= begin_button_y + begin_button_height)):
            return True
    else:
        return False


def last_record ():
    with open('best players.txt') as file:
         for line in file:
             best_score = line
    return int(best_score)

    
def save_score_and_name ():
    finished = False

    show_winner_screen (display_width, display_height, points, last_record())
    pygame.display.update()
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if click_button (display_width, display_height, event):
                    pygame.quit()
                    winner_name = input()
                    out = open('best players.txt', 'a')
                    new_best_score = str(points)
                    string = '\n' + winner_name + '\n' + new_best_score
                    out.write(string)
                    out.close()

    
def demonstrate_game_over_screen():
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        draw_game_over_screen (display_width, display_height)
        pygame.display.update()


def demonstrate_game():
    global points
    global finished
    global balls
    global balls_velocities
    global logos
    global logos_velocities
    global deleted_logos
    points = 0
    balls_left = balls_number
    logos_left = logos_number
    time_left = 3000
    clock = pygame.time.Clock()
    while not finished and time_left > 0:
        clock.tick(FPS)
        generate_balls(display_width, display_height)
        generate_logos(display_width, display_height)
        for i in range (10000):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    old_points = points
                    points = hitting_the_targets(event, points)
                    balls_left -= (points - old_points) % 10
                    logos_left -= (points - old_points) // 10
            if balls_left <= 0:
               balls_left = balls_number
               balls_velocities = []
               balls = []
               generate_balls(display_width, display_height)
            if logos_left <= 0:
               deleted_logos = [0] * logos_number
               logos_left = logos_number
               logos_velocities = []
               logos = []
               generate_logos(display_width, display_height)
            
            balls_move_and_reflect(display_width, display_height)
            logos_move_and_reflect(display_width, display_height)
            time_left -= 1
            print_time(time_left // 15, display_width)
            clock.tick(FPS)
            if finished == True:
                break
            if time_left <= 0:
                break
            draw_logos()
            draw_balls()
            print_number_up_right_corner (points)
            pygame.display.update()      
            screen.fill(BLACK)


main()
