import pygame

from main.agents.ReactiveAgent import ReactiveAgent
from main.utils.Pathfinding import path_finding


class Car(ReactiveAgent):

    def __init__(self, simulation, position, name, house):
        super().__init__(simulation, position, name)
        self.load_image()
        self.home_house = house
        self.current_house = house
        self.spot = None
        self.path = []
        self.tile_counter = -1
        self.current_tile = None
        self.next_tile = None
        self.direction = 0
        self.person = None
        self.returning_home = False

    def load_image(self):
        img = pygame.image.load("images/taxi.png")
        self.image = pygame.transform.scale(img,
                                            (self.simulation.world.TILE_SIZE - 1, self.simulation.world.TILE_SIZE - 1))

    def update(self):
        # self.move()
        self.step_move()

    def assign_spot(self, spot):
        self.spot = spot

    def assign_house(self, house):
        self.current_house = house

    def step_move(self):
        if self.tile_counter >= 0:
            self.next_tile = self.path[self.tile_counter]
            self.tile_counter -= 1
            self.position.x = self.next_tile.x
            self.position.y = self.next_tile.y
            if self.tile_counter == 0:  # 0 means it arrived to destination
                if not self.returning_home:
                    self.pick_up()  # pick up people
                else:
                    self.deliver_person()  # deliver person to house

    def move(self):
        if self.tile_counter >= 0:
            if self.position.x == self.next_tile.x and self.position.y == self.next_tile.y:
                self.current_tile = self.next_tile
                self.tile_counter -= 1
                self.next_tile = self.path[self.tile_counter]
                self.set_direction()

            if self.direction == "down":
                self.position.y = self.position.y + 1
            elif self.direction == "up":
                self.position.y = self.position.y - 1
            elif self.direction == "left":
                self.position.x = self.position.x - 1
            elif self.direction == "right":
                self.position.x = self.position.x + 1

            if self.tile_counter == 0:  # if 0, it means it arrived to destination
                if not self.returning_home:
                    self.pick_up()  # pick up people
                else:
                    self.deliver_person()  # deliver person to house

    def set_direction(self):
        if self.next_tile.x > self.current_tile.x:
            self.direction = "right"
        if self.next_tile.x < self.current_tile.x:
            self.direction = "left"
        else:
            if self.next_tile.y > self.current_tile.y:
                self.direction = "down"
            if self.next_tile.y < self.current_tile.y:
                self.direction = "up"
                # self.image = pygame.transform.rotate(self.image, -90)

    def pick_up(self):
        if self.spot is None:
            origin = self.position
        else:
            origin = self.spot.position
            if self.spot.num_persons() > 0:
                self.person = self.spot.retrieve_person()
        self.returning_home = True
        self.calculate_route(origin, self.home_house.position, 'spot')

    def deliver_person(self):
        self.current_house.receive_person(self.person)
        self.spot = None
        self.person = None
        self.returning_home = False

    def calculate_route(self, origin, destiny, path_type):
        self.load_image()
        self.path = path_finding(self.simulation.world.grid, origin, destiny, path_type)
        self.tile_counter = len(self.path) - 1
        try:
            self.current_tile = self.path[self.tile_counter]
            self.next_tile = self.current_tile
        except:
            print("Exception when calculating route")
