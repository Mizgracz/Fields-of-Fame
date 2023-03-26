import sys
import pygame
from graphics import Map
import time
from build import BuildMenu
from build import MenuItem



start_time = time.time()
seconds = 0
elapsed_time = 0




class Game:
    def __init__(self):
        pygame.init()
        self.res = (1280, 720)
        self.screen = pygame.display.set_mode(self.res)
        self.screen.fill((255, 255, 255))
        self.z = 1
        self.status = True
        #score
        self.scoregold = 0
        self.scorearmy = 0
        self.scorehex = 0
        #gui
        self.mainSurface = pygame.Surface(self.res,pygame.SRCALPHA)
        self.mainSurface.fill('#ffffff')
        self.up_bar = pygame.Surface((self.res[0],30),pygame.SRCALPHA)
        self.up_bar.fill('#0f0f0f')
        
        self.bm = BuildMenu(self.mainSurface)
        MenuItem(self.bm,'Opis1','tmp',50,10,0)
        MenuItem(self.bm,'Opis1','tmp2',50,10,0)
        MenuItem(self.bm,'Opis1','tmp3',50,10,0)
        MenuItem(self.bm,'Opis1','tmp',50,10,0)
        MenuItem(self.bm,'Opis1','tmp2',50,10,0)
        MenuItem(self.bm,'Opis1','tmp3',50,10,0)

        self.right_box = pygame.Surface((300,self.res[1]-30),pygame.SRCALPHA)
        self.right_box_rect = self.right_box.get_rect(topleft=(self.res[0]-300,30))
        self.right_box.fill('#0000ff')

        self.map1 = Map(11, 6,self.mainSurface)
        self.map1.generate()
    def on(self):
        self.status = True
    def off(self):
        self.status = False
    def play(self):
        while self.status:
            self.mainSurface.blit(self.up_bar,(0,0))
            self.mainSurface.blit(self.right_box,(self.res[0]-300,30))
            press = pygame.key.get_pressed()
            if not self.bm.on_off:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit(0)
                    if press[pygame.K_UP]:
                        self.off()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # self.updateGui()
                        if event.button ==1:
                            x,y = event.pos
                            if self.right_box_rect.collidepoint(x,y):
                                print('open menu')
                                self.bm.open_menu()
                                
                            if self.map1.s_rect.collidepoint(x,y):
                                for item in self.map1.sprites():
                                    if item.is_point_inside_polygon((x,y)):
                                        item.change_type_hex(self.map1)
                                        self.scorehex = self.map1.PlayerHex
                
                self.map1.draw()
                self.timer()
            elif self.bm.on_off:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit(0)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # self.updateGui()
                        if event.button ==1:
                            x,y = event.pos
                            if self.right_box_rect.collidepoint(x,y):
                                print('close menu')
                                self.bm.close_menu()
                            for item in self.bm.sprites():
                                if item.rect_button.collidepoint(x,y):
                                    item.buy()
                self.bm.draw_menu()
                self.timer()
            pygame.display.update()

    def timer(self):
        FONT_SIZE = 36
        FONT_NAME = 'timesnewroman'
        font_timer = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        # Update the timer
        current_time = time.time()
        elapsed_time = current_time - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)

        # Draw the timer box
        timer_box = pygame.Rect(self.res[0]-200, self.res[1]-80, 180, 60)
        pygame.draw.rect(self.mainSurface, (255, 255, 255), timer_box)
        pygame.draw.rect(self.mainSurface, (0, 0, 0), timer_box, 2)

        # Draw the timer text
        timer_text = font_timer.render('{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds), True, (0, 0, 0))
        text_rect = timer_text.get_rect(center=timer_box.center)
        self.mainSurface.blit(timer_text, text_rect)
        self.screen.blit(self.mainSurface,(0,0))
        # Update the display
        pygame.display.update()
gra = Game()
import zmienne
def gameloop():
    zmienne.start_menu_status = False
    gra.on()
    gra.play()
    zmienne.start_menu_status = True
