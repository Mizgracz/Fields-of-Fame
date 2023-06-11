import configparser
import sys, os ,csv
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
config = configparser.ConfigParser()
config.read('settings.ini')
SCREEN_WIDTH = int(config.get('Ustawienia', 'width'))
SCREEN_HEIGHT = int(config.get('Ustawienia', 'height'))
FULLSCREEN_SWITCH = True if config.get('Ustawienia','fullscreen') == 'True' else False
MUSIC_VOLUME = int(config.get('Ustawienia','volume'))/100
SOUND_VOLUME = int(config.get('Ustawienia','sound'))/100
flags = pygame.DOUBLEBUF | (pygame.FULLSCREEN if FULLSCREEN_SWITCH else 0)
pygame.mixer.init()

class SOUND:

    button_sound = pygame.mixer.Sound('sound/click.mp3')
    slide_sound = pygame.mixer.Sound('sound/slide.mp3')
    button_sound_hourglass = pygame.mixer.Sound('music/music_ambient/hourglass.mp3')
    button_sound_money = pygame.mixer.Sound('music/music_ambient/coins.mp3')
    button_sound_army = pygame.mixer.Sound('music/music_ambient/army.mp3')
    button_sound_field = pygame.mixer.Sound('music/music_ambient/sand.mp3')
    sound_diamond = pygame.mixer.Sound('music/music_ambient/diamond.mp3')
    sound_horn = pygame.mixer.Sound('music/music_ambient/horn.mp3')
    sound_sword = pygame.mixer.Sound('music/music_ambient/sword.mp3')
    sound_coin = pygame.mixer.Sound('music/music_ambient/coin.mp3')
    sound_slice = pygame.mixer.Sound('music/music_ambient/slice.mp3')
    button_sound_save= pygame.mixer.Sound('music/music_ambient/save.mp3')
    button_sound_load = pygame.mixer.Sound('music/music_ambient/load.mp3')

    slide_sound.set_volume(SOUND_VOLUME)
    button_sound_save.set_volume(SOUND_VOLUME)
    button_sound_load.set_volume(SOUND_VOLUME)
    sound_horn.set_volume(SOUND_VOLUME)
    sound_sword.set_volume(SOUND_VOLUME)
    sound_coin.set_volume(SOUND_VOLUME)
    sound_slice.set_volume(SOUND_VOLUME)
    sound_diamond.set_volume(SOUND_VOLUME)
    button_sound_hourglass.set_volume(SOUND_VOLUME)
    button_sound.set_volume(SOUND_VOLUME)
    button_sound_money.set_volume(SOUND_VOLUME)
    button_sound_army.set_volume(SOUND_VOLUME)
    button_sound_field.set_volume(SOUND_VOLUME)

    button_sound_channel = pygame.mixer.Channel(1)
    button_sound_channel2 = pygame.mixer.Channel(2)
    button_sound_channel3 = pygame.mixer.Channel(3)
    button_sound_channel4 = pygame.mixer.Channel(4)


    new_game_sound_played = False
    quit_sound_played = False
    option_sound_played = False
    load_sound_played = False

    mouse_over_new_game = False
    mouse_over_quit = False
    mouse_over_option = False
    mouse_over_load = False
    mouse_over_back = False


    def __init__(self) -> None:
        pass
    
    def volumeupdate(volume):
        SOUND.button_sound_save.set_volume(volume)
        SOUND.button_sound_load.set_volume(volume)
        SOUND.sound_horn.set_volume(volume)
        SOUND.sound_sword.set_volume(volume)
        SOUND.sound_coin.set_volume(volume)
        SOUND.sound_slice.set_volume(volume)
        SOUND.sound_diamond.set_volume(volume)
        SOUND.button_sound_hourglass.set_volume(volume)
        SOUND.button_sound.set_volume(volume)
        SOUND.button_sound_money.set_volume(volume)
        SOUND.button_sound_army.set_volume(volume)
        SOUND.button_sound_field.set_volume(volume)
        SOUND.slide_sound.set_volume(SOUND_VOLUME)
        pass

    def hover(self,pos,new_game_rect,quit_rect,load_rect,option_rect):

        if not new_game_rect.collidepoint(pos):
            SOUND.mouse_over_new_game = False
            SOUND.new_game_sound_played = False
        elif not SOUND.mouse_over_new_game and not SOUND.new_game_sound_played:
            if not SOUND.button_sound_channel4.get_busy():
                SOUND.button_sound_channel4.play(SOUND.slide_sound)
                SOUND.new_game_sound_played = True
            SOUND.mouse_over_new_game = True
        elif SOUND.mouse_over_new_game and not new_game_rect.collidepoint(pos):
            SOUND.mouse_over_new_game = False

        if not quit_rect.collidepoint(pos):
            SOUND.mouse_over_quit = False
            SOUND.quit_sound_played = False
        elif not SOUND.mouse_over_quit and not SOUND.quit_sound_played:
            if not SOUND.button_sound_channel2.get_busy():
                SOUND.button_sound_channel2.play(SOUND.slide_sound)
                SOUND.quit_sound_played = True
            SOUND.mouse_over_quit = True
        elif SOUND.mouse_over_quit and not quit_rect.collidepoint(pos):
            SOUND.mouse_over_quit = False

        if not load_rect.collidepoint(pos):
            SOUND.mouse_over_load = False
            SOUND.load_sound_played = False
        elif not SOUND.mouse_over_load and not SOUND.load_sound_played:
            if not SOUND.button_sound_channel3.get_busy():
                SOUND.button_sound_channel3.play(SOUND.slide_sound)
                SOUND.load_sound_played = True
            SOUND.mouse_over_load = True
        elif SOUND.mouse_over_load and not load_rect.collidepoint(pos):
            SOUND.mouse_over_load = False

        if not option_rect.collidepoint(pos):
            SOUND.mouse_over_option = False
            SOUND.option_sound_played = False
        elif not SOUND.mouse_over_option and not SOUND.option_sound_played:
            if not SOUND.button_sound_channel.get_busy():
                SOUND.button_sound_channel.play(SOUND.slide_sound)
                SOUND.option_sound_played = True
            SOUND.mouse_over_option = True
        elif SOUND.mouse_over_option and not option_rect.collidepoint(pos):
            SOUND.mouse_over_option = False

    def hover_congif(self,config1,pos,new_game_rect):


        if not new_game_rect.collidepoint(pos):
            SOUND.mouse_over_new_game = False
            SOUND.new_game_sound_played = False
        elif not SOUND.mouse_over_new_game and not SOUND.new_game_sound_played:
            if not SOUND.button_sound_channel2.get_busy():
                SOUND.button_sound_channel2.play(SOUND.slide_sound)
                SOUND.new_game_sound_played = True
            SOUND.mouse_over_new_game = True
        elif SOUND.mouse_over_new_game and not new_game_rect.collidepoint(pos):
            SOUND.mouse_over_new_game = False


        if not config1.Button_Back_Rect.collidepoint(pos):
            SOUND.mouse_over_back = False
            SOUND.option_sound_played = False
        elif not SOUND.mouse_over_back and not SOUND.option_sound_played:
            if not SOUND.button_sound_channel.get_busy():
                SOUND.button_sound_channel.play(SOUND.slide_sound)
                SOUND.option_sound_played = True
            SOUND.mouse_over_back = True
        elif SOUND.mouse_over_back and not config1.Button_Back_Rect.collidepoint(pos):
            SOUND.mouse_over_back = False


class Menu:
    status = True
    
    new_game = False
    PLAYER_NATION = []
    

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, max_tps: int):
        pygame.init()
        self.screen = screen
        self.clock = clock
        self.max_tps = max_tps
        Menu.status = True
        
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

        self.options = MenuSettings(self.screen)
        self.run()


    def handle_events(self):
        pygame.mixer.init()
        

        self.event = pygame.event.get()
        for event in self.event:
            while MenuSettings.Active:
                self.options.draw()
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                Menu.status = False
                self.config1.Active = False
                return 'quit'

            if not self.config1.Active:
               SOUND.hover("xd",pos, self.new_game_rect, self.quit_rect, self.option_rect, self.load_rect)

            if self.config1.Active:

                SOUND.hover_congif("",self.config1, pos,self.config1.Button_Start_Rect)

            if event.type == pygame.MOUSEBUTTONUP:

                if self.config1.Button_Start_Rect.collidepoint(pos) and self.config1.Active == True:
                    SOUND.button_sound.play()
                    PlayerConfig.Active = True

                    self.config1.Active = False
                    Menu.status = False
                    self.MAP_SIZE = MAP_SIZE
                    self.SWITCH_FOG = SWITCH_FOG
                    self.PLAYER_COUNT = PLAYER_COUNT


                    PlayerConfig(self.screen,self.clock,self.max_tps,self.PLAYER_COUNT)



                    pygame.display.update()


                elif self.new_game_rect.collidepoint(pos) and not self.config1.Active:

                    SOUND.button_sound.play()


                    print("new game")
                    return 'new_game'


                elif self.config1.Button_Back_Rect.collidepoint(pos):
                    SOUND.button_sound.play()
                    self.config1.Active = False

                    Menu.status = True


                elif self.quit_rect.collidepoint(pos)  and not self.config1.Active:
                    SOUND.button_sound.play()
                    Menu.status = False
                    return 'quit'

                elif self.load_rect.collidepoint(pos)  and not self.config1.Active:
                    SOUND.button_sound.play()
                    Menu.status = False
                    print('load')
                    return 'load_game'
                elif self.save_rect.collidepoint(pos)  and not self.config1.Active:
                    Menu.status = False

                    print('save')
                    return 'save_game'
                elif self.option_rect.collidepoint(pos)  and not self.config1.Active:
                    SOUND.button_sound.play()
                    MenuSettings.Active = True
                    Menu.status = False

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
                MenuSettings.Active = True
                Menu.status = False

            elif choice == 'quit':
                sys.exit(0)
            if choice:
                return choice
            self.draw()
            self.clock.tick(self.max_tps)




class InputBox:
    ID = 0
    
    def __init__(self, x, y, w, h, text=''):
        InputBox.ID += 1
        self.ID = InputBox.ID
        self.text_font = pygame.font.Font('fonts/PirataOne-Regular.ttf', 20)
        self.text_font2 = pygame.font.Font('fonts/PirataOne-Regular.ttf', 30)
        color = (233, 248, 215)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.txt_surface = self.text_font.render(text, True, self.color)
        self.player_txt = self.text_font2.render(f'Player {InputBox.ID}', True, self.color)
        self.active = False
        self.score = 1
        # Cursor declare
        self.txt_rect = self.txt_surface.get_rect()
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.

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

                    SOUND.button_sound.play()
                    # Limit characters           -20 for border width
                    if self.txt_surface.get_width() > self.rect.w - 15:
                        self.text = self.text[:-1]

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 10))
        # Blit the rect.
        screen.blit(self.player_txt,(self.rect.x -self.player_txt.get_width()-16, self.rect.y ))
        if self.active:
            pygame.draw.rect(screen, (255,0,0), self.rect, 1)
        else:
            pygame.draw.rect(screen, self.color, self.rect, 1)
        

    def update(self):
        # Re-render the text.
        self.txt_surface = self.text_font.render(self.text, True, self.color)
class NumberBox:
    def __init__(self,screen, x, y,w,h,max_value = 4,min_value = 1 , start_value = 1):

        self.screen = screen        
        # Define box dimensions
        BOX_WIDTH = w
        BOX_HEIGHT = h

        # Define button dimensions
        BUTTON_WIDTH = 50
        BUTTON_HEIGHT = 50
        self.value = start_value
        self.max = max_value
        self.min = min_value
        self.rect = pygame.Rect(x, y, BOX_WIDTH, BOX_HEIGHT)
        self.font = pygame.font.SysFont('PirataOne-Regular.tff', 48)
        self.button_inc = pygame.Rect(x + BOX_WIDTH, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.button_dec = pygame.Rect(x - BUTTON_WIDTH, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.font_buttons = pygame.font.SysFont(None, 32)

    def draw(self):
        # pygame.draw.rect(self.screen, (200, 200, 200), self.rect)
        text = self.font.render(str(self.value), True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

        # pygame.draw.rect(self.screen, (150, 150, 150), self.button_inc)
        # text_plus = self.font_buttons.render("+", True, (0, 0, 0))
        # self.text_plus_rect = text_plus.get_rect(center=self.button_inc.center)
        # self.screen.blit(text_plus, self.text_plus_rect)

        # pygame.draw.rect(self.screen, (150, 150, 150), self.button_dec)
        # text_minus = self.font_buttons.render("-", True, (0, 0, 0))
        # self.text_minus_rect = text_minus.get_rect(center=self.button_dec.center)
        # self.screen.blit(text_minus, self.text_minus_rect)

    def increment(self):
        if self.value < self.max:
            self.value += 1
        return self.value

    def decrement(self):
        if self.value > self.min:
            self.value -= 1
        return self.value

    def handle_event(self,eventlist):
        global PLAYER_COUNT
        for event in eventlist:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pygame.Rect.collidepoint(self.button_dec, mouse_pos):
                    if self.value != 1:
                        PLAYER_COUNT = self.decrement()
                if pygame.Rect.collidepoint(self.button_inc, mouse_pos):
                    if self.value != 4:
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
        self.warior = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/wojownik2.png"),(536/(100/75),626/(100/80)))
        self.nomad = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/nomad.png"),
                                                   (536 / (100 / 75), 626 / (100 / 80)))
        self.budowniczowie = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/budowniczy.png"),
                                                  (536 / (100 / 75), 626 / (100 / 80)))


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

           if self.selected == 2:
               self.screen.blit(self.nomad, self.nation_rect)

           if self.selected == 3:
               self.screen.blit(self.budowniczowie, self.nation_rect)

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
        self.Background = pygame.image.load("texture/main_menu/config/menu_konfiguracji_pseudnimy.png")
        self.Button_Back = pygame.image.load("texture/main_menu/config/wrocdomenu.png")
        self.Button_Start = pygame.image.load("texture/main_menu/config/wybor_nacji.png")
        self.Button_Back_Rect = self.Button_Back.get_rect(topleft=(SCREEN_WIDTH*0.450, SCREEN_HEIGHT - 3*self.Button_Back.get_height()))
        self.Button_Start_Rect = self.Button_Start.get_rect(topleft=(self.Button_Back_Rect.right+30,self.Button_Back_Rect.y ))
        self.Active = False
        self.font = pygame.font.Font('fonts/PirataOne-Regular.ttf', 36)
        self.Player_count = Player_count
        self.input_boxes =[]
        for i in range(1,Player_count+1):
            self.input_boxes.append(InputBox(SCREEN_WIDTH*0.46,223+(50*i),250,36))
        self.run()
    def draw(self):
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

                    self.gameplay = True
                    PlayerConfig.Active = False
                    self.MAP_SIZE = MAP_SIZE
                    self.SWITCH_FOG = SWITCH_FOG
                    self.PLAYER_COUNT = PLAYER_COUNT
                    
                    for box in self.input_boxes:
                        PLAYER_NAME += [box.text if box.text != '' else f'Player {box.ID}' ]
                         
                    self.PLAYER_NAME = PLAYER_NAME
                    nation =NationConfig(self.screen,self.clock,self.max_tps,self.PLAYER_COUNT,self.PLAYER_NAME)

                    PlayerConfig(self.screen,self.clock,self.max_tps,self.PLAYER_COUNT)
                    Menu.PLAYER_NATION = nation.player_nation_list
                    Menu.new_game = True
                    pygame.display.update()

                elif self.Button_Back_Rect.collidepoint(pos):
                    PlayerConfig.Active = False
                    
                    Menu.status = True
                    self.input_boxes = []
                    InputBox.ID =0
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
        self.screen.fill("black")
        self.screen.blit(self.font.render("LOADING ...", True, '#ffffff'), (
        (SCREEN_WIDTH - self.font.render("LOADING ...", True, '#ffffff').get_width()) / 2, (SCREEN_HEIGHT / 2)))
        pass

class MenuSettings:
    SCREEN_WIDTH = SCREEN_WIDTH
    SCREEN_HEIGHT = SCREEN_HEIGHT
    Active = False
    def __init__(self, screen:pygame.Surface ):
        self.screen = screen
        self.Button_Back = pygame.transform.scale_by(pygame.image.load("texture/main_menu/config/wrocdomenu.png"),0.9)
        # self.Button_Start = pygame.transform.scale_by(pygame.image.load("texture/main_menu/config/przejdz_dalej.png"),0.9)
        self.Background = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/config/nick_back.png"),(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.zaznaczone = pygame.image.load("texture/main_menu/config/zaznaczone.png")
        self.niezaznaczone = pygame.image.load("texture/main_menu/config/niezaznaczone.png")
        self.zaznaczone_rect = self.zaznaczone.get_rect(topleft=(SCREEN_WIDTH*0.45, SCREEN_HEIGHT*0.57))

        self.plus = pygame.image.load("texture/main_menu/config/plus.png")
        self.ramka_ilosc = pygame.image.load("texture/main_menu/config/ramka_ilosc.png")
        self.minus = pygame.image.load("texture/main_menu/config/minus.png")

        self.mapBig = pygame.image.load("texture/main_menu/config/bigmap.png")
        self.mapMedium = pygame.image.load("texture/main_menu/config/mediummap.png")
        self.mapSmall = pygame.image.load("texture/main_menu/config/smallmap.png")
        self.mapSmall_Rect = self.mapSmall.get_rect(topleft=(SCREEN_WIDTH*0.45, SCREEN_HEIGHT*0.27))
        self.mapMedium_Rect = self.mapMedium.get_rect(topleft= (self.mapSmall_Rect.right+15,self.mapSmall_Rect.top))
        self.mapBig_Rect = self.mapBig.get_rect(topleft= (self.mapMedium_Rect.right+15,self.mapSmall_Rect.top))

        self.minus_rect = self.minus.get_rect(topleft=(SCREEN_WIDTH*0.45, SCREEN_HEIGHT*0.37))
        self.ramka_ilosc_rect = self.ramka_ilosc.get_rect()
        self.ramka_ilosc_rect.topleft = (self.minus_rect.right + 15,self.minus_rect.top)
        self.plus_rect = self.plus.get_rect()
        self.plus_rect.topleft = (self.ramka_ilosc_rect.right + 15,self.minus_rect.top)
        
        self.minus_rect2 = self.minus.get_rect(topleft=(SCREEN_WIDTH*0.45, SCREEN_HEIGHT*0.47))
        self.ramka_ilosc_rect2 = self.ramka_ilosc.get_rect()
        self.ramka_ilosc_rect2.topleft = (self.minus_rect2.right + 15,self.minus_rect2.top)
        self.plus_rect2 = self.plus.get_rect()
        self.plus_rect2.topleft = (self.ramka_ilosc_rect2.right + 15,self.minus_rect2.top)
        
        self.Button_Back_Rect = self.Button_Back.get_rect(topleft=(SCREEN_WIDTH*0.30, SCREEN_HEIGHT - 3*self.Button_Back.get_height()))

        self.font_file = pygame.font.Font('fonts/PirataOne-Regular.ttf', 36)
        
        self.text_size_screen = self.font_file.render('Rozmiar okna ', True, '#ffffff')
        self.text_volume = self.font_file.render('Muzyka', True, '#ffffff')
        self.text_fullscreen_on_off = self.font_file.render('Fullsceen', True, '#ffffff')
        self.text_sound = self.font_file.render('Dźwięk', True, '#ffffff')

        self.text_1280x720 =  self.font_file.render('1280x720 ', True, '#ffffff','#000000')
        self.text_1366x768 =  self.font_file.render('1366x768 ', True, '#ffffff','#000000')
        self.text_1920x1080 =  self.font_file.render('1920x1080', True, '#ffffff','#000000')
        
        self.screen.blit(self.text_size_screen, (SCREEN_WIDTH*0.29, self.mapSmall_Rect.y))
        self.screen.blit(self.text_volume, (SCREEN_WIDTH*0.29, self.minus_rect.y))
        self.screen.blit(self.text_fullscreen_on_off, (SCREEN_WIDTH*0.29, self.zaznaczone_rect.y))


        self.music_volume = NumberBox(self.screen,self.ramka_ilosc_rect.x,self.ramka_ilosc_rect.y,self.ramka_ilosc_rect.width,self.ramka_ilosc_rect.height,100,0,int(MUSIC_VOLUME*100))
        self.sound_volume = NumberBox(self.screen,self.ramka_ilosc_rect2.x,self.ramka_ilosc_rect2.y+0,self.ramka_ilosc_rect2.width,self.ramka_ilosc_rect2.height,100,0,int(SOUND_VOLUME*100))
        self.MapActive =[False,False,False]
    def draw(self,):
        global FULLSCREEN_SWITCH
        global MUSIC_VOLUME
        global SOUND_VOLUME
        global SCREEN_WIDTH
        global SCREEN_HEIGHT
        
        config.read('settings.ini')
        pos = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            
            if self.plus_rect.collidepoint(pos) and press[0]:
                SOUND.button_sound.play()
                self.music_volume.increment()
                config.set('Ustawienia', 'volume', f'{self.music_volume.value}')
                # Zapisanie zmienionego pliku ini
                with open('settings.ini', 'w') as configfile:
                    config.write(configfile)
                MUSIC_VOLUME = self.music_volume.value/100
                pygame.mixer.music.set_volume(MUSIC_VOLUME)
            if self.minus_rect.collidepoint(pos)and press[0]:
                SOUND.button_sound.play()
                self.music_volume.decrement()
                config.set('Ustawienia', 'volume', f'{self.music_volume.value}')
                # Zapisanie zmienionego pliku ini
                with open('settings.ini', 'w') as configfile:
                    config.write(configfile)
                MUSIC_VOLUME = self.music_volume.value/100
                pygame.mixer.music.set_volume(MUSIC_VOLUME)
            if self.plus_rect2.collidepoint(pos)and press[0]:
                SOUND.button_sound.play()
                self.sound_volume.increment()
                config.set('Ustawienia', 'sound', f'{self.sound_volume.value}')
                # Zapisanie zmienionego pliku ini
                with open('settings.ini', 'w') as configfile:
                    config.write(configfile)
                SOUND_VOLUME = self.sound_volume.value/100
                SOUND.volumeupdate(SOUND_VOLUME)
            if self.minus_rect2.collidepoint(pos)and press[0]:
                SOUND.button_sound.play()
                self.sound_volume.decrement()
                config.set('Ustawienia', 'sound', f'{self.sound_volume.value}')
                # Zapisanie zmienionego pliku ini
                with open('settings.ini', 'w') as configfile:
                    config.write(configfile)
                SOUND_VOLUME = self.sound_volume.value/100
                SOUND.volumeupdate(SOUND_VOLUME)
            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.Button_Back_Rect.collidepoint(pos):
                    MenuSettings.Active = False
                
                    
                if self.zaznaczone_rect.collidepoint(pos):
                    FULLSCREEN_SWITCH = True if FULLSCREEN_SWITCH == False else False
                    config.set('Ustawienia', 'fullscreen', f'{FULLSCREEN_SWITCH}')
                    # Zapisanie zmienionego pliku ini
                    with open('settings.ini', 'w') as configfile:
                        config.write(configfile)
                    global flags
                    flags = pygame.DOUBLEBUF | (pygame.FULLSCREEN if FULLSCREEN_SWITCH else 0)
                    pygame.display.set_mode()
                    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),flags)
                if self.mapSmall_Rect.collidepoint(pos):
                    self.MapActive[0]=True
                    self.MapActive[1]=False
                    self.MapActive[2]=False
                    # Odczyt pliku ini
                    # Zmiana wartości w sekcji i kluczu
                    config.set('Ustawienia', 'width', '1280')
                    config.set('Ustawienia', 'height', '720')
                    # Zapisanie zmienionego pliku ini
                    with open('settings.ini', 'w') as configfile:
                        config.write(configfile)
                    # SCREEN_WIDTH,SCREEN_HEIGHT = 1280,720
                    # pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),flags)
                if self.mapMedium_Rect.collidepoint(pos):
                    self.MapActive[0]=False
                    self.MapActive[1]=True
                    self.MapActive[2]=False
                    # Odczyt pliku ini
                    config.read('settings.ini')

                    # Zmiana wartości w sekcji i kluczu
                    config.set('Ustawienia', 'width', '1366')
                    config.set('Ustawienia', 'height', '768')
                    # SCREEN_WIDTH,SCREEN_HEIGHT = 1366,768
                    # pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),flags)
                    # Zapisanie zmienionego pliku ini
                    with open('settings.ini', 'w') as configfile:
                        config.write(configfile)
                if self.mapBig_Rect.collidepoint(pos):
                    self.MapActive[0]=False
                    self.MapActive[1]=False
                    self.MapActive[2]=True
                    # Odczyt pliku ini
                    config.read('settings.ini')

                    # Zmiana wartości w sekcji i kluczu
                    config.set('Ustawienia', 'width', '1920')
                    config.set('Ustawienia', 'height', '1080')

                    # Zapisanie zmienionego pliku ini
                    with open('settings.ini', 'w') as configfile:
                        config.write(configfile)
                    # SCREEN_WIDTH,SCREEN_HEIGHT = 1920,1080
                    # pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),flags)
        self.screen.blit(self.Background, (0, 0))
        self.screen.blit(self.Button_Back, self.Button_Back_Rect)
        
        self.screen.blit(self.minus, self.minus_rect)
        self.screen.blit(self.ramka_ilosc, self.ramka_ilosc_rect)
        self.screen.blit(self.plus, self.plus_rect)
        
        self.screen.blit(self.minus, self.minus_rect2)
        self.screen.blit(self.ramka_ilosc, self.ramka_ilosc_rect2)
        self.screen.blit(self.plus, self.plus_rect2)

        
        

        if FULLSCREEN_SWITCH:
            self.screen.blit(self.zaznaczone, self.zaznaczone_rect)
        else:
            self.screen.blit(self.niezaznaczone, self.zaznaczone_rect)
        self.screen.blit(self.text_1920x1080,self.mapBig_Rect)
        self.screen.blit(self.text_1366x768,self.mapMedium_Rect)
        self.screen.blit(self.text_1280x720,self.mapSmall_Rect)

        # pygame.draw.rect(self.screen,'#ff0000',self.mapSmall_Rect,2)
        # pygame.draw.rect(self.screen,'#00ff00',self.mapMedium_Rect,2)
        # pygame.draw.rect(self.screen,'#0000ff',self.mapBig_Rect,2)
        self.music_volume.draw()
        self.sound_volume.draw()
        # self.screen.blit(self.text_map_size, (60, 240))
        # self.screen.blit(self.text_player, (60, 360))
        # self.screen.blit(self.text_fog_on_off, (525, 240))
        self.screen.blit(self.text_size_screen, (SCREEN_WIDTH*0.29, self.mapSmall_Rect.y))
        self.screen.blit(self.text_volume, (SCREEN_WIDTH*0.29, self.minus_rect.y))
        self.screen.blit(self.text_sound, (SCREEN_WIDTH*0.29, self.minus_rect2.y))
        self.screen.blit(self.text_fullscreen_on_off, (SCREEN_WIDTH*0.29, self.zaznaczone_rect.y))

        if self.MapActive[0]:
            pygame.draw.rect(self.screen,"#ff0000",self.mapSmall_Rect,2)
        if self.MapActive[1]:
            pygame.draw.rect(self.screen,"#ff0000",self.mapMedium_Rect,2)
        if self.MapActive[2]:
            pygame.draw.rect(self.screen,"#ff0000",self.mapBig_Rect,2)


        pygame.display.update()


class Config:
        
    def __init__(self, screen:pygame.Surface ):
        self.Active = False
        self.screen = screen
        self.font_file = pygame.font.Font('fonts/PirataOne-Regular.ttf',36)
        self.Button_Back = pygame.transform.scale_by(pygame.image.load("texture/main_menu/config/wrocdomenu.png"),0.9)
        self.Button_Start = pygame.transform.scale_by(pygame.image.load("texture/main_menu/config/przejdz_dalej.png"),0.9)
        self.Background = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/config/menu_konfiguracji_1.png"),(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.zaznaczone = pygame.image.load("texture/main_menu/config/zaznaczone.png")
        self.niezaznaczone = pygame.image.load("texture/main_menu/config/niezaznaczone.png")
        self.zaznaczone_rect = self.zaznaczone.get_rect(topleft=(SCREEN_WIDTH*0.45, SCREEN_HEIGHT*0.47))
        self.plus = pygame.image.load("texture/main_menu/config/plus.png")
        self.ramka_ilosc = pygame.image.load("texture/main_menu/config/ramka_ilosc.png")
        self.minus = pygame.image.load("texture/main_menu/config/minus.png")
        self.mapBig = pygame.image.load("texture/main_menu/config/bigmap.png")
        self.mapMedium = pygame.image.load("texture/main_menu/config/mediummap.png")
        self.mapSmall = pygame.image.load("texture/main_menu/config/smallmap.png")
        self.mapSmall_Rect = self.mapSmall.get_rect(topleft=(SCREEN_WIDTH*0.45, SCREEN_HEIGHT*0.27))
        self.mapMedium_Rect = self.mapMedium.get_rect(topleft= (self.mapSmall_Rect.right+15,self.mapSmall_Rect.top))
        self.mapBig_Rect = self.mapBig.get_rect(topleft= (self.mapMedium_Rect.right+15,self.mapSmall_Rect.top))

        self.minus_rect = self.minus.get_rect(topleft=(SCREEN_WIDTH*0.45, SCREEN_HEIGHT*0.37))
        self.ramka_ilosc_rect = self.ramka_ilosc.get_rect()
        self.ramka_ilosc_rect.topleft = (self.minus_rect.right + 15,self.minus_rect.top)
        self.plus_rect = self.plus.get_rect()
        self.plus_rect.topleft = (self.ramka_ilosc_rect.right + 15,self.minus_rect.top)
        self.Button_Back_Rect = self.Button_Back.get_rect(topleft=(SCREEN_WIDTH*0.30, SCREEN_HEIGHT - 3*self.Button_Back.get_height()))
        self.Button_Start_Rect = self.Button_Start.get_rect(topleft=(self.Button_Back_Rect.right+30,self.Button_Back_Rect.y ))

        #HOVER
        self.Button_Start_HOV = pygame.transform.scale_by(pygame.image.load("texture/main_menu/config/przejdz_dalej_button.png"),
                                                   0.9)
        self.Button_Back_HOV = pygame.transform.scale_by(pygame.image.load("texture/main_menu/config/wroc_do_menu_button.png"),0.9)

        self.minus_HOV = pygame.image.load("texture/main_menu/config/minus_button.png")
        self.plus_HOV = pygame.image.load("texture/main_menu/config/plus_button.png")
        self.mapBig_HOV = pygame.image.load("texture/main_menu/config/duza_button.png")
        self.mapMedium_HOV = pygame.image.load("texture/main_menu/config/srednia_button.png")
        self.mapSmall_HOV = pygame.image.load("texture/main_menu/config/mala_button.png")


        self.text_map_size = self.font_file.render('Wielkość mapy: ', True, '#ffffff')
        self.text_player = self.font_file.render('Ilość graczy', True, '#ffffff')
        self.text_fog_on_off = self.font_file.render('Mgła wojny', True, '#ffffff')

        self.Player_count_box = NumberBox(self.screen,self.ramka_ilosc_rect.x,self.ramka_ilosc_rect.y,self.ramka_ilosc_rect.width,self.ramka_ilosc_rect.height)
        self.MapActive =[True,False,False]

    def draw(self,events):
        global MAP_SIZE
        global SWITCH_FOG
        global PLAYER_COUNT
        pos = pygame.mouse.get_pos()
        self.screen.blit(self.Background, (0, 0))

        if self.Button_Back_Rect.collidepoint(pos):
            self.screen.blit(self.Button_Back_HOV, self.Button_Back_Rect)
        else:
            self.screen.blit(self.Button_Back, self.Button_Back_Rect)

        if self.Button_Start_Rect.collidepoint(pos):
            self.screen.blit(self.Button_Start_HOV, self.Button_Start_Rect)
        else:
            self.screen.blit(self.Button_Start, self.Button_Start_Rect)

        if self.minus_rect.collidepoint(pos):
            self.screen.blit(self.minus_HOV, self.minus_rect)
        else:
            self.screen.blit(self.minus, self.minus_rect)


        if self.plus_rect.collidepoint(pos):
            self.screen.blit(self.plus_HOV, self.plus_rect)
        else:
            self.screen.blit(self.plus, self.plus_rect)


        self.screen.blit(self.ramka_ilosc, self.ramka_ilosc_rect)


        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.Button_Back_Rect.collidepoint(pos):
                    MenuSettings.Active = False
                if self.plus_rect.collidepoint(pos):
                    SOUND.button_sound.play()
                    self.Player_count_box.increment()
                    PLAYER_COUNT = self.Player_count_box.value
                if self.minus_rect.collidepoint(pos):
                    SOUND.button_sound.play()
                    self.Player_count_box.decrement()
                    PLAYER_COUNT = self.Player_count_box.value
                if self.zaznaczone_rect.collidepoint(pos):
                    SWITCH_FOG = True if SWITCH_FOG == False else False
                if self.mapSmall_Rect.collidepoint(pos):
                    SOUND.button_sound.play()
                    self.MapActive[0]=True
                    self.MapActive[1]=False
                    self.MapActive[2]=False
                    MAP_SIZE = 30
                if self.mapMedium_Rect.collidepoint(pos):
                    SOUND.button_sound.play()
                    self.MapActive[0]=False
                    self.MapActive[1]=True
                    self.MapActive[2]=False
                    MAP_SIZE = 50
                if self.mapBig_Rect.collidepoint(pos):
                    SOUND.button_sound.play()
                    self.MapActive[0]=False
                    self.MapActive[1]=False
                    self.MapActive[2]=True
                    MAP_SIZE = 60
        


        
        

        if SWITCH_FOG:
            self.screen.blit(self.zaznaczone, self.zaznaczone_rect)
        else:
            self.screen.blit(self.niezaznaczone, self.zaznaczone_rect)
        self.screen.blit(self.mapBig,self.mapBig_Rect)
        self.screen.blit(self.mapMedium,self.mapMedium_Rect)
        self.screen.blit(self.mapSmall,self.mapSmall_Rect)


        self.Player_count_box.draw()
        
        

        self.screen.blit(self.text_map_size, (SCREEN_WIDTH*0.29, self.mapSmall_Rect.y))
        self.screen.blit(self.text_player, (SCREEN_WIDTH*0.29, self.minus_rect.y))
        self.screen.blit(self.text_fog_on_off, (SCREEN_WIDTH*0.29, self.zaznaczone_rect.y))

        if self.MapActive[0]:
            self.screen.blit(self.mapSmall_HOV,self.mapSmall_Rect)
        if self.MapActive[1]:
            self.screen.blit(self.mapMedium_HOV,self.mapMedium_Rect)
        if self.MapActive[2]:
            self.screen.blit(self.mapBig_HOV,self.mapBig_Rect)


        pygame.display.update()



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
class BuildingItem:
    itemId = 0
    offset_x = 0
    offset_y = 0

    def __init__(self, name: str, description: str, image: pygame.Surface, cost: int, gold_buff: int, army_buff: int):
        self.available = True
        BuildingItem.itemId += 1
        self.item_id = BuildingItem.itemId
        self.name = name
        self.image = pygame.image.load(f'texture/ui/building/{image}').convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.FONT = pygame.font.SysFont(None, 18)

        self.cost = cost
        self.army_buff = army_buff
        self.gold_buff = gold_buff

        self.font_surface = self.FONT.render(f"{self.name} - {self.cost} $", True, (255, 255, 255))
        self.background = pygame.Surface((600 - 2, 100 - 2))
        self.background = pygame.transform.scale(pygame.image.load('texture/ui/building/opis.png').convert_alpha(),
                                                 (600 - 2, 100 - 2))
        # self.background.fill((128,128,128))
        self.itemsurf = pygame.Surface((600, 100), pygame.SRCALPHA)

        self.description = description

        self.button_rect = pygame.Rect(self.itemsurf.get_width() - 110, self.itemsurf.get_height() // 2 - 15, 100, 30)
        self.button_text = None

        self.image_width = self.image.get_width()
        self.decssurf_width = self.itemsurf.get_width() - self.image_width - self.button_rect.width - 25

        self.decssurf = pygame.Surface((self.decssurf_width, 91), pygame.SRCALPHA)

        # self.button_image = pygame.Surface((self.button_rect.width,self.button_rect.height),pygame.SRCALPHA)
        # self.button_image =
        self.button_image = pygame.transform.scale(
            pygame.image.load('texture/ui/building/button_kup.png').convert_alpha(),
            (self.button_rect.width, self.button_rect.height))

        self.draw_text(self.decssurf, self.description, self.FONT, (255, 255, 255), self.decssurf.get_rect())

    def split_text(self, text: str, font: pygame.font, surface_width: int):
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

    def draw_text(self, surface: pygame.Surface, text: str, font, color: pygame.Color, rect: pygame.Rect):
        lines = self.split_text(text, font, rect.width)
        rect.y += 8 + font.size("Tg")[1]

        line_height = font.size("Tg")[1]  # Wysokość jednej linii tekstu

        max_lines = rect.height // line_height  # Maksymalna liczba linii, która zmieści się w wysokości powierzchni
        if len(lines) > max_lines:
            lines = lines[:max_lines - 1]
            lines[-1] += " ..."  # Dodanie elips na końcu ostatniej linii

        y = rect.y
        for line in lines:
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (rect.x, y))
            y += line_height

    def draw(self, window, x, y):
        # Wyświetlanie g
        # rafiki przedmiotu na określonych współrzędnych
        self.itemsurf.blit(self.background, (1, 1))
        self.itemsurf.blit(self.image, (5, 5))
        self.itemsurf.blit(self.font_surface, (self.image.get_width() + 9, 7))
        self.itemsurf.blit(self.decssurf, (100, 0))

        self.itemsurf.blit(self.button_image, self.button_rect)
        if not self.button_text is None:
            self.itemsurf.blit(self.button_text, (self.button_rect.x + 10, self.button_rect.y + 8))
        window.blit(self.itemsurf, (x, y))

    def button_action(self, player, items):
        if self.cost <= player.gold_count:
            items.remove(self)
            self.button_image.fill('#00ff00')
            self.available = False
            self.button_text = self.FONT.render("Owned", True, (255, 255, 255))
            # Może sie kiedyś przyda
            player.gold_count += self.cost * -1
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

    def __init__(self, window: pygame.Surface, items: list[BuildingItem], menu_width: int, menu_height: int,
                 menux: int = 0, menuy: int = 0):

        BuildingItem.offset_x = menux
        BuildingItem.offset_y = menuy

        self.window = window
        self.menu_items = items  # Przykładowa lista przedmiotów w menu
        self.menu_width = menu_width
        self.menu_height = menu_height
        self.menu_item_height = 100
        self.menu_top_item_index = 0
        self.item_spacing = 20  # Odstęp między przedmiotami

        self.background = pygame.Surface((menu_width, menu_height - 25), pygame.SRCALPHA)
        self.background = pygame.transform.scale(
            pygame.image.load('texture/ui/building/budynki_tlo.png').convert_alpha(), (menu_width, menu_height - 25))
        # self.background.fill('#002200')
        ALPHA = 0.85
        self.background.set_alpha(255 * ALPHA)

        # Scrollbar settings
        self.scrollbar_width = 16
        self.scrollbar_margin = 8

        self.scrollbar_y = BuildingItem.offset_y - 25
        self.scrollbar_height = self.background.get_height() - self.scrollbar_margin * 2

        self.menu_items_per_page = (self.menu_height - self.scrollbar_margin * 2) // (
                    self.menu_item_height + self.item_spacing)
        self.menu_x = menux  # Set the desired x-coordinate of the menu
        self.menu_y = menuy  # Set the desired y-coordinate of the menu

        self.scrollbar_x = self.menu_x + self.background.get_width() - self.scrollbar_width - self.scrollbar_margin

    def draw_menu(self):

        # Rysowanie menu (inne elementy pominięte dla uproszczenia)
        self.window.blit(self.background, (self.menu_x - 25, self.menu_y - 25))
        for i, item in enumerate(self.menu_items):
            item_y = 0 + self.scrollbar_margin + (i - self.menu_top_item_index) * (
                        self.menu_item_height + self.item_spacing)
            item_rect = pygame.Rect(25, item_y, self.background.get_width() - 50, self.menu_item_height)
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                # Zaznaczony przedmiot
                pygame.draw.rect(self.background, (192, 192, 255), item_rect)
            pygame.draw.rect(self.background, (20, 30, 100), item_rect, 1)

            item.draw(self.background, 25, item_y)
            # self.window.blit(font_surface, (self.menu_x + 4, item_y + 2))
        # Scrollbar
        pygame.draw.rect(self.window, (16, 32, 66),
                         (self.scrollbar_x, self.scrollbar_y, self.scrollbar_width, self.scrollbar_height + 16))
        self.scrollbar_rect = pygame.Rect(self.scrollbar_x, self.scrollbar_y, self.scrollbar_width,
                                          self.scrollbar_height + 16)
        # Calculate the position and height of the scrollbar thumb
        if len(self.menu_items) < 4:
            self.thumb_height = self.scrollbar_height + 16
            self.thumb_y = self.scrollbar_y + (self.menu_top_item_index / 1) * self.scrollbar_height
        else:
            self.thumb_height = self.scrollbar_height / len(self.menu_items) * self.menu_items_per_page + 16
            self.thumb_y = self.scrollbar_y + (self.menu_top_item_index / len(self.menu_items)) * self.scrollbar_height

        # Draw the scrollbar thumb
        pygame.draw.rect(self.window, (255, 170, 20),
                         (self.scrollbar_x, self.thumb_y, self.scrollbar_width, self.thumb_height))

    def handle_event(self, event, player):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            BuildingMenu.active = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Kliknięcie lewym przyciskiem myszy
                mouse_pos = pygame.mouse.get_pos()
                for i, item in enumerate(self.menu_items):
                    item_y = 0 + self.scrollbar_margin + (i - self.menu_top_item_index) * \
                             (self.menu_item_height + self.item_spacing)
                    item_rect = pygame.Rect(item.button_rect.x + BuildingItem.offset_x, item_y + BuildingItem.offset_y,
                                            item.button_rect.width, item.button_rect.height)

                    if item_rect.collidepoint(mouse_pos) and item.available and mouse_pos[
                        1] < BuildingItem.offset_y + self.background.get_height():
                        if item.button_action(player, self.menu_items):
                            self.background = pygame.transform.scale(
                                pygame.image.load('texture/ui/building/opis_tlo.png').convert_alpha(),
                                (self.menu_width, self.menu_height - 25))
                            ALPHA = 0.85
                            self.background.set_alpha(255 * ALPHA)

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
                    self.menu_top_item_index = int(
                        (thumb_position / max_thumb_position) * (len(self.menu_items) - self.menu_items_per_page))

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
                        self.menu_top_item_index = int(
                            (thumb_position / max_thumb_position) * (len(self.menu_items) - self.menu_items_per_page))


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


        self.button_rect = pygame.Rect(self.itemsurf.get_width() - 110, self.itemsurf.get_height() // 4 - 15, 100, 30)
        self.button_rect2 = pygame.Rect(self.itemsurf.get_width() - 110, self.itemsurf.get_height() // 2 + 15, 100, 30)
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
        self.itemsurf.blit(self.button_image,self.button_rect2)


        self.itemsurf.blit(self.button_text, (self.button_rect.x + 10, self.button_rect.y + 8))

        window.blit(self.itemsurf, (x, y))
    # from main import Game
    # def button_action(self,game:Game):
    def button_action(self,game):


        from gameplay import Player
        self.button_image.fill('#00ff00')
        self.button_text = self.FONT.render("click", True, (255, 255, 255))

        

        with open('gameinfo.bin', 'rb') as f:
            game.size = int(f.readline().decode().rstrip('\n'))
            game.PlayerCount = int(f.readline().decode().rstrip('\n'))
            game.Fog = True if str(f.readline().decode().rstrip('\n')) == 'True' else False
            ID = int(f.readline().decode().rstrip('\n'))
            MAX = int(f.readline().decode().rstrip('\n'))
            castle_hex = eval(f.readline().decode().rstrip('\n'))
            use_castle = eval(f.readline().decode().rstrip('\n'))
        game.allplayers = []
        for _ in range(game.PlayerCount):
            game.allplayers.append(Player('tmp','tmp'))
        with open('playerStats.csv', 'r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Pomijanie pierwszego wiersza z tytułami kolumn
            i = 0 
            for row in reader:
                player_name = row[0]
                home = int(row[1])
                home_x = int(row[2])
                home_y = int(row[3])
                nacja = row[4]
                wyb = True if (row[5]) == 'True' else False
                turn_stop = True if (row[6]) == 'True' else False
                field_status = True if (row[7]) == 'True' else False
                camera_stop = True if (row[8]) == 'True' else False
                player_hex_status = True if (row[9]) == 'True' else False
                atack_stop = True if (row[10]) == 'True' else False
                attack_fail = True if (row[11]) == 'True' else False
                gold_count = int(row[12])
                army_count = int(row[13])
                terrain_count = int(row[14])
                turn_count = int(row[15])
                army_count_bonus = int(row[16])
                gold_count_bonus = int(row[17])
                clay = int(row[18])
                mine_diamonds = int(row[19])
                mine_rocks = int(row[20])
                mine_iron = int(row[21])
                mine_gold = int(row[22])
                fish_port = int(row[23])
                sawmill = int(row[24])
                grain = int(row[25])
                resource_sell_bonus = int(row[26])
                field_bonus = True if (row[27]) == 'True' else False
                building_buy_bonus = int(row[28])
                licznik = int(row[29])
                barbarian_bonus = True if (row[30]) == 'True' else False
                crypt_bonus = True if (row[31]) == 'True' else False
                new_pick = True if (row[32]) == 'True' else False
                game.allplayers[i].set_data(player_name, home, home_x, home_y, nacja, wyb, turn_stop, field_status, camera_stop, player_hex_status,
                     atack_stop, attack_fail, gold_count, army_count, terrain_count, turn_count, army_count_bonus, gold_count_bonus,
                     clay, mine_diamonds, mine_rocks, mine_iron, mine_gold, fish_port, sawmill, grain, resource_sell_bonus,
                     field_bonus, building_buy_bonus, licznik, barbarian_bonus, crypt_bonus, new_pick, MAX, ID,
                use_castle, castle_hex)
                # Wykonaj operacje na odczytanych danych
                # np. przypisz je do obiektów Player, wyświetl, itp.


                
                
        game.map.num_hex_x = game.size
        game.map.num_hex_y = game.size
        game.map.num_hex_all = game.size * game.size
        game.map.num_hex_side = game.map.num_hex_y
        game.map.num_hex_right_side = game.map.num_hex_x
        game.map.all_zajete_surface = {}
        game.map.players = game.allplayers
        for x in range(Player.MAX):
            t = 2
            if game.map.players[x].nacja == "wojownicy":
                t = 0
            if game.map.players[x].nacja == "nomadzi":
                t = 1
            if game.map.players[x].nacja == "kupcy":
                t = 3

            game.map.all_zajete_surface[f'{game.map.players[x].player_name}'] = game.map.zajete[t]
        with open('hexmap.csv', 'r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Pomijanie pierwszego wiersza z tytułami kolumn
            i = 0 
            for row in reader:
                game.map.allhex['hex',i].polozenie_hex_x = int(row[0])
                game.map.allhex['hex',i].polozenie_hex_y = int(row[1])
                game.map.allhex['hex',i].number = int(row[2])
                game.map.allhex['hex',i].obwodka = True if row[3] == 'True' else False
                game.map.allhex['hex',i].zajete = True if row[4] == 'True' else False
                game.map.allhex['hex',i].odkryte = True if row[5] == 'True' else False
                game.map.allhex['hex',i].field_add = True if row[6] == 'True' else False
                game.map.allhex['hex',i].texture_index = int(row[7])
                game.map.allhex['hex',i].rodzaj = row[8]
                game.map.allhex['hex',i].rodzaj_surowca_var = row[9]
                game.map.allhex['hex',i].player = (row[10])  # Odczytanie jako listy, używając funkcji eval()
                game.map.allhex['hex',i].playerable = eval(row[11])  # Odczytanie jako listy, używając funkcji eval()
                game.map.allhex['hex',i].atack = eval(row[12])  # Odczytanie jako listy, używając funkcji eval()
                game.map.allhex['hex',i].texturing(game.map)
                i+=1

        pass
    # from main import Game
    # def button_action2(self,game_data:Game):
    def button_action2(self,game_data):
        
        save_game_data = game_data
        tmp = [game_data.allplayers,
        game_data.allevents,
        game_data.allbuildingmenu]
        # print(tmp)

        with open('gameinfo.bin', 'wb') as f:
            from gameplay import Player
            f.write(str(game_data.size).encode() + b'\n')
            f.write(str(game_data.PlayerCount).encode() + b'\n')
            f.write(str(game_data.Fog).encode() + b'\n')
            f.write(str(Player.ID).encode() + b'\n')
            f.write(str(Player.MAX).encode() + b'\n')
            f.write(str(Player.castle_hex).encode() + b'\n')
            f.write(str(Player.use_castle).encode() + b'\n')

            
        # Save Map
        with open('hexmap.csv', 'w',encoding='utf-8') as f:
            f.write('x;y;number;obwodka;zajete;odkryte;fild_add;textureID;rodzaj;rodzaj_surowca_var;player;playerable;atack\n')
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
                f.write(str(save_game_data.map.allhex['hex',hexagon].player)+';')
                f.write(str(save_game_data.map.allhex['hex',hexagon].playerable)+';')
                f.write(str(save_game_data.map.allhex['hex',hexagon].atack)+';')
                f.write('\n')
        with open('playerStats.csv', 'w',encoding='utf-8') as f:
            f.write('player_name;home;home_x;home_y;nacja;wyb;turn_stop;field_status;camera_stop;player_hex_status;atack_stop;attack_fail;gold_count;army_count;terrain_count;turn_count;army_count_bonus;gold_count_bonus;')
            for surowiec in save_game_data.allplayers[0].surowce_ilosc:
                f.write(str(surowiec[0])+';')
            f.write('resource_sell_bonus;field_bonus;building_buy_bonus;licznik;barbarian_bonus;crypt_bonus;new_pick;')
            f.write('\n')
            for player in save_game_data.allplayers:
                f.write(str(player.player_name)+';')
                f.write(str(player.home)+';')
                f.write(str(player.home_x)+';')
                f.write(str(player.home_y)+';')
                f.write(str(player.nacja)+';')
                f.write(str(player.wyb)+';')
                f.write(str(player.turn_stop)+';')
                f.write(str(player.field_status)+';')
                f.write(str(player.camera_stop)+';')
                f.write(str(player.player_hex_status)+';')
                f.write(str(player.atack_stop)+';')
                f.write(str(player.attack_fail)+';')
                f.write(str(player.gold_count)+';')
                f.write(str(player.army_count)+';')
                f.write(str(player.terrain_count)+';')
                f.write(str(player.turn_count)+';')
                f.write(str(player.army_count_bonus)+';')
                f.write(str(player.gold_count_bonus)+';')
                ######
                for surowiec in player.surowce_ilosc:
                    f.write(str(surowiec[1])+';')

                f.write(str(player.resource_sell_bonus)+';')
                f.write(str(player.field_bonus)+';')
                f.write(str(player.building_buy_bonus)+';')
                f.write(str(player.licznik)+';')
                f.write(str(player.barbarian_bonus)+';')
                f.write(str(player.crypt_bonus)+';')
                f.write(str(player.new_pick)+';')
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
        self.scrollbar_rect = pygame.Rect(0,0,0,0)
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
                    item_rect2 = pygame.Rect(item.button_rect2.x+offset, item_y+item.button_rect.height *2, item.button_rect2.width, item.button_rect2.height)
                    
                    
                    if self.back_rect.collidepoint(mouse_pos):
                        SaveMenu.active = False
                    if item_rect.collidepoint(mouse_pos)and item.available:
                        item.button_action2(game)
                        print('removed')
                    if item_rect2.collidepoint(mouse_pos)and item.available:
                        item.button_action(game)
                        
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



class MenuPause:
    Active = False
    Pause = False
    WHITE = (255, 255, 255)
    TRANSPARENT_WHITE = (0,0,0, 180)
    BLUE = (0, 0, 255)
    def __init__(self,screen:pygame.Surface,w,h) -> None:
        self.menu_width = w
        self.menu_height = h
        # self.menu_x = (SCREEN_WIDTH - self.menu_width) // 2
        # self.menu_y = (SCREEN_HEIGHT - self.menu_height) // 2
        self.screen = screen
        self.selected_option = 0
        self.options = ['TEst','Test22']
        self.overlay = pygame.transform.scale(pygame.image.load('texture/pause_menu/back.png').convert_alpha(),(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.button_resume = pygame.transform.scale_by(pygame.image.load('texture/pause_menu/button_resume.png').convert_alpha(),0.9)
        self.button_wczytaj = pygame.transform.scale_by(pygame.image.load('texture/pause_menu/button_wczytaj.png').convert_alpha(),0.9)
        self.button_zapisz = pygame.transform.scale_by(pygame.image.load('texture/pause_menu/button_zapisz.png').convert_alpha(),0.9)
        self.button_menu = pygame.transform.scale_by(pygame.image.load('texture/pause_menu/button_menu.png').convert_alpha(),0.9)
        
        self.resume_rect = self.button_resume.get_rect(topleft = ((SCREEN_WIDTH-self.button_resume.get_width())/2,(SCREEN_HEIGHT)*0.4))
        self.load_rect = self.button_wczytaj.get_rect(topleft = ((SCREEN_WIDTH-self.button_resume.get_width())/2,self.resume_rect.bottom+SCREEN_HEIGHT*0.02))
        self.save_rect = self.button_zapisz.get_rect(topleft = ((SCREEN_WIDTH-self.button_resume.get_width())/2,self.load_rect.bottom+SCREEN_HEIGHT*0.02))
        self.menu_rect = self.button_menu.get_rect(topleft = ((SCREEN_WIDTH-self.button_resume.get_width())/2,self.save_rect.bottom+SCREEN_HEIGHT*0.02))

        pass
    def draw(self):
        
        if self.Active:
            
            # Obliczanie wymiarów i położenia menu
            
            
            
            # Rysowanie tła z przeźroczystością
            overlay = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill(self.TRANSPARENT_WHITE)
            
            self.screen.blit(overlay, (0,0))
            self.screen.blit(self.overlay, (0,0))
            
            # Rysowanie opcji menu
            self.screen.blit(self.button_resume,self.resume_rect)
            self.screen.blit(self.button_wczytaj,self.load_rect)
            self.screen.blit(self.button_zapisz,self.save_rect)
            self.screen.blit(self.button_menu,self.menu_rect)
    def handle_event(self,event:pygame.event):
        from gameplay import Stats
        pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN:
            if self.menu_rect.collidepoint(pos):
                Menu.status= True
                
                MenuPause.Active = False
                Stats.camera_stop = False
        if event.type == MOUSEBUTTONDOWN:
            if self.resume_rect.collidepoint(pos):
                MenuPause.Active = False
                Stats.camera_stop = False
        if event.type == MOUSEBUTTONDOWN:
            if self.save_rect.collidepoint(pos):
                MenuPause.Active = False
                Stats.camera_stop = False
                SaveMenu.active = True
        pass