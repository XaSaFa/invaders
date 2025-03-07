import pygame, sys
from pygame.locals import *
import random
import enemics

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
TEAL = (0,128,128)
TEAL2 = (0,170,170)
AMPLADA = 800
ALCADA = 600

# PUNTS jugador
punts = 0

pygame.init()
pygame.display.set_caption("Arcade")
pantalla = pygame.display.set_mode((AMPLADA,ALCADA))

# Velocitat de moviment de la nau
velocitat_nau = 8

# carrego les imatges
nave = pygame.image.load('assets/nave.png')
ufo = pygame.image.load('assets/ufo.png')

#calculem la posició inicial de la nau a la pantalla
posicio_inicial_x = AMPLADA/2 - nave.get_rect().width / 2
posicio_inicial_y = 450

#variables que serveixen per moure la nau
player_rect = nave.get_rect()
player_rect.x = posicio_inicial_x
player_rect.y = posicio_inicial_y

# llista de onades
onades = []
onada1 =[[1, 1, 1, 1, 1, 1], [1, 1, 1]]
onades.append(onada1)

# Llista de ufos
onada = onades.pop()
print(onada)
llista_ufos = []
for i in onada:
    print(i)
    comptador = 0
    for j in i:
        enemic = enemics.enemy(j)
        ufo_rect = enemic.rectangle
        print(ufo_rect)
        ufo_rect.x = comptador * 100
        ufo_rect.y = 10
        llista_ufos.append(ufo_rect)
        comptador += 1


direccio_ufos = 1
velocitat_ufos = 4

ufos_down = False

# Funció per Dibuixar els ufos
def controla_ufos():
    global direccio_ufos
    global ufos_down
    if ufos_down:
        direccio_ufos *= -1
        baixar_ufos()
        ufos_down = False
    for enemic in llista_ufos:
        pantalla.blit(ufo,(enemic.x,enemic.y))
        enemic.x += velocitat_ufos * direccio_ufos
        if enemic.x + enemic.width > AMPLADA or enemic.x < 0:
            ufos_down = True


# Bala rectangular blanca:
bala_imatge = pygame.Surface((4,10)) #definim una superficie rectangle de 4 pixels d'ample i 10 d'alçada
bala_imatge.fill(WHITE) #pintem la superficie de color blanc
bales_jugador1 = [] #llista on guardem les bales del jugador 1
velocitat_bales = 8
temps_entre_bales = 1000 #1 segon
temps_ultima_bala_jugador1 = 0 #per contar el temps que ha passat des de que ha disparat el jugador 1


# Funció que fa baixar tots els UFOS
def baixar_ufos():
    for enemic in llista_ufos:
        enemic.y += 30

# Control de FPS
clock = pygame.time.Clock()
fps = 30

# Variables per controla moviment d'estrelles
llista_estrelles1 = []
llista_estrelles2 = []
maxim_estrelles = 150

# Funció que genera estrelles
def genera_estrella(llista):
    genera = random.randint(1,10)
    if genera == 10:
        tamany_estrella = random.randint(1,4)
        posicio_x = random.randint(0,AMPLADA)
        rect1 = pygame.Rect(posicio_x,0,tamany_estrella,tamany_estrella)
        if llista == 1:
            llista_estrelles1.append(rect1)
        else:
            llista_estrelles2.append(rect1)
def controla_estrelles():
    if len(llista_estrelles1)+2 < maxim_estrelles:
        genera_estrella(1)
        genera_estrella(1)
        genera_estrella(1)
    for estrella in llista_estrelles1:
        pygame.draw.rect(pantalla, BLUE, estrella)
        estrella.y += 2
        if estrella.y > ALCADA:
            llista_estrelles1.remove(estrella)
    if len(llista_estrelles2)+2 < maxim_estrelles:
        genera_estrella(2)
        genera_estrella(2)
        genera_estrella(2)
    for estrella in llista_estrelles2:
        pygame.draw.rect(pantalla, YELLOW, estrella)
        estrella.y += 3
        if estrella.y > ALCADA:
            llista_estrelles2.remove(estrella)


def colisio_bala_ufo(bala1,ufo1):
    global punts
    bales_jugador1.remove(bala1)  # eliminem la bala
    llista_ufos.remove(ufo1) # eliminem l'ufo
    punts += 100
    # mostrem una explosió
    # eliminem el jugador 1 (un temps)
    # anotem punts al jugador 1

def controlar_bales():
    for bala in bales_jugador1:  # bucle que recorre totes les bales
        bala.y -= velocitat_bales  # mou la bala
        if bala.bottom < 0 or bala.top > ALCADA:  # comprova que no ha sortit de la pantalla
            bales_jugador1.remove(bala)  # si ha sortit elimina la bala
        else:
            pantalla.blit(bala_imatge, bala)  # si no ha sortit la dibuixa
        # Detectar col·lisions UFOS:
        for i in llista_ufos:
            if i.colliderect(bala):  # si un ufo toca una bala
                colisio_bala_ufo(bala,i)

# Definim la font per al panell de punts:
font = pygame.font.SysFont(None, 50)
def dibuixar_panell_punts():
    pygame.draw.rect(pantalla, TEAL2, (10, 520, 780, 70))
    pygame.draw.rect(pantalla, TEAL, (20, 530, 760, 50))
    display_punts = "Punts: " + str(punts)
    img = font.render(display_punts, True, WHITE)
    pantalla.blit(img,(30,540))

while True: # main game loop
    #contador
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # controlar trets de les naus
        if event.type == KEYDOWN:
            # jugador 1
            if event.key == K_SPACE and current_time - temps_ultima_bala_jugador1 >= temps_entre_bales:
                bales_jugador1.append(pygame.Rect(player_rect.centerx - 2, player_rect.top, 4, 10))
                temps_ultima_bala_jugador1 = current_time

    # Moviment de la nau prota
    keys = pygame.key.get_pressed()
    if keys[K_a]:
        player_rect.x -= velocitat_nau
    if keys[K_d]:
        player_rect.x += velocitat_nau
    #if keys[K_w]:
    #    player_rect.y -= velocitat_nau
    #if keys[K_s]:
    #    player_rect.y += velocitat_nau

    # Dibuixem el fons
    pantalla.fill(BLACK)
    controla_estrelles()
    # Mantenir la nau dins l'espai de joc
    player_rect.clamp_ip(pantalla.get_rect())
    # Dibuixem els ufos i controlem el seu moviment
    controla_ufos()
    # Dibuixem la nau
    pantalla.blit(nave, player_rect)
    # Actualitzar i dibuixar les bales del jugador 1:
    controlar_bales()
    dibuixar_panell_punts()
    pygame.display.update()
    clock.tick(fps)
