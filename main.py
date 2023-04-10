from graphics import Map
from gameplay import Camera, UpBar, Hourglass, Decision, Build_Menu, BuildItem, Timer, SideMenu
from menu import Menu
import pygame
import sys


# config
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
clock = pygame.time.Clock()
res = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(res)
max_tps = 60.0



# class game
class Game:
    def __init__(self):
        pygame.init()
        self.camera = Camera()
        self.map = Map(30, 30, screen, self.camera)
        self.map.texture()
        self.map.generate()
        self.up_bar = UpBar(screen)
        self.klepsydra1 = Hourglass(screen)
        self.dec = Decision(screen)
        self.bm = Build_Menu(screen)
        self.timer = Timer(res, screen, screen)
        self.startmenu = Menu(screen, clock, max_tps)
        self.sd = SideMenu(screen)

        self.allItem = [   # Budynki
            BuildItem(self.bm.item_menu_surf, 50, 'wieza', 'Wieża strażniczą (+10 wojska na turę)', 10, 0),
            BuildItem(self.bm.item_menu_surf, 50, 'tartak', 'Farma (+ 10 złota na ture)', 0, 10)]


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        press = pygame.key.get_pressed()

        if press[pygame.K_b]:
            self.bm.build_stauts = True





    def run(self):
        while True:
            screen.fill((255, 255, 255))
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

            clock.tick(max_tps)



# wykonywanie

start_menu = Menu(screen, clock, max_tps,)  # wyświetlanie i obsługa menu


# if start_menu.gameplay:    # obsługa gry
#     if __name__ == '__main__':
game = Game()
game.run()
