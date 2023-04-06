from graphics import Map
from gameplay import Camera, UpBar, Hourglass, Decision, Build_Menu, BuildItem, Timer, SideMenu
from menu import Menu

import pygame
import sys

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Game:
    def __init__(self):
        pygame.init()
        self.status = False
        self.clock = pygame.time.Clock()
        self.res = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.res)
        self.max_tps = 60.0
        self.camera = Camera()
        self.map = Map(30, 30, self.screen, self.camera)
        self.map.texture()
        self.map.generate()
        self.up_bar = UpBar(self.screen)
        self.klepsydra1 = Hourglass(self.screen)
        self.dec = Decision(self.screen)
        self.bm = Build_Menu(self.screen)
        self.timer = Timer(self.res, self.screen, self.screen)
        self.startmenu = Menu(self.screen, self.clock, self.max_tps)
        self.sd = SideMenu(self.screen)
        self.allItem = [
            BuildItem(self.bm.item_menu_surf, 50, 'wieza', 'Wieża strażniczą (+10 wojska na turę)', 10, 0),
            BuildItem(self.bm.item_menu_surf, 50, 'tartak', 'Farma (+ 10 złota na ture)', 0, 10)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        press = pygame.key.get_pressed()

        if press[pygame.K_b]:
            self.bm.build_stauts = True

        if press[pygame.K_ESCAPE]:
            self.status = False
            self.startmenu.status = True

    def run(self):
        
        while True:
            while self.startmenu.status:
                choose = self.startmenu.run()
                
                if choose == 'new_game':
                    
                    self.startmenu.status = False
                    self.status = True
                elif choose == 'quit':
                    sys.exit(0)

            while self.status:
                self.screen.fill((255, 255, 255))
                self.handle_events()
                self.camera.mouse()
                self.camera.keybord()
                self.map.draw()
                self.up_bar.score()
                self.dec.draw()
                self.sd.draw()

                if self.bm.build_stauts:
                    self.bm.draw()
                    for item in self.allItem:
                        item.draw()
                        item.buy()
                if not self.bm.build_stauts:
                    self.dec.click()

                self.klepsydra1.draw()
                self.klepsydra1.turn()
                self.timer.update()
                pygame.display.flip()

                self.clock.tick(self.max_tps)


if __name__ == '__main__':
    game = Game()
    game.run()
