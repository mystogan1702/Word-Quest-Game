from settings import *
from game import Game


class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.game = Game()

    def run(self):
        while True:

            self.game.run()

            self.clock.tick(fps)
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
