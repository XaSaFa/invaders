import pygame

class enemy():
    def __init__(self, type_number):
        self.ufo_name = "assets/ufo"+str(type_number)+".png"
        self.ufo = pygame.image.load(self.ufo_name)
        self.rectangle = self.ufo.get_rect()
