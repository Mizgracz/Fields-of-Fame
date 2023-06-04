import sys, os
import zipfile
import random
from event_description import *
from pygame.locals import *
import pygame

from gameplay import *


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MAP_SIZE = 30
SWITCH_FOG = False
PLAYER_COUNT = 1
PLAYER_NAME =[]


pygame.mixer.init()
class Menu:
    status = True
    resume = False
    new_game = False
    PLAYER_NATION = []

    button_sound_save= pygame.mixer.Sound('music/music_ambient/save.mp3')
    button_sound_save.set_volume(1.0)
    button_sound_load = pygame.mixer.Sound('music/music_ambient/load.mp3')
    button_sound_load.set_volume(1.0)

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, max_tps: int):
        pygame.init()
        self.screen = screen
        self.clock = clock
        self.max_tps = max_tps
        Menu.status = True
        Menu.resume = False
        self.font = pygame.font.Font(None, 48)
        self.new_game_rect = pygame.Rect(SCREEN_WIDTH / 2 - 528, SCREEN_HEIGHT / 2 +10 , 255, 55)
        self.load_rect = pygame.Rect(SCREEN_WIDTH / 2 - 528, SCREEN_HEIGHT / 2 + 85, 255, 55)
        self.option_rect = pygame.Rect(SCREEN_WIDTH / 2 - 528, SCREEN_HEIGHT / 2 + 160, 255, 55)
        self.save_rect = pygame.Rect(SCREEN_WIDTH / 2 - 528, SCREEN_HEIGHT / 2 + 120, 255, 55)
        self.quit_rect = pygame.Rect(SCREEN_WIDTH / 2 - 528, SCREEN_HEIGHT / 2 + 235, 255, 55)
        self.background_texture = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/background.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.new_game_button_texture = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/graj_button.png").convert_alpha(),(339 * 0.769,81*0.75))
        self.new_game_marked_button_texture = pygame.transform.smoothscale(
            pygame.image.load("texture/main_menu/nowa_gra_button_red.png").convert_alpha(), (339 * 0.769, 81 * 0.75))
        self.resume_game_button_texture = pygame.image.load("texture/main_menu/wznow_button.png").convert_alpha()
        self.quit_button_texture = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/zamknij_button.png").convert_alpha(), (339 * 0.769, 81 * 0.75))
        self.quit_marked_button_texture = pygame.transform.smoothscale(
            pygame.image.load("texture/main_menu/wyjdz_button_red.png").convert_alpha(), (339 * 0.769, 81 * 0.75))
        self.option_button_texture = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/opcje_button.png").convert_alpha(),(339 * 0.769,81*0.75))
        self.option_marked_button_texture = pygame.transform.smoothscale(
            pygame.image.load("texture/main_menu/ustawienia_button_red.png").convert_alpha(), (339 * 0.769, 81 * 0.75))
        self.load_button_texture = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/wczytaj_button.png").convert_alpha(),(339 * 0.769,81*0.75))
        self.load_marked_button_texture = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/wczytaj_gre_button_red.png").convert_alpha(),(339 * 0.769,81*0.75))
        self.save_button_texture = pygame.image.load("texture/main_menu/zapisz_button.png").convert_alpha()
        self.config1 = Config(screen)
        self.MAP_SIZE = MAP_SIZE
        self.SWITCH_FOG = SWITCH_FOG
        self.PLAYER_COUNT = PLAYER_COUNT
        self.PLAYER_NAME = PLAYER_NAME


        self.run()


    def handle_events(self):
        pygame.mixer.init()
        button_sound = pygame.mixer.Sound('music/music_ambient/button_sound.mp3')
        button_sound.set_volume(1.0)

        self.event = pygame.event.get()
        for event in self.event:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                Menu.status = False
                self.config1.Active = False
                return 'quit'

            elif event.type == pygame.MOUSEBUTTONUP:
                button_sound.play()
                if self.config1.Button_Start_Rect.collidepoint(pos) and self.config1.Active == True:
                    PlayerConfig.Active = True

                    self.config1.Active = False
                    Menu.status = False
                    self.MAP_SIZE = MAP_SIZE
                    self.SWITCH_FOG = SWITCH_FOG
                    self.PLAYER_COUNT = PLAYER_COUNT


                    PlayerConfig(self.screen,self.clock,self.max_tps,self.PLAYER_COUNT)
                    


                    pygame.display.update()


                elif self.new_game_rect.collidepoint(pos):
                    if Menu.resume:
                        button_sound.play()

                        return 'resume'
                    else:
                        button_sound.play()
                        Menu.resume = True

                        print("new game")
                        return 'new_game'
                    


                elif self.config1.Button_Back_Rect.collidepoint(pos):
                    button_sound.play()
                    self.config1.Active = False
                    Menu.resume = False
                    Menu.status = True

                elif self.quit_rect.collidepoint(pos):
                    button_sound.play()
                    Menu.status = False
                    return 'quit'

                elif self.load_rect.collidepoint(pos):
                    button_sound.play()
                    Menu.status = False
                    print('load')
                    return 'load_game'
                elif self.save_rect.collidepoint(pos) and Menu.resume:
                    Menu.status = False

                    print('save')
                    return 'save_game'
                elif self.option_rect.collidepoint(pos):
                    button_sound.play()
                    print("OPCJE")
                    return 'game_options'

    def draw(self):

        pos = pygame.mouse.get_pos()
        self.screen.blit(self.background_texture, (0, 0))
        if self.load_rect.collidepoint(pos):
            self.screen.blit(self.load_marked_button_texture, self.load_rect)
        else:
            self.screen.blit(self.load_button_texture, self.load_rect)

        if self.option_rect.collidepoint(pos):
            self.screen.blit(self.option_marked_button_texture, self.option_rect)
        else:
            self.screen.blit(self.option_button_texture, self.option_rect)

        if self.new_game_rect.collidepoint(pos):
            button_texture = self.new_game_marked_button_texture
            

        else:
            if Menu.resume:
                button_texture = pygame.transform.scale(self.resume_game_button_texture,self.new_game_button_texture.get_size())
                # self.screen.blit(self.save_button_texture, self.save_rect)
            else:
                button_texture = self.new_game_button_texture

        self.screen.blit(button_texture, self.new_game_rect)

        if self.quit_rect.collidepoint(pos):
            quit_texture = self.quit_marked_button_texture
        else:
            quit_texture = self.quit_button_texture
        self.screen.blit(quit_texture, self.quit_rect)

        pygame.display.flip()

    def run(self):

        while Menu.status:
            choice = self.handle_events()
            pygame.display.update()
            if choice == 'new_game':

                self.config1.Active = True

                while self.config1.Active:
                    self.config1.draw(self.event)
                    self.handle_events()
            if choice == 'resume':
                Menu.status = False
            if choice == 'load_game':
                LoadMenu.status = True
                Menu.status = False
            if choice == 'save_game':
                SaveMenu.active = True
                Menu.status = False
            if choice == 'game_options':

                Menu.status = False

            elif choice == 'quit':
                sys.exit(0)
            if choice:
                return choice
            self.draw()
            self.clock.tick(self.max_tps)




class InputBox:
    ID = 0
    button_sound = pygame.mixer.Sound('music/music_ambient/button_sound.mp3')
    button_sound.set_volume(1.0)
    def __init__(self, x, y, w, h, text=''):
        InputBox.ID += 1
        self.ID = InputBox.ID
        self.text_font = pygame.font.Font(None, 16)
        color = (233, 248, 215)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.txt_surface = self.text_font.render(text, True, self.color)
        self.player_txt = self.text_font.render(f'Player {InputBox.ID}', True, self.color)
        self.active = False
        self.score = 1
        # Cursor declare
        self.txt_rect = self.txt_surface.get_rect()
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            InputBox.button_sound.play()
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)

                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    # Cursor

                    InputBox.button_sound.play()
                    # Limit characters           -20 for border width
                    if self.txt_surface.get_width() > self.rect.w - 15:
                        self.text = self.text[:-1]

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 10))
        # Blit the rect.
        screen.blit(self.player_txt,(self.rect.x -self.player_txt.get_width()-5, self.rect.y + 10))
        if self.active:
            pygame.draw.rect(screen, (255,0,0), self.rect, 1)
        else:
            pygame.draw.rect(screen, self.color, self.rect, 1)
        

    def update(self):
        # Re-render the text.
        self.txt_surface = self.text_font.render(self.text, True, self.color)
class NumberBox:
    def __init__(self,screen, x, y):

        self.screen = screen        
        # Define box dimensions
        BOX_WIDTH = 100
        BOX_HEIGHT = 50

        # Define button dimensions
        BUTTON_WIDTH = 50
        BUTTON_HEIGHT = 50
        self.value = 1
        self.rect = pygame.Rect(x, y, BOX_WIDTH, BOX_HEIGHT)
        self.font = pygame.font.SysFont(None, 48)
        self.button_inc = pygame.Rect(x + BOX_WIDTH, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.button_dec = pygame.Rect(x - BUTTON_WIDTH, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.font_buttons = pygame.font.SysFont(None, 32)

    def draw(self):
        pygame.draw.rect(self.screen, (200, 200, 200), self.rect)
        text = self.font.render(str(self.value), True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (150, 150, 150), self.button_inc)
        text_plus = self.font_buttons.render("+", True, (0, 0, 0))
        self.text_plus_rect = text_plus.get_rect(center=self.button_inc.center)
        self.screen.blit(text_plus, self.text_plus_rect)

        pygame.draw.rect(self.screen, (150, 150, 150), self.button_dec)
        text_minus = self.font_buttons.render("-", True, (0, 0, 0))
        self.text_minus_rect = text_minus.get_rect(center=self.button_dec.center)
        self.screen.blit(text_minus, self.text_minus_rect)

    def increment(self):
        self.value += 1
        return self.value

    def decrement(self):
        self.value -= 1
        return self.value

    def handle_event(self,eventlist):
        global PLAYER_COUNT
        for event in eventlist:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pygame.Rect.collidepoint(self.button_dec, mouse_pos):
                    if self.value is not 1:
                        PLAYER_COUNT = self.decrement()
                if pygame.Rect.collidepoint(self.button_inc, mouse_pos):
                    if self.value is not 4:
                        PLAYER_COUNT = self.increment()

class OptionBox():

    def __init__(self, x: int, y: int, w: int, h: int, color, highlight_color, font, option_list: list, selected=0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf: pygame.Surface):
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

class NationConfig:
    Active = True

    def __init__(self,screen:pygame.Surface,clock: pygame.time.Clock, max_tps: int,Player_count:int,player_name) -> None:
        self.screen = screen
        self.clock =clock
        self.max_tps = max_tps
        self.screen_width, self.screen_height = self.screen.get_size()
        self.Background = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/menu_konfiguracji_nacje.png")
                                                       , (self.screen_width,self.screen_height))
        self.Rozpocznij = pygame.image.load("texture/main_menu/nation/Rozpocznij gre.png")
        self.Rozpocznij_rect = self.Rozpocznij.get_rect()
        self.player_names = player_name
        self.select_list = []
        self.player_nation_list = []
        self.select_start()
        self.pick = None
        self.all_nation = ["kupcy","wojownicy","nomadzi","budowniczowie"]
        self.run()


    def draw(self):
        self.screen.blit(self.Background, (0, 0))
        self.Rozpocznij_rect.x = self.screen_width/15
        self.Rozpocznij_rect.y = self.screen_height - 100
        for i in self.select_list:
            i.draw()
        self.screen.blit(self.Rozpocznij, self.Rozpocznij_rect)


    def select_start(self):
        global PLAYER_COUNT
        x = self.screen_width/15
        y = self.screen_height/4
        licznik = 0
        for i in range(0, PLAYER_COUNT):
            name = self.player_names[licznik]
            Select = NationSelect(self.screen, x, y,self.Rozpocznij_rect.width,name)
            self.player_nation_list.append("kupcy")
            self.select_list.append(Select)
            y += 65
            licznik += 1
    def handle_events(self):
        global PLAYER_NAME
        self.event = pygame.event.get()
        for event in self.event:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.Rozpocznij_rect.collidepoint(pos) and NationConfig.Active == True:
                    return "new_game"

                for i in self.select_list:

                    if i.box_rect.collidepoint(pos):

                        if self.pick != None:
                            self.pick.nation_pick = False
                        i.nation_pick = True
                        self.pick = i
                        break
                    elif i.nation_rect.collidepoint(pos):
                        pass
                    elif i.opis_rect.collidepoint(pos):
                        pass
                    else:
                        i.nation_pick = False
                if self.pick != None:
                    if self.pick.left_rect.collidepoint(pos):


                        if self.pick.selected > 0:
                            self.pick.selected -= 1
                        self.pick.nation_pick = True

                if self.pick != None:
                    if self.pick.right_rect.collidepoint(pos):

                        if self.pick.selected < 3:
                            self.pick.selected += 1
                        self.pick.nation_pick = True

                if self.pick != None:
                    if self.pick.opis_box_rect.collidepoint(pos):
                        self.pick.opis_select = 0
                    if self.pick.statystki_box_rect.collidepoint(pos):
                        self.pick.opis_select = 1


    def run(self):

        while NationConfig.Active:
            choice = self.handle_events()
            pygame.display.update()
            if choice == 'new_game':
                NationConfig.Active = False



            elif choice == 'quit':
                sys.exit(0)
            if choice:
                return choice
            self.draw()
            l = 0
            for i in self.select_list:
                self.player_nation_list[l] = self.all_nation[i.selected]
                l += 1

            self.clock.tick(self.max_tps)


class NationSelect:

    def __init__(self,screen,x,y,start_width,name):

        self.box = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/player_box.png"),(347/1.2,52/1.2))

        self.box_red = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/player_box_red.png"),
                                                (347 / 1.2, 52 / 1.2))
        self.box_blue = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/player_box_blue.png"),
                                                (347 / 1.2, 52 / 1.2))
        self.box_yellow = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/player_box_yellow.png"),
                                                (347 / 1.2, 52 / 1.2))
        self.box_purple = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/player_box_purple.png"),
                                                (347 / 1.2, 52 / 1.2))

        self.opis_box = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/Opis_box.png"),(169/(100/75),61/(100/75)))
        self.statystki_box = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/statystyki_box.png"),
                                                     (169 / (100 / 75), 61 / (100 / 75)))

        self.opis_box_select = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/Opis_box_select.png"),
                                                     (169 / (100 / 75), 61 / (100 / 75)))
        self.statystki_box_select = pygame.transform.smoothscale(
            pygame.image.load("texture/main_menu/nation/statystyki_box_select.png"),
            (169 / (100 / 75), 61 / (100 / 75)))

        self.box_color_lists = [self.box_purple,self.box_red,self.box_yellow,self.box_blue]
        self.box_texture = self.box
        self.box_rect = self.box.get_rect()
        self.merchant = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/kupiec.png"),(536/(100/75),626/(100/80)))
        self.warior = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/wojownik.png"),(536/(100/75),626/(100/80)))
        self.opis = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/opis.png"),(336/(100/75),626/(100/80)))
        self.font_opis = pygame.font.Font(None, 20)
        self.left = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/arrow_left.png"),
                                                 (83 / (100 / 75), 374 / (100 / 75)))
        self.right = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/arrow_right.png"),
                                                 (83 / (100 / 75), 374 / (100 / 75)))

        self.screen = screen
        self.nation_pick = False
        self.font = pygame.font.Font(None, 32)
        self.font_wladcy = pygame.font.Font(None, 42)
        self.name = self.font.render(name, True, (255, 255, 255))
        self.wladcy = ["Godfrey Ametystowy Władca","Gunnvald Pogromca Barbarzynców","Chagan Pustynny Monarcha","Aurora Budownicza Cudów"]
        self.opis_select = 0
        self.selected = 0
        # ustawienie
        self.screen_width, self.screen_height = self.screen.get_size()
        self.box_rect.x = x + (start_width - self.box_rect.width) / 2
        self.box_rect.y = y
        self.name_rect = self.box_rect.copy()
        self.name_rect.x += 10
        self.name_rect.y += 10
        self.nation_rect = self.merchant.get_rect()
        self.nation_rect.x = self.screen_width/2.45
        self.nation_rect.y = self.screen_height * 0.20
        self.opis_rect = self.opis.get_rect()
        self.opis_rect.x = self.screen_width/1.365
        self.opis_rect.y = self.screen_height * 0.20
        self.opis_box_rect = self.opis_box.get_rect()
        self.opis_box_rect.x = self.opis_rect.x
        self.opis_box_rect.y = self.opis_rect.y
        self.opis_text_rect = self.opis_rect.copy()
        self.opis_text_rect.y += self.opis_box_rect.height + 10
        self.statystki_box_rect = self.statystki_box.get_rect()
        self.statystki_box_rect.x = self.opis_rect.x + self.opis_box_rect.width
        self.statystki_box_rect.y = self.opis_rect.y
        self.wladcy_rect = self.nation_rect.copy()
        self.wladcy_rect.y -= 80
        self.wladcy_rect.x += self.wladcy_rect.x/3.4
        self.left_rect = self.left.get_rect()
        self.right_rect = self.right.get_rect()
        self.left_rect.x = self.wladcy_rect.width +48
        self.left_rect.y = self.wladcy_rect.height /2
        self.right_rect.x = self.opis_rect.x + self.opis_rect.width + 20
        self.right_rect.y = self.left_rect.y


    def draw(self):
       self.screen.blit(self.box_texture, self.box_rect)
       self.screen.blit(self.name, self.name_rect)
       if self.nation_pick:
           self.box_texture = self.box_color_lists[self.selected]
           self.screen.blit(self.opis, self.opis_rect)
           self.screen.blit(self.left, self.left_rect)
           self.screen.blit(self.right, self.right_rect)
           self.screen.blit((self.font_wladcy.render(self.wladcy[self.selected], True, (255, 255, 255))), (self.wladcy_rect))
           self.opis_draw()
           if self.opis_select == 0:
               self.screen.blit(self.opis_box_select, self.opis_box_rect)
               self.screen.blit(self.statystki_box, self.statystki_box_rect)
           if self.opis_select == 1:
               self.screen.blit(self.opis_box, self.opis_box_rect)
               self.screen.blit(self.statystki_box_select, self.statystki_box_rect)


           if self.selected == 0:
               self.screen.blit(self.merchant, self.nation_rect)


           if self.selected == 1:
               self.screen.blit(self.warior, self.nation_rect)

    def opis_draw(self):

        if self.opis_select == 0:
            opisy = nation_opis_list[self.selected].splitlines()
            y = self.opis_text_rect.y

            for opis in opisy:
                self.font_opis = pygame.font.Font(None, 20)
                self.screen.blit(self.font_opis.render(opis, True, (255, 255, 255)), (self.opis_text_rect.x, y))
                y += self.font_opis.get_height()
        if self.opis_select == 1:
            opisy = nation_stats_list[self.selected].splitlines()
            y = self.opis_text_rect.y
            for opis in opisy:
                self.font_opis = pygame.font.Font(None, 24)
                self.screen.blit(self.font_opis.render(opis, True, (255, 255, 255)), (self.opis_text_rect.x, y))
                y += self.font_opis.get_height()


class PlayerConfig:
    Active = True
    def __init__(self,screen:pygame.Surface,clock: pygame.time.Clock, max_tps: int,Player_count:int) -> None:
        self.screen = screen
        self.clock =clock
        self.max_tps = max_tps
        self.allPlayers = []
        self.Background = pygame.image.load("texture/main_menu/config/Background.png")
        self.Button_Back = pygame.image.load("texture/main_menu/config/Button_Back.png")
        self.Button_Start = pygame.image.load("texture/main_menu/config/Button_Start.png")
        self.Button_Back_Rect = self.Button_Back.get_rect(center=(80, 40))
        self.Button_Start_Rect = self.Button_Start.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80))
        self.Active = False
        self.font = pygame.font.Font(None, 36)
        self.Player_count = Player_count
        self.input_boxes =[]
        for i in range(1,Player_count+1):
            self.input_boxes.append(InputBox(300,223+(50*i),250,36))
        self.run()
    def draw(self):
        if PlayerConfig.Active:
            self.screen.blit(self.Background,(0,0))
            self.screen.blit(self.Button_Back,self.Button_Back_Rect)
            self.screen.blit(self.Button_Start,self.Button_Start_Rect)
            for box in self.input_boxes:
                box.update()
            for box in self.input_boxes:
                box.draw(self.screen)
            pass
    def handle_events(self):
        global PLAYER_NAME
        self.event = pygame.event.get()
        for event in self.event:
            for box in self.input_boxes:
                box.handle_event(event)
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:

                if self.Button_Start_Rect.collidepoint(pos) and PlayerConfig.Active == True:


                    PlayerConfig.Active = False
                    self.MAP_SIZE = MAP_SIZE
                    self.SWITCH_FOG = SWITCH_FOG
                    self.PLAYER_COUNT = PLAYER_COUNT
                    
                    for box in self.input_boxes:
                        PLAYER_NAME += [box.text if box.text != '' else f'Player {box.ID}' ] 
                    self.PLAYER_NAME = PLAYER_NAME


                    nation =NationConfig(self.screen,self.clock,self.max_tps,self.PLAYER_COUNT,self.PLAYER_NAME)



                    Menu.PLAYER_NATION = nation.player_nation_list
                    Menu.new_game = True

                    pygame.display.update()


                elif self.Button_Back_Rect.collidepoint(pos):
                    PlayerConfig.Active = False
                    Menu.resume = False
                    Menu.status = True
                    self.input_boxes = []
                    InputBox.ID = 0
                    return 0

                
    def run(self):
        global PLAYER_NAME
        while PlayerConfig.Active:
            choice = self.handle_events()
            pygame.display.update()
            if choice == 'new_game':
                PlayerConfig.Active = False
                PLAYER_NAME = self.allPlayers
            elif choice == 'quit':
                sys.exit(0)
            if choice:
                return choice
            self.draw()
            self.clock.tick(self.max_tps)

        pass
class Config:
    def __init__(self, screen: pygame.surface):
        self.screen = screen
        self.Button_Back = pygame.image.load("texture/main_menu/config/Button_Back.png")
        self.Button_Start = pygame.image.load("texture/main_menu/config/Button_Start.png")
        self.Background = pygame.image.load("texture/main_menu/config/Background.png")
        self.Button_Back_Rect = self.Button_Back.get_rect(center=(80, 40))
        self.Button_Start_Rect = self.Button_Start.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80))
        self.Active = False
        self.font = pygame.font.Font(None, 36)
        self.text_map_size = self.font.render("Wielkość mapy : ", True, (255, 255, 255))
        self.text_player = self.font.render("Ilość graczy : ", True, (255, 255, 255))
        self.map_size = OptionBox(
            300, 223, 180, 60, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(None, 30),
            ["Mała (30x30)", "Średnia (50x50)", "Duża (60x60)"])
        self.text_fog_on_off = self.font.render("Mgła Wojny : ", True, (255, 255, 255))
        self.fog_on_off = OptionBox(
            700, 223, 180, 60, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(None, 30),
            ["Wyłącz", "Włącz"])
        self.Player_count_box = NumberBox(self.screen,350,350)
    def draw(self, event):
        global MAP_SIZE

        self.screen.blit(self.Background, (0, 0))
        self.Player_count_box.draw()
        self.screen.blit(self.Button_Back, self.Button_Back_Rect)
        self.screen.blit(self.Button_Start, self.Button_Start_Rect)
        self.screen.blit(self.text_map_size, (60, 240))
        self.screen.blit(self.text_player, (60, 360))
        self.screen.blit(self.text_fog_on_off, (525, 240))
        self.map_size.draw(self.screen)
        self.fog_on_off.draw(self.screen)
        self.event_list = event
        self.Size()
        self.Switching_Fog()
        self.Player_count_box.handle_event(self.event_list)

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

    def Switching_Fog(self):
        global SWITCH_FOG
        self.selected_option = self.fog_on_off.update(self.event_list)
        if self.selected_option == 0:
            SWITCH_FOG = False
        elif self.selected_option == 1:
            SWITCH_FOG = True

    


#################################################################################################################

class LoadMenu(object):
    """docstring for LoadMenu"""
    scroll = 0
    status = False

    def __init__(self, screen, GAME):
        super(LoadMenu, self).__init__()
        self.game = GAME

        self.MOUSE_Y = 0
        self.allItem = []
        self.screen = screen

        self.WINDOW_SIZE = self.screen.get_size()
        self.background_texture = pygame.Surface(self.WINDOW_SIZE)
        self.SCROLL_SURFACE = pygame.Surface((30, self.screen.get_size()[1] * 0.25))
        self.SCROLL_SURFACE.fill((0, 0, 0))
        self.SCROLL_RECT = pygame.Rect(0, 0, 0, 0)
        self.SCROLL_RECT.topleft = (self.screen.get_size()[0] - 30, 0)
        self.SCROLL_RECT.size = (30, self.screen.get_size()[1] * 0.25)
        self.RECT = pygame.Rect(self.WINDOW_SIZE[0] - 30, 0, 30, self.screen.get_size()[1] * 0.25)
        self.RECT.centery = self.screen.get_size()[1] * 0.25 / 2

        self.background_texture.fill('#00101f')
        ###CZYTAJ ILOŚĆ PLIKÓW PLIKI / 3
        self.folder_path = 'save/'
        self.ILOSC_PLIKOW = len(
            [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))])
        x = self.ILOSC_PLIKOW / 4.5
        if x < 1:
            x = 1
            pass
        self.x = x
        #### ZAOKRĄGLIĆ W GURE
        self.window = pygame.Surface((self.WINDOW_SIZE[0], self.WINDOW_SIZE[1] * x), pygame.SRCALPHA)

        self.on_bar = False
        self.mouse_diff = 0
        self.y_axis = 0
        self.change_y = 0

        bar_height = int((self.WINDOW_SIZE[1] - 40) / (self.window.get_size()[1] / (self.WINDOW_SIZE[1] * 1.0)))
        self.bar_rect = pygame.Rect(self.WINDOW_SIZE[0] - 40, 20, 40, bar_height)
        self.bar_up = pygame.Rect(self.WINDOW_SIZE[0] - 20, 0, 20, 20)
        self.bar_down = pygame.Rect(self.WINDOW_SIZE[0] - 20, self.WINDOW_SIZE[1] - 20, 20, 20)

        self.scroll_length = self.WINDOW_SIZE[1] - self.bar_rect.height - 40

        self.close_sur = pygame.image.load('texture/ui/load_menu/CheckBoxFalse.png')
        self.close_sur = pygame.transform.scale(self.close_sur, (50, 50))

        self.close_rect = self.close_sur.get_rect(topleft=(self.WINDOW_SIZE[0] - 100, 50))
        self.update()

    def update(self):
        self.allItem = []
        self.ILOSC_PLIKOW = len(
            [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))])
        x = self.ILOSC_PLIKOW / 4.5
        if x < 1:
            x = 1
            pass
        #### ZAOKRĄGLIĆ W GURE
        self.window = pygame.Surface((self.WINDOW_SIZE[0], self.WINDOW_SIZE[1] * x), pygame.SRCALPHA)
        from os import listdir
        from os.path import isfile, join
        mypath = 'save/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for i in range(self.ILOSC_PLIKOW):
            self.allItem += [LoadItem(f'{onlyfiles[i]}', self.window, i)]
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        if pygame.mouse.get_pressed()[0]:

            pos = pygame.mouse.get_pos()
            if self.close_rect.collidepoint(pos):
                print('EXIT')
                if Menu.resume == False:
                    Menu.status = True
                LoadMenu.status = False
                pygame.time.Clock().tick(3)
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            elif self.bar_up.collidepoint(pos):
                self.change_y = 10
            elif self.bar_down.collidepoint(pos):
                self.change_y = -10
        else:
            self.change_y = 0
            self.on_bar = False

        PRESS = pygame.mouse.get_pressed()[0]
        POS = pygame.mouse.get_pos()
        self.MOUSE_Y = pygame.mouse.get_pos()[1]
        for item in self.allItem:
            if item.rect_del.collidepoint(POS) and PRESS:
                item.remove()
                self.update()
                pygame.time.Clock().tick(3)
            if item.rect_item.collidepoint(POS) and PRESS:
                self.load_game(item.tmpID)
                LoadMenu.status = False
                pygame.time.Clock().tick(3)
        # if self.RECT.collidepoint(pygame.mouse.get_pos()) :

    def load_game(self, index):
        from gameplay import Stats
        print('LoadGame')
        import csv, zipfile
        Menu.resume = True
        with zipfile.ZipFile(f"save/{self.allItem[index].name}", "r") as zip:
            zip.extractall()
        with open(f'save/map.csv', 'r') as savefile:
            csvfile = csv.reader(savefile, delimiter=';')
            i = -1
            for row in csvfile:
                if i != -1:
                    self.game.map.allhex["hex", i].polozenie_hex_x = int(row[0])
                    self.game.map.allhex["hex", i].polozenie_hex_y = int(row[1])
                    self.game.map.allhex["hex", i].number = int(row[2])
                    self.game.map.allhex["hex", i].texture_index = int(row[3])
                    self.game.map.allhex['hex', i].zajete = True if (row[4]) == 'True' else False
                    self.game.map.allhex['hex', i].update_texture()

                i += 1

            pass
        with open(f'save/stats.txt', 'r') as savefile:
            # csvfile = csv.reader(savefile,delimiter=':')
            stats = []
            for line in savefile:
                stats += [line.strip().split(":")]
            print(stats)

            Stats.gold_count = int(stats[0][1])
            Stats.army_count = int(stats[1][1])
            Stats.terrain_count = int(stats[2][1])
            Stats.army_count_bonus = int(stats[3][1])
            Stats.gold_count_bonus = int(stats[4][1])
            Stats.turn_count = int(stats[5][1])
            print(Stats.gold_count, Stats.army_count, Stats.terrain_count, Stats.wyb, Stats.player_hex_status,
                  Stats.army_count_bonus, Stats.gold_count_bonus, Stats.turn_count)
        pygame.time.Clock().tick(1)
        os.remove(f"save/stats.txt")
        os.remove(f"save/map.csv")
        self.update()
        pygame.time.Clock().tick(3)
        pass

    def draw(self):

        self.handle_events()
        self.screen.blit(self.background_texture, (0, 0))

        self.y_axis += self.change_y

        if self.y_axis > 0:
            self.y_axis = 0
        elif (self.y_axis + self.window.get_size()[1]) < self.WINDOW_SIZE[1]:
            self.y_axis = self.WINDOW_SIZE[1] - self.window.get_size()[1]

        height_diff = self.window.get_size()[1] - self.WINDOW_SIZE[1]
        if height_diff == 0:
            height_diff = 1
        bar_half_lenght = self.bar_rect.height / 2 + 20
        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < 20:
                self.bar_rect.top = 20
            elif self.bar_rect.bottom > (self.WINDOW_SIZE[1] - 20):
                self.bar_rect.bottom = self.WINDOW_SIZE[1] - 20
            if self.x == 1:
                self.y_axis = 0
            else:
                self.y_axis = int(
                    height_diff / (self.scroll_length * 1.0) * (self.bar_rect.centery - bar_half_lenght) * -1)
            self.scroll = self.y_axis
        else:
            self.bar_rect.centery = self.scroll_length / (height_diff * 1.0) * (self.y_axis * -1) + bar_half_lenght
        for i in self.allItem:
            i.update()
            i.drawItem()

        pygame.draw.rect(self.screen, (255, 255, 0), self.bar_rect)
        self.screen.blit(self.window, (0, self.scroll))
        self.screen.blit(self.close_sur, self.close_rect)
        pygame.display.flip()


class LoadItem(object):
    _ID_ = 0
    """docstring for Item"""

    def __init__(self, name, screen: pygame.Surface, tmpID):
        FONT_SIZE = 25
        FONT_NAME = 'timesnewroman'
        font_text = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        super(LoadItem, self).__init__()
        self.screen = screen
        self.name = name
        self.tmpID = tmpID
        self.WIDTH = self.screen.get_size()[0] // 2
        self.HEIGHT = 100
        self.item_surface = pygame.image.load('texture/ui/load_menu/opis.png')
        self.item_surface = pygame.transform.scale(self.item_surface, (self.WIDTH, self.HEIGHT))

        self.del_surface = pygame.image.load('texture/ui/load_menu/CheckBoxFalse.png')
        self.del_surface = pygame.transform.scale(self.del_surface, (90, 90))

        self.rect_item = pygame.Rect(self.WIDTH / 2, 150 * self.tmpID + 50 + LoadMenu.scroll, self.WIDTH, 100)
        self.rect_del = pygame.Rect(self.WIDTH / 2 - 5, 150 * self.tmpID + 50 + LoadMenu.scroll + 5, 90, 90)

        self.rect_del.right = self.rect_item.right
        self.rect_item = pygame.Rect(self.WIDTH / 2, 150 * self.tmpID + 50 + LoadMenu.scroll, self.WIDTH - 100, 100)

        self.font_opis = font_text.render((f'{self.tmpID + 1}. {self.name}'), True, (255, 0, 0))

    def remove(self):
        os.remove(f"save/{self.name}")
        pass

    def drawItem(self):
        description_surf = pygame.Surface(self.item_surface.get_size(),
                                          pygame.SRCALPHA)
        description_surf.blit(self.font_opis, (10, 10))
        self.item_surface.blit(description_surf, (10, 5))
        self.screen.blit(self.item_surface, self.rect_item)
        self.screen.blit(self.del_surface, self.rect_del)

    def update(self):
        self.rect_item.top = 150 * self.tmpID + 50 + LoadMenu.scroll
        self.rect_del.top = 150 * self.tmpID + 50 + LoadMenu.scroll + 5


#################################################################################################################

class SaveMenu2(object):
    """docstring for SaveMenu"""
    scroll = 0
    status = False

    def __init__(self, screen: pygame.Surface, GAME):
        super(SaveMenu2, self).__init__()
        self.game = GAME

        self.MOUSE_Y = 0
        self.allItem = []
        self.screen = screen

        self.WINDOW_SIZE = self.screen.get_size()
        self.background_texture = pygame.Surface(self.WINDOW_SIZE)
        self.SCROLL_SURFACE = pygame.Surface((30, self.screen.get_size()[1] * 0.25))
        self.SCROLL_SURFACE.fill((0, 0, 0))
        self.SCROLL_RECT = pygame.Rect(0, 0, 0, 0)
        self.SCROLL_RECT.topleft = (self.screen.get_size()[0] - 30, 0)
        self.SCROLL_RECT.size = (30, self.screen.get_size()[1] * 0.25)
        self.RECT = pygame.Rect(self.WINDOW_SIZE[0] - 30, 0, 30, self.screen.get_size()[1] * 0.25)
        self.RECT.centery = self.screen.get_size()[1] * 0.25 / 2

        self.background_texture.fill('#00101f')
        ###CZYTAJ ILOŚĆ PLIKÓW PLIKI / 3
        self.folder_path = 'save/'
        self.ILOSC_PLIKOW = len(
            [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]) + 1
        x = self.ILOSC_PLIKOW / 4.5
        if x < 1:
            x = 1
            pass
        self.x = x
        #### ZAOKRĄGLIĆ W GURE
        self.window = pygame.Surface((self.WINDOW_SIZE[0], self.WINDOW_SIZE[1] * x + 250), pygame.SRCALPHA)

        self.on_bar = False
        self.mouse_diff = 0
        self.y_axis = 0
        self.change_y = 0

        bar_height = int((self.WINDOW_SIZE[1] - 40) / (self.window.get_size()[1] / (self.WINDOW_SIZE[1] * 1.0)))
        self.bar_rect = pygame.Rect(self.WINDOW_SIZE[0] - 40, 20, 40, bar_height)
        self.bar_up = pygame.Rect(self.WINDOW_SIZE[0] - 20, 0, 20, 20)
        self.bar_down = pygame.Rect(self.WINDOW_SIZE[0] - 20, self.WINDOW_SIZE[1] - 20, 20, 20)

        self.scroll_length = self.WINDOW_SIZE[1] - self.bar_rect.height - 40

        self.close_sur = pygame.image.load('texture/ui/load_menu/CheckBoxFalse.png')
        self.close_sur = pygame.transform.scale(self.close_sur, (50, 50))

        self.close_rect = self.close_sur.get_rect(topleft=(self.WINDOW_SIZE[0] - 100, 50))
        self.update()

    def update(self):
        self.allItem = []
        SaveItem2.ID = 0

        self.ILOSC_PLIKOW = len(
            [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]) + 1
        x = self.ILOSC_PLIKOW / 4.5
        if x < 1:
            x = 1
            pass
        #### ZAOKRĄGLIĆ W GURE
        self.window = pygame.Surface((self.WINDOW_SIZE[0], self.WINDOW_SIZE[1] * x + 250), pygame.SRCALPHA)
        from os import listdir
        from os.path import isfile, join
        mypath = 'save/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for i in range(self.ILOSC_PLIKOW - 1):
            self.allItem += [SaveItem2(f'{onlyfiles[i]}', self.window)]
        self.allItem += [SaveItem2(f'Save{SaveItem2.ID + 1}', self.screen)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        if pygame.mouse.get_pressed()[0]:

            pos = pygame.mouse.get_pos()
            if self.close_rect.collidepoint(pos):
                print('EXIT')
                if Menu.resume == False:
                    Menu.status = True
                SaveMenu2.status = False
                pygame.time.Clock().tick(3)
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            elif self.bar_up.collidepoint(pos):
                self.change_y = 10
            elif self.bar_down.collidepoint(pos):
                self.change_y = -10
        else:
            self.change_y = 0
            self.on_bar = False

        PRESS = pygame.mouse.get_pressed()[0]
        POS = pygame.mouse.get_pos()
        self.MOUSE_Y = pygame.mouse.get_pos()[1]
        for item in self.allItem:
            if item.rect_del.collidepoint(POS) and PRESS:
                item.remove()
                self.update()
                pygame.time.Clock().tick(3)
            if item.rect_item.collidepoint(POS) and PRESS:
                self.save_game(item.tmpID)
                SaveMenu2.status = False
                pygame.time.Clock().tick(3)
        # if self.RECT.collidepoint(pygame.mouse.get_pos()) :


    def draw(self):

        self.handle_events()
        self.screen.blit(self.background_texture, (0, 0))

        self.y_axis += self.change_y

        if self.y_axis > 0:
            self.y_axis = 0
        elif (self.y_axis + self.window.get_size()[1]) < self.WINDOW_SIZE[1]:
            self.y_axis = self.WINDOW_SIZE[1] - self.window.get_size()[1]

        height_diff = self.window.get_size()[1] - self.WINDOW_SIZE[1]
        if height_diff == 0:
            height_diff = 1
        bar_half_lenght = self.bar_rect.height / 2 + 20
        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < 20:
                self.bar_rect.top = 20
            elif self.bar_rect.bottom > (self.WINDOW_SIZE[1] - 20):
                self.bar_rect.bottom = self.WINDOW_SIZE[1] - 20
            elif self.x <= 1:
                self.y_axis = 0
            else:
                self.y_axis = int(
                    height_diff / (self.scroll_length * 1.0) * (self.bar_rect.centery - bar_half_lenght) * -1)
            self.scroll = self.y_axis
        else:
            self.bar_rect.centery = self.scroll_length / (height_diff * 1.0) * (self.y_axis * -1) + bar_half_lenght
        for i in self.allItem:
            i.update()
            i.drawItem()

        self.screen.blit(self.window, (0, self.scroll))
        self.screen.blit(self.close_sur, self.close_rect)
        pygame.display.flip()


class SaveItem2(object):
    ID = 0
    """docstring for Item"""

    def __init__(self, name, screen):
        FONT_SIZE = 25
        FONT_NAME = 'timesnewroman'
        font_text = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        super(SaveItem2, self).__init__()
        self.screen = screen
        self.name = name
        self.tmpID = SaveItem2.ID
        self.WIDTH = self.screen.get_size()[0] // 2
        self.HEIGHT = 100
        self.item_surface = pygame.image.load('texture/ui/load_menu/opis.png')
        self.item_surface = pygame.transform.scale(self.item_surface, (self.WIDTH, self.HEIGHT))

        self.del_surface = pygame.image.load('texture/ui/load_menu/CheckBoxFalse.png')
        self.del_surface = pygame.transform.scale(self.del_surface, (90, 90))

        self.rect_item = pygame.Rect(self.WIDTH / 2, 150 * self.tmpID + 50 + SaveMenu2.scroll, self.WIDTH, 100)
        self.rect_del = pygame.Rect(self.WIDTH / 2 - 5, 150 * self.tmpID + 50 + SaveMenu2.scroll + 5, 90, 90)

        self.rect_del.right = self.rect_item.right
        self.rect_item = pygame.Rect(self.WIDTH / 2, 150 * self.tmpID + 50 + SaveMenu2.scroll, self.WIDTH - 100, 100)

        self.font_opis = font_text.render((f'{self.tmpID + 1}. {self.name}'), True, (255, 0, 0))

        SaveItem2.ID += 1

    def remove(self):
        os.remove(f"save/{self.name}")
        pass

    def drawItem(self):
        description_surf = pygame.Surface(self.item_surface.get_size(),
                                          pygame.SRCALPHA)
        description_surf.blit(self.font_opis, (10, 10))
        self.item_surface.blit(description_surf, (10, 5))
        self.screen.blit(self.item_surface, self.rect_item)
        self.screen.blit(self.del_surface, self.rect_del)

    def update(self):
        self.rect_item.top = 150 * self.tmpID + 50 + SaveMenu2.scroll
        self.rect_del.top = 150 * self.tmpID + 50 + SaveMenu2.scroll + 5

#################################################################################################################
class BuildingItem:
    itemId = 0
    offset_x = 0
    offset_y = 0
    def __init__(self, name:str, description:str, image:pygame.Surface, cost:int, gold_buff:int, army_buff:int):
        self.available = True
        BuildingItem.itemId += 1
        self.item_id = BuildingItem.itemId
        self.name = name
        self.image = pygame.image.load(f'texture/ui/building/{image}').convert_alpha()
        self.image = pygame.transform.scale(self.image,(90,90))
        self.FONT = pygame.font.SysFont(None, 18)
        
        self.cost = cost
        self.army_buff = army_buff
        self.gold_buff = gold_buff


        self.font_surface = self.FONT.render(f"{self.name} - {self.cost} $", True, (255, 255,255))
        self.background = pygame.Surface((600-2,100-2))
        self.background = pygame.transform.scale(pygame.image.load('texture/ui/building/opis.png').convert_alpha(),(600-2,100-2))
        # self.background.fill((128,128,128))
        self.itemsurf = pygame.Surface((600,100),pygame.SRCALPHA)

        self.description = description


        self.button_rect = pygame.Rect(self.itemsurf.get_width() - 110, self.itemsurf.get_height() // 2 - 15, 100, 30)
        self.button_text = None

        self.image_width = self.image.get_width()
        self.decssurf_width = self.itemsurf.get_width() - self.image_width - self.button_rect.width-25

        self.decssurf = pygame.Surface((self.decssurf_width, 91), pygame.SRCALPHA)

        # self.button_image = pygame.Surface((self.button_rect.width,self.button_rect.height),pygame.SRCALPHA)
        # self.button_image = 
        self.button_image = pygame.transform.scale(pygame.image.load('texture/ui/building/button_kup.png').convert_alpha(),(self.button_rect.width,self.button_rect.height))
        


        self.draw_text(self.decssurf,self.description,self.FONT,(255,255,255),self.decssurf.get_rect())

    def split_text(self,text:str, font:pygame.font, surface_width:int):
        words = text.split()
        lines = []
        current_line = words[0]
        for word in words[1:]:
            test_line = current_line + " " + word
            if font.size(test_line)[0] <= surface_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def draw_text(self,surface:pygame.Surface, text:str, font, color:pygame.Color, rect:pygame.Rect):
        lines = self.split_text(text, font, rect.width)
        rect.y+=8+font.size("Tg")[1] 
        
        line_height = font.size("Tg")[1]  # Wysokość jednej linii tekstu
        
        max_lines = rect.height // line_height  # Maksymalna liczba linii, która zmieści się w wysokości powierzchni
        if len(lines) > max_lines:
            lines = lines[:max_lines-1]
            lines[-1] += " ..."  # Dodanie elips na końcu ostatniej linii
    
        y = rect.y
        for line in lines:
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (rect.x, y))
            y += line_height


    def draw(self, window, x, y):
        # Wyświetlanie g
        # rafiki przedmiotu na określonych współrzędnych
        self.itemsurf.blit(self.background,(1,1))
        self.itemsurf.blit(self.image,(5,5))
        self.itemsurf.blit(self.font_surface, (self.image.get_width()+9, 7))
        self.itemsurf.blit(self.decssurf,(100,0))
        

        self.itemsurf.blit(self.button_image,self.button_rect)
        if not self.button_text is None:
            self.itemsurf.blit(self.button_text, (self.button_rect.x + 10, self.button_rect.y + 8))
        window.blit(self.itemsurf, (x, y))

    def button_action(self,player,items):
        if self.cost<= player.gold_count:
            items.remove(self)
            self.button_image.fill('#00ff00')
            self.available = False
            self.button_text = self.FONT.render("Owned", True, (255, 255, 255))
            # Może sie kiedyś przyda
            player.gold_count += self.cost *-1
            player.army_count += 0
            #
            player.army_count_bonus += self.army_buff
            player.gold_count_bonus += self.gold_buff
            return True
        else:
            print('Brak złota')
            return False
        
        pass
class BuildingMenu:
    active = False
    def __init__(self, window:pygame.Surface, items:list[BuildingItem], menu_width:int, menu_height:int, menux:int = 0,menuy:int = 0):
        
        BuildingItem.offset_x = menux
        BuildingItem.offset_y = menuy
        
        self.window = window
        self.menu_items = items  # Przykładowa lista przedmiotów w menu
        self.menu_width = menu_width
        self.menu_height = menu_height
        self.menu_item_height = 100
        self.menu_top_item_index = 0
        self.item_spacing = 20  # Odstęp między przedmiotami
        

        self.background = pygame.Surface((menu_width,menu_height-25),pygame.SRCALPHA)
        self.background = pygame.transform.scale(pygame.image.load('texture/ui/building/opis_tlo.png').convert_alpha(), (menu_width,menu_height-25))
        # self.background.fill('#002200')
        ALPHA = 0.85
        self.background.set_alpha(255*ALPHA)
        

        # Scrollbar settings
        self.scrollbar_width = 16
        self.scrollbar_margin = 8
        
        self.scrollbar_y =  BuildingItem.offset_y-25
        self.scrollbar_height = self.background.get_height() - self.scrollbar_margin * 2

        self.menu_items_per_page = (self.menu_height - self.scrollbar_margin * 2) // (self.menu_item_height + self.item_spacing)
        self.menu_x = menux  # Set the desired x-coordinate of the menu
        self.menu_y = menuy  # Set the desired y-coordinate of the menu

        self.scrollbar_x = self.menu_x + self.background.get_width() - self.scrollbar_width - self.scrollbar_margin
    def draw_menu(self):
        
        
        # Rysowanie menu (inne elementy pominięte dla uproszczenia)
        self.window.blit(self.background, (self.menu_x-25,self.menu_y-25))
        for i, item in enumerate(self.menu_items):
            item_y = 0 + self.scrollbar_margin + (i - self.menu_top_item_index) * (self.menu_item_height + self.item_spacing)
            item_rect = pygame.Rect(25, item_y, self.background.get_width()-50, self.menu_item_height)
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                # Zaznaczony przedmiot
                pygame.draw.rect(self.background, (192, 192, 255), item_rect)
            pygame.draw.rect(self.background, (20, 30, 100), item_rect, 1)
            
            item.draw(self.background, 25, item_y)
            # self.window.blit(font_surface, (self.menu_x + 4, item_y + 2))
        # Scrollbar
        pygame.draw.rect(self.window, (128, 128, 128), (self.scrollbar_x, self.scrollbar_y, self.scrollbar_width, self.scrollbar_height))
        self.scrollbar_rect = pygame.Rect(self.scrollbar_x, self.scrollbar_y, self.scrollbar_width, self.scrollbar_height)
        # Calculate the position and height of the scrollbar thumb
        if len(self.menu_items) <4:
            self.thumb_height = self.scrollbar_height
            self.thumb_y = self.scrollbar_y + (self.menu_top_item_index / 1) * self.scrollbar_height
        else:
            self.thumb_height = self.scrollbar_height / len(self.menu_items) * self.menu_items_per_page
            self.thumb_y = self.scrollbar_y + (self.menu_top_item_index / len(self.menu_items)) * self.scrollbar_height
        

        # Draw the scrollbar thumb
        pygame.draw.rect(self.window, (192, 192, 192), (self.scrollbar_x, self.thumb_y, self.scrollbar_width, self.thumb_height))
    def handle_event(self, event,player):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            BuildingMenu.active = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Kliknięcie lewym przyciskiem myszy
                mouse_pos = pygame.mouse.get_pos()
                for i, item in enumerate(self.menu_items):
                    item_y = 0 + self.scrollbar_margin + (i - self.menu_top_item_index) * \
                        (self.menu_item_height + self.item_spacing)
                    item_rect = pygame.Rect(item.button_rect.x+BuildingItem.offset_x, item_y+BuildingItem.offset_y, item.button_rect.width, item.button_rect.height)
        
                    if item_rect.collidepoint(mouse_pos)and item.available and mouse_pos[1]<BuildingItem.offset_y+self.background.get_height() :
                        if item.button_action(player,self.menu_items):
                            self.background = pygame.transform.scale(pygame.image.load('texture/ui/building/opis_tlo.png').convert_alpha(), (self.menu_width,self.menu_height-25))
                            ALPHA = 0.85
                            self.background.set_alpha(255*ALPHA)
                        

        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_WHEELUP:  # Scroll up
                    if self.menu_top_item_index > 0:
                        self.menu_top_item_index -= 1
                elif event.button == pygame.BUTTON_WHEELDOWN:  # Scroll down
                    if self.menu_top_item_index + self.menu_items_per_page < len(self.menu_items):
                        self.menu_top_item_index += 1

                
                if event.button == pygame.BUTTON_LEFT:  # Left mouse button
                    if self.scrollbar_rect.collidepoint(event.pos):  # Check if the mouse is on the scrollbar
                        mouse_y = event.pos[1] - self.scrollbar_y
                        thumb_position = mouse_y - self.thumb_height / 2
                        max_thumb_position = self.scrollbar_height - self.thumb_height

                        # Limit the thumb position within the scrollbar
                        if thumb_position < 0:
                            thumb_position = 0
                        elif thumb_position > max_thumb_position:
                            thumb_position = max_thumb_position

                        # Calculate the corresponding menu top item index
                        self.menu_top_item_index = int((thumb_position / max_thumb_position) * (len(self.menu_items) - self.menu_items_per_page))

                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:  # Left mouse button is pressed
                        if self.scrollbar_rect.collidepoint(event.pos):  # Check if the mouse is on the scrollbar
                            mouse_y = event.pos[1] - self.scrollbar_y
                            thumb_position = mouse_y - self.thumb_height / 2
                            max_thumb_position = self.scrollbar_height - self.thumb_height

                            # Limit the thumb position within the scrollbar
                            if thumb_position < 0:
                                thumb_position = 0
                            elif thumb_position > max_thumb_position:
                                thumb_position = max_thumb_position

                            # Calculate the corresponding menu top item index
                            self.menu_top_item_index = int((thumb_position / max_thumb_position) * (len(self.menu_items) - self.menu_items_per_page))





class Item:
    itemId = 0
    
    def __init__(self, name:str="Item ",description:str="Wylogowywanie się z życia jest Ok :P "*100, image:pygame.Surface=None, cost:int=0):
        self.available = True
        Item.itemId += 1
        self.item_id = Item.itemId
        self.name = name + str(self.item_id)
        self.image = pygame.Surface((90, 90))
        self.image.fill('#ff00ff')

        self.FONT = pygame.font.SysFont(None, 30)
        self.cost = random.randint(10,100)
        self.font_surface = self.FONT.render(f"{self.name} - {self.cost} $", True, (0, 0, 0))
        self.background = pygame.Surface((pygame.display.get_window_size()[0]/2,100-2))
        self.background.fill((128,128,128))
        self.itemsurf = pygame.Surface((pygame.display.get_window_size()[0]/2-2,100),pygame.SRCALPHA)

        self.description = description


        self.button_rect = pygame.Rect(self.itemsurf.get_width() - 110, self.itemsurf.get_height() // 2 - 15, 100, 30)
        self.button_text = self.FONT.render("DELETE", True, (255, 255, 255))

        self.image_width = self.image.get_width()
        self.decssurf_width = self.itemsurf.get_width() - self.image_width - self.button_rect.width-25

        self.decssurf = pygame.Surface((self.decssurf_width, 91), pygame.SRCALPHA)

        self.button_image = pygame.Surface((self.button_rect.width,self.button_rect.height),SRCALPHA)
        self.button_image.fill('#000000')


        self.draw_text(self.decssurf,self.description,self.FONT,(0,0,0),self.decssurf.get_rect())
    def split_text(self,text:str, font:pygame.font, surface_width:int):
        words = text.split()
        lines = []
        current_line = words[0]
        for word in words[1:]:
            test_line = current_line + " " + word
            if font.size(test_line)[0] <= surface_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def draw_text(self,surface:pygame.Surface, text:str, font, color:pygame.Color, rect:pygame.Rect):
        lines = self.split_text(text, font, rect.width)
        rect.y+=8+font.size("Tg")[1] 
        
        line_height = font.size("Tg")[1]  # Wysokość jednej linii tekstu
        
        max_lines = rect.height // line_height  # Maksymalna liczba linii, która zmieści się w wysokości powierzchni
        if len(lines) > max_lines:
            lines = lines[:max_lines-1]
            lines[-1] += " ..."  # Dodanie elips na końcu ostatniej linii
    
        y = rect.y
        for line in lines:
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (rect.x, y))
            y += line_height


    def draw(self, window, x, y):
        # Wyświetlanie g self.menu_width/2
        # rafiki przedmiotu na określonych współrzędnych
        self.itemsurf.blit(self.background,(1,1))
        self.itemsurf.blit(self.image,(5,5))
        self.itemsurf.blit(self.font_surface, (self.image.get_width()+9, 7))
        self.itemsurf.blit(self.decssurf,(100,0))
        

        self.itemsurf.blit(self.button_image,self.button_rect)


        self.itemsurf.blit(self.button_text, (self.button_rect.x + 10, self.button_rect.y + 8))

        window.blit(self.itemsurf, (x, y))

    def button_action(self,items):
        
        items.remove(self)
        self.button_image.fill('#00ff00')
        self.available = False
        self.button_text = self.FONT.render("Owned", True, (255, 255, 255))
        pass
    
    def button_action2(self,game_data):
        
        save_game_data = game_data
        tmp = [game_data.allplayers,
        game_data.allevents,
        game_data.allbuildingmenu]
        # print(tmp)


        # Save Map
        with open('hexmap.csv', 'w',encoding='utf-8') as f:
            f.write('x;y;number;obwodka;zajete;odkryte;fild_add;textureID;rodzaj;surowiec\n')
            for hexagon in range(len(save_game_data.map.allhex)):
                f.write(str(save_game_data.map.allhex['hex',hexagon].polozenie_hex_x)+';')
                f.write(str(save_game_data.map.allhex['hex',hexagon].polozenie_hex_y)+';')
                f.write(str(save_game_data.map.allhex['hex',hexagon].number)+';')
                f.write(str(save_game_data.map.allhex['hex',hexagon].obwodka)+';')
                f.write(str(save_game_data.map.allhex['hex',hexagon].zajete)+';')
                f.write(str(save_game_data.map.allhex['hex',hexagon].odkryte)+';')
                f.write(str(save_game_data.map.allhex['hex',hexagon].field_add)+';')
                f.write(str(save_game_data.map.allhex['hex',hexagon].texture_index)+';')
                f.write(str(save_game_data.map.allhex['hex',hexagon].rodzaj)+ ';')
                f.write(str(save_game_data.map.allhex['hex',hexagon].rodzaj_surowca_var)+';')
                f.write('\n')
        with open('playerStats.csv', 'w',encoding='utf-8') as f:
            f.write('player_name;home;nacja;wyb;turn_stop;field_status;camera_stop;player_hex_status;gold_count;army_count;terrain_count;turn_count;army_count_bonus;gold_count_bonus;')
            for surowiec in save_game_data.allplayers[0].surowce_ilosc:
                f.write(str(surowiec[0])+';')
            f.write('\n')
            for player in save_game_data.allplayers:
                f.write(str(player.player_name)+';')
                f.write(str(player.home)+';')
                f.write(str(player.nacja)+';')
                f.write(str(player.wyb)+';')
                f.write(str(player.turn_stop)+';')
                f.write(str(player.field_status)+';')
                f.write(str(player.camera_stop)+';')
                f.write(str(player.player_hex_status)+';')
                f.write(str(player.gold_count)+';')
                f.write(str(player.army_count)+';')
                f.write(str(player.terrain_count)+';')
                f.write(str(player.turn_count)+';')
                f.write(str(player.army_count_bonus)+';')
                f.write(str(player.gold_count_bonus)+';')

                ######
                for surowiec in player.surowce_ilosc:
                    f.write(str(surowiec[1])+';')
                f.write('\n')
                
    
    
        
        
        self.button_text = self.FONT.render("Owned", True, (255, 255, 255))
        pass

    def print_info(self):
        print("Item ID:", self.item_id)
        print("Name:", self.name)
        print("Cost:", self.cost)
        print("Description:", self.description)
        print("------------------------")


class SaveMenu:
    active = False
    def __init__(self, window:pygame.Surface, items:list[Item], menu_width:int, menu_height:int):
        self.window = window
        self.menu_items = items  # Przykładowa lista przedmiotów w menu
        self.menu_width = menu_width
        self.menu_height = menu_height
        self.menu_item_height = 100
        self.menu_top_item_index = 0
        self.item_spacing = 20  # Odstęp między przedmiotami

        # Scrollbar settings
        self.scrollbar_width = 16
        self.scrollbar_margin = 8
        self.scrollbar_x = self.window.get_width() - self.scrollbar_width - self.scrollbar_margin
        self.scrollbar_y = self.scrollbar_margin
        self.scrollbar_height = self.window.get_height() - self.scrollbar_margin * 2

        self.menu_items_per_page = (self.menu_height - self.scrollbar_margin * 2) // (self.menu_item_height + self.item_spacing)
        self.menu_x = 0  # Set the desired x-coordinate of the menu
        self.menu_y = 0  # Set the desired y-coordinate of the menu

        self.back_rect = pygame.Rect(self.scrollbar_x-200,50,150,50)

    def draw_menu(self):
        # Rysowanie menu (inne elementy pominięte dla uproszczenia)
        
        pygame.draw.rect(self.window,(255,255,0),self.back_rect)

        for i, item in enumerate(self.menu_items):
            item_y = self.menu_y + self.scrollbar_margin + (i - self.menu_top_item_index) * (self.menu_item_height + self.item_spacing)
            item_rect = pygame.Rect(self.menu_width/4, item_y, self.menu_width/2, self.menu_item_height)
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                # Zaznaczony przedmiot
                pygame.draw.rect(self.window, (192, 192, 255), item_rect)
            pygame.draw.rect(self.window, (20, 30, 100), item_rect, 1)
            
            item.draw(self.window, item_rect.x, item_y)

        # Scrollbar
        pygame.draw.rect(self.window, (128, 128, 128), (self.scrollbar_x, self.scrollbar_y, self.scrollbar_width, self.scrollbar_height))
        self.scrollbar_rect = pygame.Rect(self.scrollbar_x, self.scrollbar_y, self.scrollbar_width, self.scrollbar_height)
        # Calculate the position and height of the scrollbar thumb
        self.thumb_height = self.scrollbar_height / len(self.menu_items) * self.menu_items_per_page
        self.thumb_y = self.scrollbar_y + (self.menu_top_item_index / len(self.menu_items)) * self.scrollbar_height

        # Draw the scrollbar thumb
        pygame.draw.rect(self.window, (192, 192, 192), (self.scrollbar_x, self.thumb_y, self.scrollbar_width, self.thumb_height))
    def handle_event(self, event,game):
        offset = self.menu_width/4
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Kliknięcie lewym przyciskiem myszy
                mouse_pos = pygame.mouse.get_pos()
                for i, item in enumerate(self.menu_items):
                    item_y = item.button_rect.y + self.scrollbar_margin + (i - self.menu_top_item_index) * \
                        (self.menu_item_height + self.item_spacing)
                    item_rect = pygame.Rect(item.button_rect.x+offset, item_y, item.button_rect.width, item.button_rect.height)
                    
                    
                    if self.back_rect.collidepoint(mouse_pos):
                        SaveMenu.active = False
                    if item_rect.collidepoint(mouse_pos)and item.available:
                        item.button_action2(game)
                        print('removed')
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_WHEELUP:  # Scroll up
                    if self.menu_top_item_index > 0:
                        self.menu_top_item_index -= 1
                elif event.button == pygame.BUTTON_WHEELDOWN:  # Scroll down
                    if self.menu_top_item_index + self.menu_items_per_page < len(self.menu_items):
                        self.menu_top_item_index += 1

                
                if event.button == pygame.BUTTON_LEFT:  # Left mouse button
                    if self.scrollbar_rect.collidepoint(event.pos):  # Check if the mouse is on the scrollbar
                        mouse_y = event.pos[1] - self.scrollbar_y
                        thumb_position = mouse_y - self.thumb_height / 2
                        max_thumb_position = self.scrollbar_height - self.thumb_height

                        # Limit the thumb position within the scrollbar
                        if thumb_position < 0:
                            thumb_position = 0
                        elif thumb_position > max_thumb_position:
                            thumb_position = max_thumb_position

                        # Calculate the corresponding menu top item index
                        self.menu_top_item_index = int((thumb_position / max_thumb_position) * (len(self.menu_items) - self.menu_items_per_page))

                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:  # Left mouse button is pressed
                        if self.scrollbar_rect.collidepoint(event.pos):  # Check if the mouse is on the scrollbar
                            mouse_y = event.pos[1] - self.scrollbar_y
                            thumb_position = mouse_y - self.thumb_height / 2
                            max_thumb_position = self.scrollbar_height - self.thumb_height

                            # Limit the thumb position within the scrollbar
                            if thumb_position < 0:
                                thumb_position = 0
                            elif thumb_position > max_thumb_position:
                                thumb_position = max_thumb_position

                            # Calculate the corresponding menu top item index
                            self.menu_top_item_index = int((thumb_position / max_thumb_position) * (len(self.menu_items) - self.menu_items_per_page))



