import sys
import pygame
from graphics import Map


class Game:
    def __init__(self):
        pygame.init()
        self.res = (1280, 720)
        self.screen = pygame.display.set_mode(self.res)
        self.screen.fill((255, 255, 255))
        self.z = 1
        map1 = Map(3, 2,self.screen)
        map1.generate()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = event.pos
                    for item in map1.sprites():
                        if item.is_point_inside_polygon((x,y)):
                            item.function(map1)
                    pass
            map1.draw()
            pygame.display.update()
gra = Game()

