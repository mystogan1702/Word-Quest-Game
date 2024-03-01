from settings import *
from game import Game
from world import World

class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.world = World(world_data)


    def run(self):
        while True:

            self.game.run()
            self.game.event_loop()
            self.world.draw()

            pygame.display.update()
            self.clock.tick(fps)


if __name__ == "__main__":
    main = Main()
    main.run()
