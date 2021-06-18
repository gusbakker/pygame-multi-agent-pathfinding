import random
from math import sqrt
import pygame

from main.entities.Car import Car
from main.world.Tile2D import Tile2D

# colors
BLACK = (30, 30, 30)
WHITE = (250, 250, 250)
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (int(x), int(y))
    surf.blit(text_surface, text_rect)


def distance_between(a, b):
    return sqrt(((a.x - b.x) ** 2 + (a.y - b.y) ** 2))


class GridWorld:

    TILE_SIZE = 20

    def __init__(self):

        self.world = []
        self.grid = []
        self.read_file()
        self.create_grid()
        self.screen = pygame.display.set_mode((self.get_world_width(), self.get_world_height() + 50))
        self.tree = pygame.transform.scale(pygame.image.load("images/tree.png"),
                                           (self.TILE_SIZE - 1, self.TILE_SIZE - 1))
        self.house = pygame.transform.scale(pygame.image.load("images/house.png"),
                                            (self.TILE_SIZE - 1, self.TILE_SIZE - 1))

    def read_file(self):
        map_file = open("maps/map1.txt", "r")
        for line in map_file:
            integer_map = map(int, line.split())
            self.world.append(list(integer_map))

        map_file.close()

    def get_tile_size(self):
        return self.TILE_SIZE

    def get_world_width(self):
        return self.TILE_SIZE * len(self.world[0])

    def get_world_height(self):
        return self.TILE_SIZE * len(self.world[1])

    def create_grid(self):
        for x in range(len(self.world[0])):
            self.grid.append([])
            for y in range(len(self.world[1])):
                if self.world[x][y] == 0:
                    tile = Tile2D(x, y, self.TILE_SIZE, len(self.world[0]), "empty")
                elif self.world[x][y] == 1:
                    tile = Tile2D(x, y, self.TILE_SIZE, len(self.world[0]), "tree")
                elif self.world[x][y] == 2:
                    tile = Tile2D(x, y, self.TILE_SIZE, len(self.world[0]), "house")
                self.grid[x].append(tile)

    def draw(self, simulation, entities):

        self.screen.fill((0, 0, 0))

        # draw default white squares
        for row in self.grid:
            for tile in row:
                tile.draw(self.screen)

        # draw pathfinding
        for entity in entities:
            if isinstance(entity, Car):
                for tile in entity.path:
                    tile.draw(self.screen)

        # draw moving objects
        for entity in entities:
            entity.draw(self.screen)

        # draw world grid
        for x in range(0, self.get_world_width(), self.TILE_SIZE):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, self.get_world_height()))
        for y in range(0, self.get_world_height(), self.TILE_SIZE):
            pygame.draw.line(self.screen, BLACK, (0, y), (self.get_world_width(), y))

        # draw world objects
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid[0])):
                if self.grid[x][y].tile_type == "tree":
                    self.screen.blit(self.tree, (x * self.TILE_SIZE + 1, y * self.TILE_SIZE + 1))
                if self.grid[x][y].tile_type == "house":
                    self.screen.blit(self.house, (x * self.TILE_SIZE + 1, y * self.TILE_SIZE + 1))

        # draw moving objects
        for entity in entities:
            entity.draw(self.screen)

        # draw panel information text
        s = 'People: ' + str(len(simulation.houses[0].persons))
        draw_text(self.screen, s, 20, 100, self.get_world_height())
        s = 'Deliveries: ' + str(simulation.persons_solved)
        draw_text(self.screen, s, 20, 350, self.get_world_height())
        s = 'Cars: ' + str(len(simulation.cars))
        draw_text(self.screen, s, 20, 600, self.get_world_height())

    def get_random_empty_tile(self):
        empty_tiles = []
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid[0])):
                if not self.grid[x][y].is_barrier():
                    empty_tiles.append(self.grid[x][y])

        return random.choice(empty_tiles)

    def get_all_empty_pos(self):
        empty_pos = []
        for x, row in enumerate(self.grid):
            for y, pos in enumerate(row):
                if self.world[x][y] == 0:
                    empty_pos.append(self.grid[x][y])
        return empty_pos
