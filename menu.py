import sys

import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MAP_SIZE = 30

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
        self.MAP_SIZE = 30
        while self.status:

            choose = self.run()

            pygame.display.update()



            if choose == 'new_game':

                self.config1.Active = True
                while self.config1.Active:
                    self.config1.draw(self.event)

                    self.handle_events()




            elif choose == 'quit':
                 sys.exit(0)



    def handle_events(self):
        self.event = pygame.event.get()
        for event in self.event:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                return 'quit'


            elif event.type == pygame.MOUSEBUTTONUP:

                if self.config1.Button_Start_Rect.collidepoint(pos):
                    self.gameplay = True
                    self.config1.Active = False
                    self.status = False
                    self.MAP_SIZE = MAP_SIZE
                    print(self.MAP_SIZE)
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



class OptionBox():

    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected=0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1



    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (
            self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
        return -1



class Config:
    def __init__(self, s1):
        self.screen = s1
        self.Button_Back = pygame.image.load("texture/main_menu/config/Button_Back.png")
        self.Button_Start = pygame.image.load("texture/main_menu/config/Button_Start.png")
        self.Background = pygame.image.load("texture/main_menu/config/Background.png")
        self.Button_Back_Rect = self.Button_Back.get_rect(center=(80, 40))
        self.Button_Start_Rect = self.Button_Start.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-80))
        self.Active = False
        self.font = pygame.font.Font(None, 36)
        self.text_map_size = self.font.render("Wielkość mapy : ", True, (255, 255, 255))
        self.map_size = OptionBox(
            300, 223, 180, 60, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(None, 30),
            ["Mała (30x30)", "Średnia (50x50)", "Duża (60x60)"])



    def draw(self,event):
        self.screen.blit(self.Background, (0, 0))
        self.screen.blit(self.Button_Back, self.Button_Back_Rect)
        self.screen.blit(self.Button_Start, self.Button_Start_Rect)
        self.screen.blit(self.text_map_size, (60, 240))
        self.map_size.draw(self.screen)
        self.event_list = event
        self.Size()


        pygame.display.update()


    def Size(self):
        global MAP_SIZE
        self.selected_option = self.map_size.update(self.event_list)
        if self.selected_option == 0:
            MAP_SIZE = 30
        elif self.selected_option == 1:
            MAP_SIZE = 50
        elif self.selected_option == 2:
            MAP_SIZE = 60