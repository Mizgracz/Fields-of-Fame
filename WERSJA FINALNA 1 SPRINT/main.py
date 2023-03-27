from graphics import Map
from gameplay import Camera, UpBar , Hourglass , Decision

import pygame
import sys

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.res = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.res)
        self.max_tps = 60.0
        self.map = Map(30, 30)
        self.map.texture()
        self.map.generate()
        self.camera = Camera(SCREEN_WIDTH,SCREEN_HEIGHT)
        self.up_bar = UpBar(self.screen)
        self.klepsydra1 = Hourglass(self.screen)
        self.dec = Decision(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

    def run(self):
        while True:
            self.handle_events()
            self.camera.mouse()
            self.camera.keybord()
            self.map.draw(self.screen, self.camera)
            self.up_bar.score()
            self.dec.draw()
            self.dec.click()
            self.klepsydra1.draw()
            self.klepsydra1.turn()
            pygame.display.flip()
            self.screen.fill((255, 255, 255))
            self.clock.tick(self.max_tps)


if __name__ == '__main__':
    game = Game()
    game.run()
