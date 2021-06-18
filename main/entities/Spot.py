import pygame
from main.entities.Person import Person
from main.entities.Entity import Entity


class Spot(Entity):

    def __init__(self, simulation, position, name, required_cars, urgency, type):
        super().__init__(simulation, position, name)
        self.required_cars = required_cars
        self.solved = False
        self.load_image()
        self.urgency = urgency
        self.type = type
        self.persons = [Person() for x in range(1, required_cars + 1)]

    def load_image(self):
        if self.solved:
            image = pygame.image.load("images/spot_solved.png")
        else:
            image = pygame.image.load("images/spot.png")
        self.image = pygame.transform.scale(image,
                                            (self.simulation.world.TILE_SIZE - 1, self.simulation.world.TILE_SIZE - 1))

    def set_solved(self):
        self.solved = True
        self.load_image()

    def update(self):
        if self.num_persons == 0:
            self.image = None

    def num_persons(self):
        return len(self.persons)

    def retrieve_person(self):
        return self.persons.pop()
