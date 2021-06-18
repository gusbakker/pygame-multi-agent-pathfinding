import random

from main.agents.AbstractAgent import AbstractAgent


class ReactiveAgent(AbstractAgent):

    def __init__(self, simulation, position, name):
        super().__init__(simulation, position, name)
        self.counter = random.randint(1, 10)
        self.possible_directions = ["up", "down", "left", "right"]
        self.direction = random.choice(self.possible_directions)

    def decide(self):
        pass
