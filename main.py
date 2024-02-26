from settings import *
from game import Game

class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.game = Game()

    def run(self):
        while True:
            self.game.run()
            self.game.event_loop()

            pygame.display.update()
            self.clock.tick(fps)


if __name__ == "__main__":
    main = Main()
    main.run()
