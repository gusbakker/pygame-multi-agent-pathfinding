import pygame

WHITE = (255, 255, 255)
PATH = (170, 165, 170)
PATH_BORROW = (255, 255, 0)  # yellow
PATH_SEND_PATIENT = (200, 255, 200)  # green


class Tile2D:

    def __init__(self, row, col, tile_size, total_rows, tile_type):
        self.row = row
        self.col = col
        self.x = row * tile_size
        self.y = col * tile_size
        self.tile_type = tile_type
        self.color = WHITE
        self.neighbors = []
        self.size = tile_size
        self.total_rows = total_rows

    def is_barrier(self):
        if self.tile_type == "tree" or self.tile_type == "house":
            return True
        return False

    def get_pos(self):
        return self.row, self.col

    def make_start(self):
        pass

    def make_closed(self):
        pass

    def make_open(self):
        pass

    def make_end(self):
        pass

    def make_path(self, path_type):
        if path_type == 'spot':
            self.color = PATH
        if path_type == 'borrow':
            self.color = PATH_BORROW
        if path_type == 'send_person':
            self.color = PATH_SEND_PATIENT

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

