import pygame
import os
import sys
import time
import RPi.GPIO as GPIO
from pygame.locals import *

# cat /proc/bus/input/devices
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/event2"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

# define basic colors
# color    R    G    B
white = (255, 255, 255)
black = (0, 0, 0)

auto = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)

auto_off = (128, 128, 128)
red_off = (132, 0, 0)
yellow_off = (132, 130, 0)
green_off = (0, 130, 0)

signal_color_on = (red, yellow, green)
signal_color_off = (red_off, yellow_off, green_off)

# screen size
width = 480
height = 320
fontsize = 60
debugsize = 25

box = 3
box_margin = 10
box_width = (width - (box_margin * (box + 1))) / box
box_height = height - (box_margin * 2)
box_signal = box_height / 3

# timer
refresh = 0.01
auto_green = 2  # Same for Red
auto_yellow = 0.4

# Signal (Red, Yellow, Green) with GPIO.BCM
signal_pin = [[19, 13, 26], [20, 21, 16]]

# initial state
state_auto = False
state_signal = [[True, False, False], [True, False, False]]
auto_counter = 0

# setup gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(signal_pin[0], GPIO.OUT)
GPIO.setup(signal_pin[1], GPIO.OUT)

# setup pygame
pygame.init()
screen = pygame.display.set_mode((width, height), FULLSCREEN)
screen.fill(black)

running = True
while running:
    for event in pygame.event.get():
        # close
        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            running = False
            GPIO.cleanup()
            pygame.quit()
            sys.exit()

        # if touchscreen pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            # get position
            pos = (pygame.mouse.get_pos()[0],
                   pygame.mouse.get_pos()[1])
            pos_color = screen.get_at((pos[0], pos[1]))

            # check by box
            for n in range(3):
                pos_min = box_margin * (n + 1) + box_width * n
                pos_max = pos_min + box_width
                # check clicked box
                if pos[0] > pos_min and pos[0] < pos_max:
                    if n == 0:
                        # auto
                        state_auto = ~state_auto
                        state_signal = [[True, False, False],
                                        [False, False, True]]
                        auto_counter = 0
                    elif n > 0 and pos_color != white and pos_color != black:
                        # signal
                        for c in range(3):
                            if signal_color_off[c] == pos_color:
                                # off -> on
                                state_auto = False
                                state_signal[n - 1] = [False, False, False]
                                state_signal[n - 1][c] = True
            screen.fill(black)
            # screen.blit(pygame.font.Font(None, debugsize).render(str(pos_color), 1, white), (0, 0))

    # Auto
    if state_auto:
        screen.fill(black)
        # screen.blit(pygame.font.Font(None, debugsize).render(str(auto_counter), 1, white), (0, 0))
        if state_signal[1][1] == True and auto_counter >= auto_yellow:
            # 2) Yellow -> Red
            # 1) Red -> Green
            state_signal[0][0] = False
            state_signal[0][2] = True
            state_signal[1][0] = True
            state_signal[1][1] = False
            auto_counter = 0
        elif state_signal[0][1] == True and auto_counter >= auto_yellow:
            # 1) Yellow -> Red
            # 2) Red -> Green
            state_signal[0][0] = True
            state_signal[0][1] = False
            state_signal[1][0] = False
            state_signal[1][2] = True
            auto_counter = 0
        elif state_signal[0][2] == True and auto_counter >= auto_green:
            # 1) Green -> Yellow
            state_signal[0][1] = True
            state_signal[0][2] = False
            auto_counter = 0
        elif state_signal[1][2] == True and auto_counter >= auto_green:
            # 2) Green -> Yellow
            state_signal[1][1] = True
            state_signal[1][2] = False
            auto_counter = 0

    # render auto
    if state_auto:
        color_state = auto
    else:
        color_state = auto_off
    str_auto = pygame.font.Font(None, fontsize).render(
        "A u t o", 1, color_state)
    screen.blit(pygame.transform.rotate(str_auto, 90),
                (box_margin + (box_width / 2) - (fontsize / 3), (height / 2) - (7 * 10)))

    # render box and signal
    for n in range(3):
        pos_x = box_margin * (n + 1) + box_width * n
        pos_y = box_margin
        pygame.draw.rect(screen, white, Rect(
            pos_x, pos_y, box_width, box_height), 1)
        if n > 0:
            for m in range(3):
                circle_x = pos_x + box_signal / 2 + \
                    ((box_width - box_signal) / 2)
                circle_y = pos_y + box_signal / 2 + box_signal * m
                if state_signal[n - 1][m]:
                    circle_color = signal_color_on[m]
                    GPIO.output(signal_pin[n - 1][m], GPIO.HIGH)
                else:
                    circle_color = signal_color_off[m]
                    GPIO.output(signal_pin[n - 1][m], GPIO.LOW)
                pygame.draw.circle(
                    screen, circle_color, (circle_x, circle_y), box_signal / 2, 0)

    # refresh screen
    pygame.display.update()
    if state_auto:
        auto_counter += refresh
    time.sleep(refresh)
