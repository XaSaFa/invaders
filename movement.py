import time
from pygame.locals import *
import pygame


# Tamany finestra
VIEW_WIDTH = 640
VIEW_HEIGHT = 360

# iniciem pygame
pygame.init()
pantalla = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
pygame.display.set_caption("Arcade")

# Carreguem imatge de fons
background_image = 'assets/backgrounds/back1.jpg'
background_width = pygame.image.load(background_image).convert().get_width()
background_height = pygame.image.load(background_image).convert().get_height()

# Límits per moure el fons enlloc del personatge
MARGIN_X, MARGIN_Y = VIEW_WIDTH // 2, VIEW_HEIGHT // 2

# Carreguem imatge inicial personatge
player_image = pygame.image.load('assets/sprites/down0.png')
protagonist_speed = 8

# Posicions inicials del personatge i del fons
player_rect = player_image.get_rect(midbottom=(VIEW_WIDTH // 2, VIEW_HEIGHT // 2))
bg_x, bg_y = 0, 0

# Control de FPS
clock = pygame.time.Clock()
fps = 30

# Control de l'animació del personatge
# 1 up. 2 down. 3 right. 4 left
sprite_direction  = "down"
sprite_index = 0
animation_protagonist_speed = 200
sprite_frame_number = 3
last_change_frame_time = 0
idle = False

def imprimir_pantalla_fons(image, x, y):
    # Imprimeixo imatge de fons:
    background = pygame.image.load(image).convert()
    pantalla.blit(background, (x, y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    current_time = pygame.time.get_ticks()

    # Moviment del jugador
    idle = True
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        idle = False
        sprite_direction = "up"
        if player_rect.y > MARGIN_Y or bg_y >= 0:
            player_rect.y = max(player_rect.y - protagonist_speed, player_rect.height // 2)
        else:
            bg_y = min(bg_y + protagonist_speed, 0)

    if keys[K_DOWN]:
        idle = False
        sprite_direction = "down"
        if player_rect.y < VIEW_HEIGHT - MARGIN_Y or bg_y <= VIEW_HEIGHT - background_height:
            player_rect.y = min(player_rect.y + protagonist_speed, VIEW_HEIGHT - player_rect.height // 2)
        else:
            bg_y = max(bg_y - protagonist_speed, VIEW_HEIGHT - background_height)
    if keys[K_RIGHT]:
        idle = False
        sprite_direction = "right"
        if player_rect.x < VIEW_WIDTH - MARGIN_X or bg_x <= VIEW_WIDTH - background_width:
            player_rect.x = min(player_rect.x + protagonist_speed, VIEW_WIDTH - player_rect.width // 2)
        else:
            bg_x = max(bg_x - protagonist_speed, VIEW_WIDTH - background_width)

    if keys[K_LEFT]:
        idle = False
        sprite_direction = "left"
        if player_rect.x > MARGIN_X or bg_x >= 0:
            player_rect.x = max(player_rect.x - protagonist_speed, player_rect.width // 2)
        else:
            bg_x = min(bg_x + protagonist_speed, 0)

    # Dibuixar el fons
    imprimir_pantalla_fons(background_image, bg_x, bg_y)

    # frame number: (there are 3 frames only)
    # selccionem la imatge a mostrar
    if not idle:
        if current_time - last_change_frame_time >= animation_protagonist_speed:
            last_change_frame_time = current_time
            sprite_index = sprite_index + 1
            sprite_index = sprite_index % sprite_frame_number
    else:
        sprite_index = 0
    # dibuixar el jugador
    player_image = pygame.image.load('assets/sprites/'+sprite_direction+str(sprite_index)+'.png')
    pantalla.blit(player_image, player_rect)
    # mantenir el jugador dins la finestra
    player_rect.clamp_ip(pantalla.get_rect())

    pygame.draw.rect(pantalla,(255,255,0),(bg_x+100,bg_y+200,100,10))

    pygame.display.update()
    clock.tick(fps)