import random
import pygame
from main.agents.ReactiveAgent import ReactiveAgent


class House(ReactiveAgent):

    MAX_CAPACITY = 10

    def __init__(self, simulation, position, name):
        super().__init__(simulation, position, name)
        self.load_image()
        self.house_action = None
        self.cars = []
        self.persons = []

    def load_image(self):
        image = pygame.image.load("images/home.png")
        self.image = pygame.transform.scale(image, (self.simulation.world.TILE_SIZE - 1,
                                                    self.simulation.world.TILE_SIZE - 1))

    def update(self):
        pass

    def decide(self):
        spots = self.simulation.spots
        available_cars = self.look_for_free_vehicles()
        if len(spots) > 0 and len(available_cars) > 0:
            car = available_cars[0]
            car.assign_spot(random.choice(spots))
            can_arrive_within_time = car.calculate_route(self.position, spots[0].position, 'spot')
            if not can_arrive_within_time:
                pass

    def receive_person(self, person):
        self.persons.append(person)

    def look_for_free_vehicles(self):
        free_cars = []
        for car in self.cars:
            if (car.spot is None) and (car.current_house == self):
                free_cars.append(car)
        return free_cars


