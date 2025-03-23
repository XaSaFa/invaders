
import pygame, sys
from pygame import *
from colors import *
from time import sleep

# Class character is a character of the game
class Character:
    def __init__(self, lives, x, y, speed):
        self.animations = []
        self.animation_index = 0
        self.lives = lives
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(0,0,0,0)
        self.direction = 0

    # Sets a new animation speed for the character
    def set_animation_speed(self,new_speed):
        self.animations[self.animation_index].frame_time = new_speed

    # draw the character in the screen
    def draw(self):
        screen.blit(self.animations[self.animation_index].get_frame(), (self.x, self.y))

    # moves to the left
    def move_left(self):
        self.x -= self.speed
        self.rect.x = self.x
        self.rect.clamp_ip(screen.get_rect())
        if self.x < 0:
            self.x = 0

    # moves to the right
    def move_right(self):
        self.x += self.speed
        self.rect.x = self.x
        self.rect.clamp_ip(screen.get_rect())
        if self.x + self.rect.width > screen.get_width():
            self.x = screen.get_width() - self.rect.width

    # moves up
    def move_up(self):
        self.y -= self.speed
        self.rect.y = self.y
        self.rect.clamp_ip(screen.get_rect())
        if self.y < 0:
            self.y = 0

    # moves down
    def move_down(self):
        self.y += self.speed
        self.rect.y = self.y
        self.rect.clamp_ip(screen.get_rect())
        if self.y + self.rect.height > screen.get_height():
            self.y = screen.get_height() - self.rect.height

    # Adds an animation to the list.
    def add_animation(self,image,start_frame,end_frame,frame_time,width,height,loops):
        self.animations.append(Animation(image,width,height,start_frame, end_frame,frame_time,loops))
        self.set_animation(0)

    # set the actual animation from the list and inits it
    def set_animation(self, animation_number):
        self.animation_index = animation_number
        self.animations[self.animation_index].frame = 0
        self.animations[self.animation_index].actual_loop = 0
        self.rect = pygame.Rect(self.x, self.y, self.animations[self.animation_index].width, self.animations[self.animation_index].height)

    # gets the frame to be shown
    def get_frame(self):
        self.animations[self.animation_index].get_frame()




# Return the frame to show of a character in a given moment.
class Animation:
    def __init__(self,image, width, height, start_frame, end_frame, frame_time, loops):
        self.sprite_sheet_image = pygame.image.load(image).convert_alpha()
        self.width = width
        self.height = height
        self.frame_time = frame_time
        self.last_update = 0
        self.frame = 0
        self.number_of_frames = end_frame-start_frame
        self.frames = []
        self.loops = loops
        self.actual_loop = 0
        for x in range(self.number_of_frames):
            self.frames.append(self.set_frames(start_frame+x))

    # gets the frames from the image and appends them to self.frames list field.
    def set_frames(self,frame_number):
        image = pygame.Surface((self.width,self.height)).convert_alpha()
        image.blit(self.sprite_sheet_image,(0,0),(frame_number * self.width,0, self.width,self.height))
        image.set_colorkey(TRANSPARENT_COLOR)
        return image

    # returns the actual frame of the animation
    def get_frame(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.frame_time:
            if not (self.loops > 0 and self.loops == self.actual_loop):
                if self.frame == self.number_of_frames-1:
                        self.actual_loop += 1
                        self.frame = 0
                else:
                    self.frame += 1
                self.last_update = current_time
        return self.frames[self.frame]

class Game():
    def __init__(self, fps):
        self.fps = fps
        self.state = 1 #1- menu, 2- credits, 3- game, 4- game over...

    def draw_screen(self):
        if self.state == 1:
            self.show_menu()
        elif self.state == 2:
            pass
        elif self.state == 3:
            screen.blit(pygame.image.load("assets/background.png"),(0,0))
            ufo.draw()
        elif self.state == 4:
            pass

    # Controla l'entrada de teclat a cada stat del joc
    def control_inputs(self):


        # 1- menu
        if self.state == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        self.state = 3
                    elif event.key == K_3:
                        pygame.display.toggle_fullscreen()
                    elif event.key == K_4:
                        pygame.quit()
                        sys.exit()
        # 3- game
        elif self.state == 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            keys = pygame.key.get_pressed()

            if keys[K_LEFT]:
                ufo.move_left()
            if keys[K_RIGHT]:
                ufo.move_right()
            if keys[K_UP]:
                ufo.move_up()
            if keys[K_DOWN]:
                ufo.move_down()

    # showa the menu on the screen
    def show_menu(self):
        font1 = pygame.font.SysFont(None, 150)
        font2 = pygame.font.SysFont(None, 70)
        img1 = font1.render("UFO Attack!", True, MAGENTA)
        img2 = font2.render("1 to play", True, GREEN)
        img3 = font2.render("2 to show Credits", True, GREEN)
        img4 = font2.render("3 toggle Window/Fullscreen", True, GREEN)
        img5 = font2.render("4 to exit", True, RED)
        screen.blit(img1, (100, 50))
        screen.blit(img2, (100, 200))
        screen.blit(img3, (100, 280))
        screen.blit(img4, (100, 360))
        screen.blit(img5, (100, 440))



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (50,50,50)
TRANSPARENT_COLOR = (170,0,170)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("UFO Attack!")

# Characters
ufo = Character(1,0,0,5)
ufo.add_animation("assets/ufo_idle.png",0,9,150,64,64, 0)

# Game
game = Game(60)


clock = pygame.time.Clock()
while True:
    current_time = pygame.time.get_ticks()
    screen.fill(BACKGROUND_COLOR)


    game.draw_screen()
    game.control_inputs()



    pygame.display.update()
    clock.tick(game.fps)


