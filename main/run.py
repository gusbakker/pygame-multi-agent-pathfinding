import sys
import pygame

sys.path.append('./')
from main.world.Simulation import Simulation


def start():
    # Create world
    pygame.init()
    pygame.display.set_caption("Pygame Pathfinding")
    simulation = Simulation()
    # Run
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        simulation.update()
        pygame.display.update()
        pygame.time.wait(1)


if __name__ == "__main__":
    start()
