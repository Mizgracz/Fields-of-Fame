import sys

import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Menu:
    def __init__(self, screen, clock, max_tps):
        pygame.init()
        self.screen = screen
        self.clock = clock
        self.max_tps = max_tps
        self.status = True
        self.resume = False
        self.font = pygame.font.Font(None, 48)
        self.new_game_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 120, 200, 100)
        self.quit_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 120, 200, 100)
        self.background_texture = pygame.image.load("texture/main_menu/background.png").convert()
        self.new_game_button_texture = pygame.image.load("texture/main_menu/graj_button.png").convert_alpha()
        self.new_game_rect = self.new_game_button_texture.get_rect()
        self.new_game_rect.topleft = (490, 250)
        self.resume_game_button_texture = pygame.image.load("texture/main_menu/wznow_button.png").convert_alpha()
        self.quit_button_texture = pygame.image.load("texture/main_menu/zamknij_button.png").convert_alpha()
        self.load_button_texture = pygame.image.load("texture/main_menu/wczytaj_button.png").convert_alpha()
        self.gameplay = False
        self.config1 = Config(screen)

        while self.status:

            choose = self.run()

            pygame.display.update()



            if choose == 'new_game':

                self.config1.Active = True
                while self.config1.Active:
                    self.config1.draw()
                    self.handle_events()




            elif choose == 'quit':
                 sys.exit(0)



    def handle_events(self):

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                return 'quit'


            elif event.type == pygame.MOUSEBUTTONUP:

                if self.config1.Button_Start_Rect.collidepoint(pos):
                    self.gameplay = True
                    self.config1.Active = False
                    self.status = False
                    pygame.display.update()


                elif self.new_game_rect.collidepoint(pos):

                    return 'new_game'


                elif self.config1.Button_Back_Rect.collidepoint(pos):
                    self.config1.Active = False

                    self.resume = False


                elif self.quit_button.collidepoint(pos):
                    self.status = False
                    return 'quit'



    def draw(self):
        self.screen.blit(self.background_texture, (0, 0))
        self.screen.blit(self.load_button_texture, (SCREEN_WIDTH / 2 - 150, 360))
        if self.resume:
            button_texture = self.resume_game_button_texture
        else:
            button_texture = self.new_game_button_texture
        self.screen.blit(button_texture, self.new_game_rect)

        quit_texture = self.quit_button_texture
        self.screen.blit(quit_texture, self.quit_button)



    def run(self):
        choice = self.handle_events()
        if choice:
            return choice
        self.draw()
        self.clock.tick(self.max_tps)




class Config:
    def __init__(self, s1):
        self.screen = s1
        self.Button_Back = pygame.image.load("texture/main_menu/config/Button_Back.png")
        self.Button_Start = pygame.image.load("texture/main_menu/config/Button_Start.png")
        self.Background = pygame.image.load("texture/main_menu/config/Background.png")
        self.Button_Back_Rect = self.Button_Back.get_rect(center=(150, 70))
        self.Button_Start_Rect = self.Button_Start.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-80))
        self.Active = False



    def draw(self):
        self.screen.blit(self.Background, (0, 0))
        self.screen.blit(self.Button_Back, self.Button_Back_Rect)
        self.screen.blit(self.Button_Start, self.Button_Start_Rect)
        pygame.display.update()



