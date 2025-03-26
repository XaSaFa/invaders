import pygame, sys, random, csv
from pygame import *
from colors import *
from time import sleep

ROWS = 9
MAX_COLS = 12
TILE_SIZE = 64

# gets the army from the level editor csv
class Army:
    def __init__(self, level):
        self.units = []
        self.world_data = []
        for row in range(ROWS):
            r = [-1] * MAX_COLS
            self.world_data.append(r)
        with open(f'assets/levels/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for y, row in enumerate(reader):
                for x, tile in enumerate(row):
                    if int(tile) >= 0:
                        ufo1 = Character(1, 16 +  x * TILE_SIZE, y * TILE_SIZE, 2)
                        ufo1.add_animation("assets/enemies/ufo_idle.png", 0, 9, 150, 64, 64, 0)
                        self.units.append(ufo1)

    def draw(self):
        for i in self.units:
            i.draw()


class Patrol(Army):
    def __init__(self, level):
        super().__init__(level)
        self.direction = 1
        self.bounce = False
        self.shoots = []

    def move(self):
        if self.bounce:
            self.direction *= -1
            self.bounce = False
            self.go_down()
        else:
            for i in self.units:
                i.x += i.speed * self.direction
                i.rect.x = i.x
                if i.x <= 0 or i.x + i.rect.width > screen.get_width():
                    self.bounce = True

    def go_down(self):
        for i in self.units:
            i.y += 20
            i.rect.y = i.y

    def update(self):
        self.move()
        self.draw()

# Class character is a character of the game
class Character:
    def __init__(self, lives, x, y, speed):
        self.animations = []
        self.animation_index = 0
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.direction = 0
        self.lives = lives
        self.x = x
        self.y = y
        self.speed = speed

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
    def add_animation(self,image1,start_frame,end_frame,frame_time,width,height,loops):
        self.animations.append(Animation(image1,width,height,start_frame, end_frame,frame_time,loops))
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



# Class for the protagonist of the game, inherits from Character Class
class Protagonist(Character):
    firing_rate = 0
    shoot_speed = 0
    last_shoot = 0
    bullets = []

    # fields needed for the class
    def set_stats(self, firing_rate, shoot_speed):
        self.firing_rate = firing_rate
        self.shoot_speed = shoot_speed
    # move instantly to one position
    def move(self,x,y):
        self.x = x
        self.y = y
    # creates a bullet
    def shoot(self):
        if self.weapon_is_ready():
            b1 = Bullet("assets/protagonist/bullet1.png",self.x + self.rect.width / 2, self.y, self.shoot_speed,1)
            self.bullets.append(b1)
            self.last_shoot = current_time
    # draw the protagonist and all the bullets
    def update(self):
        self.draw()
        for i in self.bullets:
            i.move()
            i.draw()
    # return True if the weapon is ready to fire
    def weapon_is_ready(self):
        return current_time - self.last_shoot >= self.firing_rate

    def init_game(self):
        starship.add_animation("assets/protagonist/starship_idle.png", 0, 4, 200, 50, 68, 0)
        starship.set_stats(300, 6)
        starship.move(368, 530)

# Return the frame to show of a character in a given moment.
class Animation:
    def __init__(self,image1, width, height, start_frame, end_frame, frame_time, loops):
        self.sprite_sheet_image = pygame.image.load(image1).convert_alpha()
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


def show_menu():
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

# Shows the control panel below the game screen
class ControlPanel:
    def __init__(self, color_front, color_back, lives, firing_rate):
        self.color_front = color_front
        self.color_back = color_back
        self.energy_rectangle = EnergyBar(662,662,130,20,lives)
        self.shoot_rectangle = ShootBar(388,662,130,20,firing_rate)

    def draw(self, points, level, lives,last_shoot):
        # pygame.draw.rect(big_screen, self.color_back, (10, 640, 780, 70))
        # pygame.draw.rect(big_screen, self.color_front, (20, 650, 760, 50))
        font1 = pygame.font.SysFont(None, 36)
        img1 = font1.render("Points: " + str(points), True, WHITE)
        img2 = font1.render("Level: " + str(level), True, WHITE)
        img3 = font1.render("Integrity:", True, WHITE)
        img4 = font1.render("Shoot:", True, WHITE)
        big_screen.blit(img2, (30, 650))
        big_screen.blit(img1, (30, 675))
        big_screen.blit(img3, (550, 660))
        big_screen.blit(img4, (300, 660))
        self.energy_rectangle.update_bar(lives)
        self.shoot_rectangle.update_bar(last_shoot)
        pygame.draw.rect(big_screen, self.energy_rectangle.color, self.energy_rectangle.rect)
        pygame.draw.rect(big_screen, self.energy_rectangle.color, self.shoot_rectangle.rect)
        self.energy_rectangle.generate_lines(BLACK)

class Game:
    def __init__(self, fps, protagonist):
        self.fps = fps
        self.state = 1 #1- menu, 2- credits, 3- game, 4- game over...
        self.background = "stars" # default stars background
        self.star_background = Stars([[TEAL, 2], [GREEN, 3], [BLUE, 1]])
        self.points = 0
        self.level = 0
        self.protagonist = protagonist
        self.control_panel = ControlPanel(TEAL, TEAL2, self.protagonist.lives, self.protagonist.firing_rate)
        self.enemies = Army(self.level)
        self.patrol = Patrol(self.level)


    # draw elements to the screen
    def draw_screen(self):
        if self.state == 1: # menu
            show_menu()
        elif self.state == 2:
            pass
        elif self.state == 3: # game

            screen.fill(BACKGROUND_COLOR)
            if self.background == "stars":
                self.star_background.update_stars()
            else:
                screen.blit(pygame.image.load(self.background),(0,0))
            self.patrol.update()
            self.protagonist.update()
            self.control_panel.draw(self.points, self.level, self.protagonist.lives, self.protagonist.last_shoot)
        elif self.state == 4:
            pass

    # Sets the image to show in a phase, if stars then show moving stars
    def set_background(self, bg_image):
        self.background = bg_image

    # Controla l'entrada de teclat a cada stat del joc
    def control_inputs(self):
        # 1- menu
        if self.state == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_1: # play
                        self.state = 3
                    if event.key == K_2: # credits
                        pass
                    elif event.key == K_3: # togle fullscreen
                        pygame.display.toggle_fullscreen()
                    elif event.key == K_4: # exit
                        pygame.quit()
                        sys.exit()
        # 3- game
        elif self.state == 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.protagonist.shoot()

            keys = pygame.key.get_pressed()

            if keys[K_LEFT]:
                self.protagonist.move_left()
            if keys[K_RIGHT]:
                self.protagonist.move_right()
            # if keys[K_UP]:
            #     self.protagonist.move_up()
            # if keys[K_DOWN]:
            #     self.protagonist.move_down()



# star and star_field classes serves to create a background of stars.
class Stars:
    def __init__(self, color_speed):
        self.star_list = []
        for i in color_speed:
            star_color = i[0]
            star_speed = i[1]
            sf = StarField(star_color, star_speed)
            self.star_list.append(sf)

    def update_stars(self):
        for i in self.star_list:
            i.control_stars()

class StarField:
    def __init__(self, star_color, star_speed):
        self.star_color = star_color
        self.speed = star_speed
        self.max_stars = 150
        self.stars = []
        for i in range(50):
            star_y = random.randint(0, screen.get_width())
            self.new_star(star_y,100)

    def new_star(self, y, odds):
        chance = random.randint(1, 100)
        if chance <= odds:
            star_size = random.randint(1, 4)
            star_x = random.randint(0, screen.get_width())
            star_y = y
            rect1 = pygame.Rect(star_x, star_y, star_size, star_size)
            self.stars.append(rect1)

    def control_stars(self):
        if len(self.stars) + 2 < self.max_stars:
            self.new_star(0,10)
            self.new_star(0,10)
            self.new_star(0,10)
        for s in self.stars:
            pygame.draw.rect(screen, self.star_color, s)
            s.y += self.speed
            if s.y > screen.get_height():
                self.stars.remove(s)

# Displays the energy (lives) of the main character
class EnergyBar:
    def __init__(self, x,y,width, height, lives):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = GREEN
        self.rect = pygame.Rect(x,y,width,height)
        self.initial_lives = lives
        self.bar_slice = self.width / self.initial_lives

    def generate_lines(self, color1):
        i = 7
        while i < self.width:
            rect1 = pygame.Rect(self.x+i, self.y, 5, self.height)
            pygame.draw.rect(big_screen, color1, rect1)
            i += 12

    def update_bar(self, lives):
        if lives == self.initial_lives:
            self.color = GREEN
        elif lives < self.initial_lives:
            self.color = YELLOW
            if lives <= self.initial_lives / 2:
                self.color = ORANGE
            if lives <= self.initial_lives / 3:
                self.color = RED
        self.width = lives * self.bar_slice
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

# This class is for the protagonist only
class Bullet:
    def __init__(self, image1, x, y, speed, damage):
        self.sprite = pygame.image.load(image1)
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x-8, self.y, self.sprite.get_rect().width, self.sprite.get_rect().height)
        self.lives = damage
        self.animation = Animation("assets/protagonist/bullet1.png",8,22,0,4,100,0)


    # Sets a new animation speed for the character
    def set_animation_speed(self, new_speed):
        self.animation.frame_time = new_speed

    def draw(self):
        screen.blit(self.animation.get_frame(), (self.x-4, self.y))

    def move(self):
        self.y -= self.speed
        self.rect.y = self.y

    # def collisions(self,army):
    #     if army is not None:
    #         for i in army.units:
    #             if self.rect.colliderect(i.rect):
    #                 self.lives -= 1
    #                 i.lives -= 1

# Displays the energy (lives) of the main character
class ShootBar:
    def __init__(self, x,y,width, height, firing_rate):
        self.width = width
        self.max_width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = MAGENTA
        self.rect = pygame.Rect(x,y,width,height)
        self.firing_rate = firing_rate

    def update_bar(self, last_shoot):

        if current_time - last_shoot >= self.firing_rate:
            self.width = self.max_width
        else:
            self.width = (current_time - last_shoot)/self.firing_rate*100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)






FULL_SCREEN_WIDTH = 1280
FULL_SCREEN_HEIGHT = 720
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BACKGROUND_COLOR = (0,0,0,)
TRANSPARENT_COLOR = (170,0,170)

pygame.init()

# screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen = pygame.Surface((800,600))
big_screen = pygame.display.set_mode((FULL_SCREEN_WIDTH,FULL_SCREEN_HEIGHT))
big_screen.blit(screen,(0,0))
pygame.display.set_caption("UFO Attack!")

# Characters
ufo = Character(1,0,0,5)
ufo.add_animation("assets/enemies/ufo_idle.png",0,9,150,64,64, 0)


starship = Protagonist(1,0,0,5)
starship.init_game()

# Game
game = Game(60,starship)


clock = pygame.time.Clock()
while True:
    current_time = pygame.time.get_ticks()
    big_screen.fill((10,10,10))
    big_screen.blit(screen,(10,10))

    game.draw_screen()
    game.control_inputs()



    pygame.display.update()
    clock.tick(game.fps)


