from __future__ import annotations
import pygame


class Entity:

    ID = 0

    def __init__(self, simulation, position, name):
        self.name = name
        self.id = Entity.ID = Entity.ID + 1
        self.simulation = simulation
        self.position = position
        self.images_loaded = False
        self.image = None

    def get_width(self):
        return self.simulation.world.get_tile_size()

    def get_height(self):
        return self.simulation.world.get_tile_size()

    def update(self):
        pass

    def draw(self, screen):
        if self.image is not None:
            screen.blit(self.image, (self.position.x+1, self.position.y+1))
            # print(self.name, self.get_x(), self.get_y())
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.position.x, self.position.y, self.get_width(), self.get_height()))
        return self
