from main.entities.Entity import Entity


class AbstractAgent(Entity):

    def __init__(self, simulation, position, name):
        super().__init__(simulation, position, name)

    def decide(self):
        pass





