#!/usr/bin/env python

import pygame
import os
from rational import rational
from random import choice

pygame.init()



#For Compiling
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



#Basic Information
CAPTION = "Physical pi calculator"
ICON = resource_path("icon.png")
WIDTH = 640
HEIGHT = 360
TARGET_FRAME_RATE = 144
MAGNIFYING_RATE = 60



#Colors
BLACK   = (  0,   0,   0)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255,   0)
MAGENTA = (255,   0, 255)
CYAN    = (  0, 255, 255)
WHITE   = (255, 255, 255)

#Extended Colors
LIGHT_GRAY  = (240, 240, 240)
LIGHT_GREEN = (144, 238, 144)
DARK_GRAY   = (120, 120, 120)



#Preset
RUNNING = True
WINDOW = pygame.display
WINDOW.set_caption(CAPTION)
WINDOW.set_icon(pygame.image.load(ICON))
SCREEN = WINDOW.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)



#Global Variables
FLOOR_HEIGHT = HEIGHT // 4
WALL_THICKNESS = 80
PAUSED = True
STATUS = "Simulate"
TEXT_BOX_INFO = {"Size": "", "Mass": "", "Position": "", "Velocity": "", "Color": ""}
ERROR_MESSAGE_TIMER = 0
PAUSE_BUTTON_FLAG = True
ERROR_MESSAGE = ""
CLICKED_TEXT_BUTTON = None
SPEED = 1

COLLISION = 0
COLLISION_TIMER = rational(0)
PAST_COLLIDE = 0
PRED_COLLIDER = None

collider = []



#Classes
class box():
    def __init__(self, length: rational, mass: rational, position: rational, velocity: rational, color: tuple):
        self.length = length
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.color = color
    def __repr__(self):
        return "Box{%skg, %sm, %sm/s, Color: %s}" % (mass, position, velocity, color)
    def info(self):
        return (self.length, self.mass, self.position, self.velocity, self.color)
    def update(self, colider: list):
        pass
    def render(self):
        pygame.draw.rect(SCREEN, self.color, [float(WALL_THICKNESS + self.position * MAGNIFYING_RATE), float(HEIGHT - FLOOR_HEIGHT - self.length * MAGNIFYING_RATE), float(self.length * MAGNIFYING_RATE), float(self.length * MAGNIFYING_RATE)])
    def copy(self):
        return box(self.length, self.mass, self.position, self.velocity, self.color)



#Functions
def print_text(text = "", pos = (0, 0), center_align = False, font = None, font_size = 18, color = BLACK, alpha = 255):
    split_text = list(text.split("\n"))
    font = pygame.font.SysFont(font, font_size)
    for i in range(len(split_text)):
        txt = font.render(split_text[i], True, color)
        txt.set_alpha(alpha)
        if center_align:
            rect = txt.get_rect()
            rect.center = (pos[0], pos[1] + (2 * i - len(split_text) + 1) * font_size // 2)
            SCREEN.blit(txt, rect)
        else:
            SCREEN.blit(txt, (pos[0], pos[1] + font_size * i))
            
def FLOOR_relocation():
    global FLOOR_HEIGHT
    FLOOR_HEIGHT = HEIGHT // 4

def render_restart_button():
    pygame.draw.rect(SCREEN, RED, [WALL_THICKNESS // 8, WALL_THICKNESS // 8, WALL_THICKNESS * 3 // 4, WALL_THICKNESS * 3 // 8], 0, WALL_THICKNESS * 3 // 24)
    print_text("RS", (WALL_THICKNESS // 2, WALL_THICKNESS * 5 // 16), True, None, 24, WHITE)

def restart_button_clicked():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    if click and WALL_THICKNESS // 8 <= mouse[0] < WALL_THICKNESS * 7 // 8 and WALL_THICKNESS // 8 <= mouse[1] < WALL_THICKNESS // 2:
        return True
    return False

def render_pause_button():
    if PAUSED:
        bgcolor = LIGHT_GREEN
        fgcolor = BLACK
        text = "RUN"
    else:
        bgcolor = MAGENTA
        fgcolor = WHITE
        text = "PAUSE"
    pygame.draw.rect(SCREEN, bgcolor, [WALL_THICKNESS // 8, WALL_THICKNESS * 5 // 8, WALL_THICKNESS * 3 // 4, WALL_THICKNESS * 3 // 8], 0, WALL_THICKNESS * 3 // 24)
    print_text(text, (WALL_THICKNESS // 2, WALL_THICKNESS * 13 // 16), True, None, 18, fgcolor)

def pause_button_clicked():
    global PAUSE_BUTTON_FLAG
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    if click and WALL_THICKNESS // 8 <= mouse[0] < WALL_THICKNESS * 7 // 8 and WALL_THICKNESS * 5 // 8 <= mouse[1] < WALL_THICKNESS:
        if PAUSE_BUTTON_FLAG == True:
            PAUSE_BUTTON_FLAG = False
            return True
        return False
    PAUSE_BUTTON_FLAG = True
    return False

def render_collision_counter():
    print_text("Collisions: %d" % COLLISION, (WALL_THICKNESS * 9 // 8, WALL_THICKNESS // 8), False, None, 24)

def render_pause_ui():
    if not PAUSED:
        return
    print_text("Paused", (WIDTH - 64, WALL_THICKNESS // 8), False, None, 24)

def collider_update():
    global COLLISION, COLLISION_TIMER, PRED_COLLIDER, PAST_COLLIDE, collider
    while COLLISION_TIMER < rational(1, TARGET_FRAME_RATE): #While there is not-processed collision in the current frame
        if PRED_COLLIDER != None: #if it is valid collision
            #Move to the collision
            for i in collider:
                i.position += i.velocity * PAST_COLLIDE
            #Collision with the wall
            if PRED_COLLIDER[0] == "Wall":
                PRED_COLLIDER[1].velocity = -PRED_COLLIDER[1].velocity
            #Collision between colliders
            else:
                c1 = PRED_COLLIDER[0]
                c2 = PRED_COLLIDER[1]
                m1 = c1.mass
                m2 = c2.mass
                v1 = c1.velocity
                v2 = c2.velocity
                c1.velocity = (v1 * (m1 - m2) + 2 * m2 * v2) / (m1 + m2)
                c2.velocity = (v2 * (m2 - m1) + 2 * m1 * v1) / (m2 + m1)
            COLLISION += 1
        #Next collision prediction
        NCT = rational("inf") #Next Collision Time
        PRED_COLLIDER = None
        for i in collider:
            if i.velocity < 0:
                CCT = i.position / abs(i.velocity) #Current Collision Time
                if CCT < NCT:
                    NCT = CCT
                    PRED_COLLIDER = ["Wall", i]
            for j in collider:
                L, R = sorted([i, j], key = lambda x: x.position)
                if R.velocity < L.velocity:
                    CCT = (R.position - L.position - L.length) / (L.velocity - R.velocity)
                    if CCT < NCT:
                        NCT = CCT
                        PRED_COLLIDER = [L, R]
        #End of prediction
        PAST_COLLIDE = NCT
        COLLISION_TIMER += NCT
    if COLLISION_TIMER == rational("inf"):
        for i in collider:
            i.position += i.velocity * rational(1, TARGET_FRAME_RATE)
    else:
        MOV_TIME = rational(1, TARGET_FRAME_RATE) - (COLLISION_TIMER - PAST_COLLIDE)
        for i in collider:
            i.position += i.velocity * MOV_TIME
        COLLISION_TIMER -= rational(1, TARGET_FRAME_RATE)
        PAST_COLLIDE = COLLISION_TIMER

def render_size_input_box():
    pygame.draw.rect(SCREEN, WHITE, [WIDTH * 2 // 5, HEIGHT * 7 // 24, WIDTH * 7 // 20, 24])

def size_button_clicked():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    if click and WIDTH * 2 // 5 <= mouse[0] < WIDTH * 3 // 4 and HEIGHT * 7 // 24 <= mouse[1] < HEIGHT * 7 // 24 + 24:
        return True
    return False

def render_mass_input_box():
    pygame.draw.rect(SCREEN, WHITE, [WIDTH * 2 // 5, HEIGHT * 9 // 24, WIDTH * 7 // 20, 24])

def mass_button_clicked():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    if click and WIDTH * 2 // 5 <= mouse[0] < WIDTH * 3 // 4 and HEIGHT * 9 // 24 <= mouse[1] < HEIGHT * 9 // 24 + 24:
        return True
    return False
    
def render_position_input_box():
    pygame.draw.rect(SCREEN, WHITE, [WIDTH * 2 // 5, HEIGHT * 11 // 24, WIDTH * 7 // 20, 24])

def position_button_clicked():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    if click and WIDTH * 2 // 5 <= mouse[0] < WIDTH * 3 // 4 and HEIGHT * 11 // 24 <= mouse[1] < HEIGHT * 11 // 24 + 24:
        return True
    return False
    
def render_velocity_input_box():
    pygame.draw.rect(SCREEN, WHITE, [WIDTH * 2 // 5, HEIGHT * 13 // 24, WIDTH * 7 // 20, 24])

def velocity_button_clicked():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    if click and WIDTH * 2 // 5 <= mouse[0] < WIDTH * 3 // 4 and HEIGHT * 13 // 24 <= mouse[1] < HEIGHT * 13 // 24 + 24:
        return True
    return False
    
def render_color_input_box():
    pygame.draw.rect(SCREEN, WHITE, [WIDTH * 2 // 5, HEIGHT * 15 // 24, WIDTH * 7 // 20, 24])

def color_button_clicked():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    if click and WIDTH * 2 // 5 <= mouse[0] < WIDTH * 3 // 4 and HEIGHT * 15 // 24 <= mouse[1] < HEIGHT * 15 // 24 + 24:
        return True
    return False

def render_add_button():
    pygame.draw.rect(SCREEN, RED, [WIDTH * 7 // 24, HEIGHT * 19 // 24, WIDTH // 6, HEIGHT // 12], 0, HEIGHT // 30)
    print_text("ADD", (WIDTH * 3 // 8, HEIGHT * 5 // 6), True, None, 24, WHITE)

def add_button_clicked():
    global PAUSE_BUTTON_FLAG
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    if click and WIDTH * 7 // 24 <= mouse[0] < WIDTH * 11 // 24 and HEIGHT * 19 // 24 <= mouse[1] < HEIGHT * 21 // 24:
        if PAUSE_BUTTON_FLAG == True:
            PAUSE_BUTTON_FLAG = False
            return True
        return False
    PAUSE_BUTTON_FLAG = True
    return False

def render_done_button():
    pygame.draw.rect(SCREEN, GREEN, [WIDTH * 13 // 24, HEIGHT * 19 // 24, WIDTH // 6, HEIGHT // 12], 0, HEIGHT // 30)
    print_text("DONE", (WIDTH * 5 // 8, HEIGHT * 5 // 6), True, None, 24, BLACK)

def done_button_clicked():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    if click and WIDTH * 13 // 24 <= mouse[0] < WIDTH * 17 // 24 and HEIGHT * 19 // 24 <= mouse[1] < HEIGHT * 21 // 24:
        return True
    return False

def render_speed_ui():
    print_text("Speed: x%s" % SPEED, (WALL_THICKNESS * 9 // 8, WALL_THICKNESS // 8 + 18), False, None, 24)

def render_version_ui():
    print_text("Version: A1.00", (WIDTH - 50, HEIGHT - 14), True, None, 18, WHITE)



#Main Code
collider.append(box(length = rational(1), mass = rational(1), position = rational(2), velocity = rational(0), color = RED))
collider.append(box(length = rational(1), mass = rational(1), position = rational(5), velocity = rational(-1), color = BLUE))



#Main Loop
while RUNNING:
    pygame.time.Clock().tick(TARGET_FRAME_RATE)

    #Simulating
    if STATUS == "Simulate":
        #Render Background, Floor and Wall
        SCREEN.fill(LIGHT_GRAY)
        pygame.draw.rect(SCREEN, BLACK, [0, HEIGHT - FLOOR_HEIGHT, WIDTH, FLOOR_HEIGHT])
        pygame.draw.rect(SCREEN, BLACK, [0, 0, WALL_THICKNESS, HEIGHT])

        #Render Colliders
        for i in collider:
            i.render()

        #Render UIs
        render_restart_button()
        render_pause_button()
        render_collision_counter()
        render_pause_ui()
        #render_speed_ui()
        render_version_ui()

        #Update Collider Status
        if not PAUSED:
            collider_update()

        #Interrupt
        if restart_button_clicked():
            STATUS = "Reset"
            collider = []
            TEXT_BOX_INFO = {"Size": "", "Mass": "", "Position": "", "Velocity": "", "Color": ""}
            COLLISION = 0
            COLLISION_TIMER = rational(0)
            PRED_COLLIDER = None
            SPEED = 1
        if pause_button_clicked():
            if PAUSED:
                PAUSED = False
            else:
                PAUSED = True

    #New Experiment Setting
    if STATUS == "Reset":
        #Render Background and Input Textbox
        SCREEN.fill(DARK_GRAY)
        print_text("Add new collider", (WIDTH // 2, HEIGHT // 6), True, None, 36, WHITE)
        print_text("Size    : ", (WIDTH // 4, HEIGHT * 7 // 24), False, None, 24, WHITE)
        print_text("Mass    : ", (WIDTH // 4, HEIGHT * 9 // 24), False, None, 24, WHITE)
        print_text("Position: ", (WIDTH // 4, HEIGHT * 11 // 24), False, None, 24, WHITE)
        print_text("Velocity: ", (WIDTH // 4, HEIGHT * 13 // 24), False, None, 24, WHITE)
        print_text("Color   : ", (WIDTH // 4, HEIGHT * 15 // 24), False, None, 24, WHITE)
        render_size_input_box()
        render_mass_input_box()
        render_position_input_box()
        render_velocity_input_box()
        render_color_input_box()
        render_add_button()
        render_done_button()
        print_text(TEXT_BOX_INFO["Size"], (WIDTH * 2 // 5 + 4, HEIGHT * 7 // 24 + 4), False, None, 24, BLACK)
        print_text(TEXT_BOX_INFO["Mass"], (WIDTH * 2 // 5 + 4, HEIGHT * 9 // 24 + 4), False, None, 24, BLACK)
        print_text(TEXT_BOX_INFO["Position"], (WIDTH * 2 // 5 + 4, HEIGHT * 11 // 24 + 4), False, None, 24, BLACK)
        print_text(TEXT_BOX_INFO["Velocity"], (WIDTH * 2 // 5 + 4, HEIGHT * 13 // 24 + 4), False, None, 24, BLACK)
        print_text(TEXT_BOX_INFO["Color"], (WIDTH * 2 // 5 + 4, HEIGHT * 15 // 24 + 4), False, None, 24, BLACK)

        #Interrupt
        if add_button_clicked():
            try:
                if TEXT_BOX_INFO["Color"] != "":
                    exec("color = %s" % TEXT_BOX_INFO["Color"].upper())
                else:
                    color = choice([RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, LIGHT_GREEN])
                sz = float(TEXT_BOX_INFO["Size"])
                ms = float(TEXT_BOX_INFO["Mass"])
                ps = float(TEXT_BOX_INFO["Position"])
                vc = float(TEXT_BOX_INFO["Velocity"])
                collider.append(box(sz, ms, ps, vc, color))
                ERROR_MESSAGE_TIMER = TARGET_FRAME_RATE * 2
                ERROR_MESSAGE = "Collider added successfully"
                TEXT_BOX_INFO = {"Size": "", "Mass": "", "Position": "", "Velocity": "", "Color": ""}
            except:
                ERROR_MESSAGE_TIMER = TARGET_FRAME_RATE * 2
                ERROR_MESSAGE = "Some of inputs are missing or wrong!"
            CLICKED_TEXT_BUTTON = None
            
        if done_button_clicked():
            STATUS = "Simulate"
            PAUSED = True
            ERROR_MESSAGE_TIMER = 0
            CLICKED_TEXT_BUTTON = None
        if size_button_clicked():
            CLICKED_TEXT_BUTTON = "Size"
            TEXT_BOX_INFO["Size"] = ""
        if mass_button_clicked():
            CLICKED_TEXT_BUTTON = "Mass"
            TEXT_BOX_INFO["Mass"] = ""
        if position_button_clicked():
            CLICKED_TEXT_BUTTON = "Position"
            TEXT_BOX_INFO["Position"] = ""
        if velocity_button_clicked():
            CLICKED_TEXT_BUTTON = "Velocity"
            TEXT_BOX_INFO["Velocity"] = ""
        if color_button_clicked():
            CLICKED_TEXT_BUTTON = "Color"
            TEXT_BOX_INFO["Color"] = ""
        if CLICKED_TEXT_BUTTON != None:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if TEXT_BOX_INFO[CLICKED_TEXT_BUTTON] != "":
                            TEXT_BOX_INFO[CLICKED_TEXT_BUTTON] = TEXT_BOX_INFO[CLICKED_TEXT_BUTTON][:-1]
                    elif event.key == pygame.K_TAB:
                        if CLICKED_TEXT_BUTTON == "Size":
                            CLICKED_TEXT_BUTTON = "Mass"
                            TEXT_BOX_INFO["Mass"] = ""
                        elif CLICKED_TEXT_BUTTON == "Mass":
                            CLICKED_TEXT_BUTTON = "Position"
                            TEXT_BOX_INFO["Position"] = ""
                        elif CLICKED_TEXT_BUTTON == "Position":
                            CLICKED_TEXT_BUTTON = "Velocity"
                            CLICKED_TEXT_BUTTON = "Velocity"
                        elif CLICKED_TEXT_BUTTON == "Velocity":
                            CLICKED_TEXT_BUTTON = "Color"
                            TEXT_BOX_INFO["Color"] = ""
                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        try:
                            if TEXT_BOX_INFO["Color"] != "":
                                exec("color = %s" % TEXT_BOX_INFO["Color"].upper())
                            else:
                                color = choice([RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, LIGHT_GREEN])
                            sz = float(TEXT_BOX_INFO["Size"])
                            ms = float(TEXT_BOX_INFO["Mass"])
                            ps = float(TEXT_BOX_INFO["Position"])
                            vc = float(TEXT_BOX_INFO["Velocity"])
                            collider.append(box(sz, ms, ps, vc, color))
                            ERROR_MESSAGE_TIMER = TARGET_FRAME_RATE * 2
                            ERROR_MESSAGE = "Collider added successfully"
                            TEXT_BOX_INFO = {"Size": "", "Mass": "", "Position": "", "Velocity": "", "Color": ""}
                            CLICKED_TEXT_BUTTON = "Size"
                        except:
                            ERROR_MESSAGE_TIMER = TARGET_FRAME_RATE * 2
                            ERROR_MESSAGE = "Some of inputs are missing or wrong!"
                    else:
                        TEXT_BOX_INFO[CLICKED_TEXT_BUTTON] += event.unicode
        #Error Message
        if 0 < ERROR_MESSAGE_TIMER:
            print_text(ERROR_MESSAGE, (WIDTH // 2, HEIGHT * 3 / 4), True, None, 18, WHITE, 255 * ERROR_MESSAGE_TIMER // TARGET_FRAME_RATE)
            ERROR_MESSAGE_TIMER -= 1

    #Refresh Screen
    pygame.display.update()

    #Event Processing
    for event in pygame.event.get():

        #Quit Button Action
        if event.type == pygame.QUIT:
            pygame.display.quit()
            RUNNING = False

        #Update Size
        elif event.type == pygame.VIDEORESIZE:
            WIDTH = event.w
            HEIGHT = event.h
            FLOOR_relocation()
