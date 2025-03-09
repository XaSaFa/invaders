import pygame, sys, random
from pygame import *
from colors import *



class shoot():
    def __init__(self, sprites, lives,x1,y1,speed1):
        sprite_filename = "assets/" + sprites[0] + ".png"
        self.sprite = pygame.image.load(sprite_filename)
        self.x = x1
        self.y = y1
        self.speed = speed1
        self.rect = pygame.Rect(self.x, self.y, self.sprite.get_rect().width, self.sprite.get_rect().height)

    def draw(self,window1):
        window1.screen.blit(self.sprite,self.rect)

    def move_up(self, window1):
        self.x -= self.speed
        self.update_position()
        self.rect.clamp_ip(window1.screen.get_rect())
        if self.x < 0:
            self.x = 0

    def move_down(self, window1):
        self.x -= self.speed
        self.update_position()
        self.rect.clamp_ip(window1.screen.get_rect())
        if self.x < 0:
            self.x = 0

    def update_position(self):
        self.rect.x = self.x
        self.rect.y = self.y

class patrol_group():
    def __init__(self, army):
        self.units = army
        self.direction = 1
        self.bounce = False

    def move(self,window1):
        if self.bounce:
            self.direction *= -1
            self.bounce = False
            self.go_down()
        else:
            for i in self.units:
                i.x += i.speed * self.direction
                i.update_position()
                if i.x <= 0 or i.x + i.sprite.get_rect().width > window1.width:
                    self.bounce = True
        self.enemy_shoots()

    def draw(self,window1):
        for i in self.units:
            i.draw(window1)

    def go_down(self):
        for i in self.units:
            i.y += 20
            i.update_position()

    def check_casualties(self):
        p = 0
        for i in self.units:
            if i.lives <= 0:
                p += i.points
                self.units.remove(i)
        return p

    def enemy_shoots(self):
        for i in self.units:
            chance = random.randint(1,i.chance_to_shoot)
            if chance == 1:
                bullet1 = enemy_bullet(i.shoot_sprite, i.x + i.sprite.get_width() / 2,
                                 i.y, i.shoot_speed)
                i.shoots.append(bullet1)
                print("BOOM!")


class starship():
    def __init__(self, sprites, lives,x,y,speed,time_between_shoots,shoot_speed,points,chance_to_shoot):
        sprite_filename = "assets/" + sprites[0] + ".png"
        sprite_shoot_filename = "assets/" + sprites[1] + ".png"
        self.sprite = pygame.image.load(sprite_filename)
        self.lives = lives
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.sprite.get_rect().width, self.sprite.get_rect().height)
        self.shoot_sprite = pygame.image.load(sprite_shoot_filename)
        self.shoots = []
        self.time_between_shoots = time_between_shoots
        self.time_last_shoot = 0
        self.shoot_speed = shoot_speed
        self.points = points
        self.chance_to_shoot = chance_to_shoot

    def define_enemy(self, type_number,handicap,x,y):
        if type_number == 1:
            speed = 2 + handicap
            sprite_filename = "assets/ufo1.png"
            self.sprite = pygame.image.load(sprite_filename)
            s = starship(["ufo1", "ufo_weapon1"], 1, x-self.sprite.get_width()/2, y, speed, 5000, 4, 100,1000)
            return s

    def draw(self,window1):
        window1.screen.blit(self.sprite,self.rect)

    def move_left(self,window1):
        self.x -= self.speed
        self.update_position()
        self.rect.clamp_ip(window1.screen.get_rect())
        if self.x < 0:
            self.x = 0

    def move_right(self,window1):
        self.x += self.speed
        self.update_position()
        self.rect.clamp_ip(window1.screen.get_rect())
        if self.x + self.sprite.get_width() > window1.width:
            self.x = window1.width - self.sprite.get_width()

    def update_position(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def update_shoots(self):
        for i in self.shoots:
            if i.lives <= 0:
                self.shoots.remove(i)

class enemy_bullet():
    def __init__(self, sprite, x, y, speed):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x-4, self.y, self.sprite.get_rect().width, self.sprite.get_rect().height)
        self.lives = 1

    def draw(self,window1):
        window1.screen.blit(self.sprite,self.rect)

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def collisions(self,army):
        if army is not None:
            for i in army.units:
                if self.rect.colliderect(i.rect):
                    self.lives -= 1
                    i.lives -= 1

class bullet():
    def __init__(self, sprite, x, y, speed):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x-4, self.y, self.sprite.get_rect().width, self.sprite.get_rect().height)
        self.lives = 1

    def draw(self,window1):
        window1.screen.blit(self.sprite,self.rect)

    def move(self):
        self.y -= self.speed
        self.rect.y = self.y

    def collisions(self,army):
        if army is not None:
            for i in army.units:
                if self.rect.colliderect(i.rect):
                    self.lives -= 1
                    i.lives -= 1






class text_display():
    def __init__(self, window, game, color_front, color_back):
        self.window = window
        self.game = game
        self.color_front = color_front
        self.color_back = color_back

    def draw(self):
        pygame.draw.rect(self.window.screen, self.color_back, (10, 520, 780, 70))
        pygame.draw.rect(self.window.screen, self.color_front, (20, 530, 760, 50))
        display_points = "Points: " + str(self.game.points)
        display_wave = "Wave: " + str(self.game.wave)
        font = pygame.font.SysFont(None, 50)
        img1 = font.render(display_points, True, WHITE)
        img2 = font.render(display_wave, True, WHITE)
        self.window.screen.blit(img1, (30, 540))
        self.window.screen.blit(img2, (600, 540))

class announce():
    def __init__(self, window1, color_front, alpha):
        self.transparent_section = pygame.Surface((600, 400), pygame.SRCALPHA)
        self.color = color_front
        self.alpha = alpha
        self.window = window1


    def draw_text(self,lines, justify):
        pygame.draw.rect(self.transparent_section, (self.color[0],self.color[1],self.color[2],self.alpha), (0, 0, 600, 400))
        self.window.screen.blit(self.transparent_section,(100,60))
        lines_quantity = len(lines)
        font = pygame.font.SysFont(None, 50)
        count = 0
        min_x = self.window.width
        images = []
        if justify:
            for i in lines:
                img1 = font.render(i, True, BLACK)
                x = self.window.width / 2 - img1.get_width() / 2
                if x < min_x:
                    min_x = x
        for i in lines:
            img1 = font.render(i, True, BLACK)
            x = self.window.width / 2 - img1.get_width() / 2
            if justify:
                x = min_x
            y = (self.window.height / 2 - img1.get_height() / 2) - 30 * lines_quantity + count * 60
            count += 1
            self.window.screen.blit(img1, (x, y))




        else:
            for i in images:
                self.window.screen.blit(i, (i.get_rect().x, i.get_rect().y))





class game():
    def __init__(self, player1,fps, window1):
        self.points = 0
        self.wave = 0
        self.player = player1
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.army = None
        # self.waves =  [[[1,1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1,1]],[[1,1,1],[1,1],[1]]]
        self.waves = [[[1,1,1,1,1,1,1,1,1,1], [1,1,1,1,1,1,1,1],[1,1,1,1,1,1], [1,1,1,1]], [[1, 1, 1], [1, 1], [1]]]
        self.window = window1
        self.announce = announce(self.window, TEAL, 200)
        self.showing_menu = True
        self.pause = False
        self.restart = False

    def control_input_player(self):
        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            self.player.move_left(self.window)
        if keys[K_d] or keys[K_RIGHT]:
            self.player.move_right(self.window)

    def control_inputs(self, event1):
        if event1.type == KEYDOWN:
            current_time = pygame.time.get_ticks()
            if self.showing_menu:
                if event1.key == K_1:
                    self.showing_menu = False
                if event1.key == K_3:
                    pygame.quit()
                    sys.exit()
            else:
                if self.restart:
                    self.points = 0
                    self.wave = 0
                    self.showing_menu = True
                    self.pause = False
                    self.restart = False
                elif self.pause:
                    self.pause = False
                elif event1.key == K_SPACE and current_time - self.player.time_last_shoot >= self.player.time_between_shoots and self.army is not None:
                    bullet1 = bullet(self.player.shoot_sprite, self.player.x + self.player.sprite.get_width() / 2,
                                     self.player.y, self.player.shoot_speed)
                    self.player.shoots.append(bullet1)
                    self.player.time_last_shoot = current_time

    def get_new_wave(self):
        try:

            new_wave = self.waves[self.wave]
            self.wave += 1
            rows = 0
            x = 0
            y = 0
            army1 = []
            for i in new_wave:
                columns = 0
                for j in i:
                    ships_quantity = len(i)

                    if ships_quantity == 1:
                        x = self.window.width / 2
                    elif ships_quantity == 2:
                        x = abs(columns * self.window.width - self.window.width / 4)
                    elif ships_quantity == 3:
                        x = columns * 340 + 60
                    elif ships_quantity == 4:
                        x = columns * 226 + 60
                    elif ships_quantity == 5:
                        x = columns * 170 + 60
                    elif ships_quantity == 6:
                        x = columns * 136 + 60
                    elif ships_quantity == 7:
                        x = columns * 120 + 60
                    elif ships_quantity == 8:
                        x = columns * 97 + 60
                    elif ships_quantity == 9:
                        x = columns * 85 + 60
                    elif ships_quantity == 10:
                        x = columns * 75 + 60

                    y = 10 + rows * 66
                    enemy1 = starship.define_enemy(self, int(j), self.wave - 2,x,y)
                    army1.append(enemy1)
                    columns += 1
                rows += 1
            patrol = patrol_group(army1)
            self.army = patrol
        except:
            self.restart = True
            self.pause = True
            self.announce.draw_text(["YOU ACHIEVED", "VICTORY", "CONGRATULATIONS!"], False)


    def update_game(self):
        if self.showing_menu:
            self.show_menu()
            self.pause = True
        else:
            if self.army is not None:
                if len(self.army.units) == 0:
                    self.pause = True
                    self.get_new_wave()
            elif self.pause:
                self.announce.draw_text(["STARTING", "WAVE "+ str(self.wave), "GET READY!"], False)
            else:
                if self.army is None:
                    self.get_new_wave()
        self.player.draw(self.window)
        if self.army is not None:
            self.army.draw(self.window)
            self.army.move(self.window)
            for a in self.army.units:
                for b in a.shoots:
                    b.draw(self.window)
                    b.move()
        for i in self.player.shoots:
            i.draw(self.window)
            i.move()
            i.collisions(self.army)
        self.player.update_shoots()
        if self.army is not None:
            self.points += self.army.check_casualties()

    def show_menu(self):
        self.announce.draw_text(["1.- Play", "2.- Credits", "3.- Exit to DOS"], True)



class stars():
    def __init__(self, color_speed, window1):
        self.star_list = []
        for i in color_speed:
            star_color = i[0]
            star_speed = i[1]
            sf = star_field(star_color, star_speed, window1)
            self.star_list.append(sf)

    def update_stars(self):
        for i in self.star_list:
            i.control_stars()

class star_field():
    def __init__(self, star_color, star_speed, window1):
        self.star_color = star_color
        self.speed = star_speed
        self.max_stars = 150
        self.stars = []
        self.window = window1
        for i in range(50):
            star_y = random.randint(0, self.window.height)
            self.new_star(star_y,100)

    def new_star(self, y, odds):
        chance = random.randint(1, 100)
        if chance <= odds:
            star_size = random.randint(1, 4)
            star_x = random.randint(0, self.window.width)
            star_y = y
            rect1 = pygame.Rect(star_x, star_y, star_size, star_size)
            self.stars.append(rect1)

    def control_stars(self):
        if len(self.stars) + 2 < self.max_stars:
            self.new_star(0,10)
            self.new_star(0,10)
            self.new_star(0,10)
        for s in self.stars:
            pygame.draw.rect(self.window.screen, self.star_color, s)
            s.y += self.speed
            if s.y > self.window.height:
                self.stars.remove(s)







class window():
    def __init__(self, w1, h1, caption):
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((w1, h1))
        self.width = w1
        self.height = h1

    def clean_screen(self):
        self.screen.fill(BLACK)
