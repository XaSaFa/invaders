import time
from pygame.locals import *
import pygame

VIEW_WIDTH = 640
VIEW_HEIGHT = 360
BACKGROUND_IMAGE = 'assets/backgrounds/back1.jpg'
BACKGROUND_WIDTH = pygame.image.load(BACKGROUND_IMAGE).convert().get_width()
BACKGROUND_HEIGHT = pygame.image.load(BACKGROUND_IMAGE).convert().get_height()

player_image = pygame.image.load('assets/sprites/up1.png')
player_rect = player_image.get_rect(midbottom=(VIEW_WIDTH // 2, VIEW_HEIGHT // 2))
protagonist_speed = 8

pygame.init()
pantalla = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
pygame.display.set_caption("Arcade")

# Control de FPS
clock = pygame.time.Clock()
fps = 30

# Control de l'animació del personatge
# 1 up. 2 down. 3 right. 4 left
sprite_direction  = "up"
sprite_index = 0
animation_protagonist_speed = 300
sprite_frame_number = 3
last_change_frame_time = 0
idle = False

def imprimir_pantalla_fons(image):
    # Imprimeixo imatge de fons:
    background = pygame.image.load(image).convert()
    pantalla.blit(background, (0, 0))

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
        player_rect.y -= protagonist_speed
    if keys[K_DOWN]:
        idle = False
        sprite_direction = "down"
        player_rect.y += protagonist_speed
    if keys[K_RIGHT]:
        idle = False
        sprite_direction = "right"
        player_rect.x += protagonist_speed
    if keys[K_LEFT]:
        idle = False
        sprite_direction = "left"
        player_rect.x -= protagonist_speed

    # Mantenir al jugador dins de la pantalla

    imprimir_pantalla_fons(BACKGROUND_IMAGE)
    # frame number: (there are 3 frames only)
    if not idle:
        if current_time - last_change_frame_time >= animation_protagonist_speed:
            last_change_frame_time = current_time
            sprite_index = sprite_index + 1
            sprite_index = sprite_index % sprite_frame_number
    else:
        sprite_index = 0
    player_image = pygame.image.load('assets/sprites/'+sprite_direction+str(sprite_index)+'.png')
    # player_image = pygame.transform.scale(player_image,(64,64))
    pantalla.blit(player_image, player_rect)
    player_rect.clamp_ip(pantalla.get_rect())

    # pantalla.blit(player_image, player_rect)
    pygame.display.update()
    clock.tick(fps)