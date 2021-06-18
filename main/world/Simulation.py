from __future__ import annotations
import copy
import random
from datetime import datetime, timedelta
from main.entities.Car import Car
from main.entities.House import House
from main.entities.Spot import Spot
from main.world.GridWorld import GridWorld, distance_between

NUM_HOUSES = 5
NUM_CARS_PER_HOUSE = 1


class Simulation:

    SPOT_TIME_STEP = timedelta(seconds=4.0)
    TIME_STEP = timedelta(seconds=0.1)

    def __init__(self):
        self.entities = []
        self.houses = []
        self.spots = []
        self.cars = []
        self.world = GridWorld()
        self.create_simulation()
        self.next_spot_time = datetime.now()
        self.next_step_time = datetime.now()
        self.current_step = 1
        # statistics
        self.persons_solved = 0
        self.spots_solved = 0

    def create_simulation(self):
        # Create houses
        for i in range(1, NUM_HOUSES + 1):
            place = self.get_random_empty_place()
            house = House(self, place, "house_" + str(i))
            self.houses.append(house)
            # Create cars for each house
            house_cars = []
            for j in range(1, NUM_CARS_PER_HOUSE + 1):
                place_copy = copy.deepcopy(place)
                car = Car(self, place_copy, "car_" + str(i) + "_" + str(j), house)
                house_cars.append(car)
                self.cars.append(car)
                self.add_entity(car)
            house.cars = house_cars
            self.add_entity(house)

    def add_entity(self, entity):
        if entity in self.entities:
            return self
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def update(self):
        # steps
        now = datetime.now()
        if now >= self.next_step_time:
            for house in self.houses:
                house.decide()
            for entity in self.entities:
                entity.update()
            self.check_if_spots_solved()
            self.next_step_time = now + self.TIME_STEP
            self.current_step += 1
        self.create_random_spot()
        # draws all world objects
        self.world.draw(self, self.entities)

    def check_if_spots_solved(self):
        for spot in self.spots:
            if spot.num_persons() <= 0:
                self.entities.remove(spot)
                self.spots.remove(spot)
                spot.set_solved()
                self.spots_solved += 1

    def get_random_empty_place(self):
        return self.world.get_random_empty_tile()

    def create_random_spot(self):
        now = datetime.now()
        if now >= self.next_spot_time:
            place = self.get_random_empty_place()
            urgency = random.choice(range(1, 3))
            spot_type = random.choice(range(1, 3))
            required_cars = random.choice(range(1, 5))
            spot = Spot(self, place, "Spot", required_cars, urgency, spot_type)
            self.add_entity(spot)
            self.spots.append(spot)
            self.next_spot_time = now + self.SPOT_TIME_STEP

    def distance_to_closest_house(self, pos):
        if len(self.houses) == 0:
            return 0
        dist = distance_between(pos, self.houses[0].position)
        for house in self.houses:
            new_dist = distance_between(pos, house.position)
            if new_dist < dist:
                dist = new_dist

        return dist
