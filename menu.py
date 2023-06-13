import configparser
import sys, os ,csv,pickle
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

    def hover_player_menu(self,pos,new_game_rect, Button_Back_Rect):

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


        if not Button_Back_Rect.collidepoint(pos):
            SOUND.mouse_over_back = False
            SOUND.option_sound_played = False
        elif not SOUND.mouse_over_back and not SOUND.option_sound_played:
            if not SOUND.button_sound_channel.get_busy():
                SOUND.button_sound_channel.play(SOUND.slide_sound)
                SOUND.option_sound_played = True
            SOUND.mouse_over_back = True
        elif SOUND.mouse_over_back and not Button_Back_Rect.collidepoint(pos):
            SOUND.mouse_over_back = False

    def hover_nation(self,pos,new_game_rect):
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
                    
                    LoadMenu.active = True
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
        
        text = self.font.render(str(self.value), True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

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

        self.warning_repeat = pygame.image.load("texture/main_menu/nation/repeat.png")

        self.warning_no_pick = pygame.image.load("texture/main_menu/nation/no_pick.png")

        self.warning_repeat_active = False
        self.warning_no_pick_active = False
        self.ok_button = pygame.image.load("texture/main_menu/nation/OK.png")
        self.ok_button_HOV = pygame.image.load("texture/main_menu/nation/OK_HOVER.png")
        self.warning_rect = self.warning_no_pick.get_rect()
        self.warning_rect.y = SCREEN_HEIGHT/2.7
        self.warning_rect.x = SCREEN_WIDTH/2

        self.ok_button_rect = self.ok_button.get_rect()
        self.ok_button_rect.midbottom = self.warning_rect.midbottom
        self.ok_button_rect.y -= 20

        self.Background = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/menu_konfiguracji_nacje.png")
                                                       , (self.screen_width,self.screen_height))
        self.Rozpocznij = pygame.image.load("texture/main_menu/nation/Rozpocznij gre.png")
        self.Rozpocznij_HOV = pygame.image.load("texture/main_menu/nation/wybornacji_button_hover.png")
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
        if self.warning_no_pick_active:
            self.screen.blit(self.warning_no_pick,self.warning_rect)
            self.screen.blit(self.ok_button,self.ok_button_rect)
        if self.warning_repeat_active:
            self.screen.blit(self.warning_repeat, self.warning_rect)
            self.screen.blit(self.ok_button, self.ok_button_rect)


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
        pos = pygame.mouse.get_pos()
        SOUND.hover_nation("",pos,self.Rozpocznij_rect)
        if self.Rozpocznij_rect.collidepoint(pos):
            self.screen.blit(self.Rozpocznij_HOV, self.Rozpocznij_rect)
        if self.ok_button_rect.collidepoint(pos) and (self.warning_repeat_active or self.warning_no_pick_active):
            self.screen.blit(self.ok_button_HOV,self.ok_button_rect)
        if self.pick != None and self.pick.nation_pick:
            if self.pick.left_rect.collidepoint(pos):
                self.screen.blit(self.pick.left_HOV, self.pick.left_rect)
            else:
                self.screen.blit(self.pick.left, self.pick.left_rect)


            if self.pick.right_rect.collidepoint(pos):
                self.screen.blit(self.pick.right_HOV, self.pick.right_rect)
            else:

                self.screen.blit(self.pick.right, self.pick.right_rect)

        for event in self.event:

            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if self.Rozpocznij_rect.collidepoint(pos) and NationConfig.Active == True:
                    SOUND.button_sound.play()
                    repeat = False
                    all_pick = True

                    for i in self.select_list:
                        if not i.active:
                            all_pick = False
                            self.warning_no_pick_active = True

                    if all_pick:
                        for i in range(len(self.select_list)-1):
                            if self.select_list[i].selected == self.select_list[i+1].selected:
                                repeat = True
                                self.warning_repeat_active = True

                    if not repeat and all_pick:
                       return "new_game"


                for i in self.select_list:

                    if i.box_rect.collidepoint(pos):
                        SOUND.button_sound.play()
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
                        SOUND.button_sound.play()

                        if self.pick.selected > 0:
                            self.pick.selected -= 1
                        self.pick.nation_pick = True

                if self.pick != None:
                    if self.pick.right_rect.collidepoint(pos):
                        SOUND.button_sound.play()
                        if self.pick.selected < 3:
                            self.pick.selected += 1
                        self.pick.nation_pick = True

                if self.pick != None:
                    if self.pick.opis_box_rect.collidepoint(pos):
                        SOUND.button_sound.play()
                        self.pick.opis_select = 0
                    if self.pick.statystki_box_rect.collidepoint(pos):
                        SOUND.button_sound.play()
                        self.pick.opis_select = 1


                if self.ok_button_rect.collidepoint(pos):
                    SOUND.button_sound.play()
                    self.warning_repeat_active = False
                    self.warning_no_pick_active = False

                if self.warning_repeat_active or self.warning_no_pick_active:
                    for i in self.select_list:
                        i.nation_pick = False

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

        self.right_HOV =  pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/right_HOV.png"),
                                                 (83 / (100 / 75), 374 / (100 / 75)))

        self.left_HOV = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/nation/left_HOV.png"),
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


        
        self.left_rect = self.left.get_rect()
        self.right_rect = self.right.get_rect()
        
        
        self.left_rect.left = SCREEN_WIDTH*0.35
        self.left_rect.y =(SCREEN_HEIGHT-self.left_rect.height)/2

        self.nation_rect = self.merchant.get_rect()
        self.nation_rect.left = self.left_rect.right + self.right_rect.width/8
        self.nation_rect.y = (SCREEN_HEIGHT-self.nation_rect.height)/2

        self.wladcy_rect = self.nation_rect.copy()
        self.wladcy_rect.y -= 80
        self.wladcy_rect.centerx = self.nation_rect.centerx

        self.opis_rect = self.opis.get_rect()
        self.opis_rect.left = self.nation_rect.right + self.right_rect.width/4
        self.opis_rect.y = (SCREEN_HEIGHT-self.opis_rect.height)/2

        self.opis_box_rect = self.opis_box.get_rect()
        self.opis_box_rect.x = self.opis_rect.x
        self.opis_box_rect.y = self.opis_rect.y

        self.opis_text_rect = self.opis_rect.copy()
        self.opis_text_rect.y += self.opis_box_rect.height + 10
        
        self.statystki_box_rect = self.statystki_box.get_rect()
        self.statystki_box_rect.x = self.opis_rect.x + self.opis_box_rect.width
        self.statystki_box_rect.y = self.opis_rect.y
        

        self.right_rect.left = self.opis_rect.right + self.right_rect.width/2
        self.right_rect.y = (SCREEN_HEIGHT-self.right_rect.height)/2
        
        self.active = False

    def draw(self):
       self.screen.blit(self.box_texture, self.box_rect)
       self.screen.blit(self.name, self.name_rect)
       if self.nation_pick:
           self.active = True
           self.box_texture = self.box_color_lists[self.selected]
           self.screen.blit(self.opis, self.opis_rect)

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
        self.Background = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/config/menu_konfiguracji_pseudnimy.png"),(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.Button_Back = pygame.transform.scale_by(pygame.image.load("texture/main_menu/config/wrocdomenu.png"), 0.9)
        self.Button_Start = pygame.transform.scale_by(pygame.image.load("texture/main_menu/config/wybor_nacji.png"), 0.9)
        self.Button_Back_Rect = self.Button_Back.get_rect(
            topleft=(SCREEN_WIDTH * 0.30, SCREEN_HEIGHT - 3 * self.Button_Back.get_height()))
        self.Button_Start_Rect = self.Button_Start.get_rect(
            topleft=(self.Button_Back_Rect.right + 30, self.Button_Back_Rect.y))

        self.Button_Start_HOV = pygame.transform.scale_by(
            pygame.image.load("texture/main_menu/config/wybornacji_button_hover.png"),
            0.9)
        self.Button_Back_HOV = pygame.transform.scale_by(
            pygame.image.load("texture/main_menu/config/wroc_do_menu_button.png"), 0.9)

        self.Active = False
        self.font = pygame.font.Font('fonts/PirataOne-Regular.ttf', 36)
        self.Player_count = Player_count
        self.input_boxes =[]
        for i in range(1,Player_count+1):
            self.input_boxes.append(InputBox(SCREEN_WIDTH*0.46,223+(50*i),250,36))
        self.run()
    def draw(self):

        self.screen.blit(self.Background,(0,0))


        for box in self.input_boxes:
            box.update()
        for box in self.input_boxes:
            box.draw(self.screen)
        pass
    def handle_events(self):
        global PLAYER_NAME
        self.event = pygame.event.get()
        pos = pygame.mouse.get_pos()
        SOUND.hover_player_menu("",pos,self.Button_Start_Rect,self.Button_Back_Rect)
        if self.Button_Start_Rect.collidepoint(pos):
            self.screen.blit(self.Button_Start_HOV, self.Button_Start_Rect)
        else:
            self.screen.blit(self.Button_Start, self.Button_Start_Rect)

        if self.Button_Back_Rect.collidepoint(pos):
            self.screen.blit(self.Button_Back_HOV, self.Button_Back_Rect)
        else:
            self.screen.blit(self.Button_Back, self.Button_Back_Rect)

        for event in self.event:
            for box in self.input_boxes:
                box.handle_event(event)

            if event.type == pygame.QUIT:
                sys.exit()



            elif event.type == pygame.MOUSEBUTTONUP:

                if self.Button_Start_Rect.collidepoint(pos) and PlayerConfig.Active == True:
                    SOUND.button_sound.play()
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
                    SOUND.button_sound.play()
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
        self.Button_Back_HOV =  pygame.transform.scale_by(pygame.image.load("texture/main_menu/config/wroc_do_menu_button.png"),0.9)
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
        if self.Button_Back_Rect.collidepoint(pos):
            self.screen.blit(self.Button_Back_HOV, self.Button_Back_Rect)
        else:
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


        self.music_volume.draw()
        self.sound_volume.draw()

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
        self.fog_button_HOV = pygame.image.load("texture/main_menu/config/mgla_wojny_button.png")

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
            if self.zaznaczone_rect.collidepoint(pos):
                self.screen.blit(self.fog_button_HOV, self.zaznaczone_rect)
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



class BuildingItem:
    itemId = 0
    offset_x = 0
    offset_y = 0
    item_width = 0.47*SCREEN_WIDTH
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
        self.background = pygame.Surface((BuildingItem.item_width, 100 - 2))
        self.background = pygame.transform.smoothscale(pygame.image.load('texture/ui/building/opis.png').convert_alpha(),
                                                 (BuildingItem.item_width, 100 - 2))
        # self.background.fill((128,128,128))
        self.itemsurf = pygame.Surface((BuildingItem.item_width, 100), pygame.SRCALPHA)

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
        BuildingItem.item_width  = menu_width

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



        self.background_upbar = pygame.Surface((menu_width+16, 60), pygame.SRCALPHA)
        self.background_upbar.fill((0, 16, 31))
        self.background_upbar_rect = self.background_upbar.get_rect(topleft=(self.menu_x - 25, self.menu_y - 25-self.background_upbar.get_height()))

        self.close_button = pygame.Surface((60,35))
        self.close_button.fill((200,128,128))

        self.close_button_rect = self.close_button.get_rect()
        self.close_button_rect.top = self.background_upbar_rect.top+(60-35)/2
        self.close_button_rect.right = self.background_upbar_rect.right-50


    def draw_menu(self):

        # Rysowanie menu (inne elementy pominięte dla uproszczenia)
        self.window.blit(self.background, (self.menu_x - 25, self.menu_y - 25))
        self.window.blit(self.background_upbar,self.background_upbar_rect)
        self.window.blit(self.close_button,self.close_button_rect)
        for i, item in enumerate(self.menu_items):
            item_y = 0 + self.scrollbar_margin + (i - self.menu_top_item_index) * (
                        self.menu_item_height + self.item_spacing)
            item_rect = pygame.Rect(25, item_y, self.background.get_width() - 100, self.menu_item_height)
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

                if self.close_button_rect.collidepoint(mouse_pos):
                    BuildingMenu.active = False
                for i, item in enumerate(self.menu_items):
                    item_y = 0 + self.scrollbar_margin + (i - self.menu_top_item_index) * \
                             (self.menu_item_height + self.item_spacing)
                    item_rect = pygame.Rect(item.button_rect.x + BuildingItem.offset_x, item_y + BuildingItem.offset_y,
                                            item.button_rect.width, item.button_rect.height)

                    if item_rect.collidepoint(mouse_pos) and item.available and mouse_pos[
                        1] < BuildingItem.offset_y + self.background.get_height():
                        if item.button_action(player, self.menu_items):
                            self.background = pygame.transform.scale(
                                pygame.image.load('texture/ui/building/budynki_tlo.png').convert_alpha(),
                                (self.menu_width, self.menu_height - 25))
                            ALPHA = 0.85
                            self.background.set_alpha(255 * ALPHA)
                            # Draw the scrollbar thumb
                            pygame.draw.rect(self.window, (255, 170, 20),
                         (self.scrollbar_x, self.thumb_y, self.scrollbar_width, self.thumb_height))

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


class ItemSave:
    itemId = 0
    
    def __init__(self, name:str="",description:str="Zapis gry nr ", image:pygame.Surface=None, cost:int=0):
        self.available = True
        ItemSave.itemId += 1
        self.item_id = ItemSave.itemId
        self.name = name + str(self.item_id)
        self.image = pygame.Surface((90, 90))
        self.image.fill('#ff00ff')

        self.FONT = pygame.font.Font('fonts/PirataOne-Regular.ttf', 24)
        self.cost = random.randint(10,100)
        # self.font_surface = self.FONT.render(f"ID) {self.item_id}", True, (0, 0, 0))
        self.background = pygame.Surface((pygame.display.get_window_size()[0]/2,100-2))
        self.background.fill((128,128,128))
        self.itemsurf = pygame.Surface((pygame.display.get_window_size()[0]/2-2,100),pygame.SRCALPHA)

        self.description = description+str(self.item_id)


        self.remove_rect = pygame.Rect(self.itemsurf.get_width() - 110, self.itemsurf.get_height() // 4 - 15, 100, 30)
        self.load_rect = pygame.Rect(self.itemsurf.get_width() - 110, self.itemsurf.get_height() // 2 + 15, 100, 30)
        self.button_text = self.FONT.render("SAVE", True, (255, 255, 255))
        self.button_text2 = self.FONT.render("REMOVE", True, (255, 255, 255))

        self.image_width = self.image.get_width()
        self.decssurf_width = self.itemsurf.get_width() - self.image_width - self.remove_rect.width-25

        self.decssurf = pygame.Surface((self.decssurf_width, 91), pygame.SRCALPHA)

        self.button_image = pygame.Surface((self.remove_rect.width,self.remove_rect.height),SRCALPHA)
        gameinfo_file = os.path.join('save', f'save_{self.name}.bin')
        if not os.path.exists(gameinfo_file):
            self.button_image.fill('#000000')
        else:
            self.button_image.fill('#00aa90')


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
        gameinfo_file = os.path.join('save', f'save_{self.name}.bin')
        if not os.path.exists(gameinfo_file):
            self.button_image.fill('#000000')
        else:
            self.button_image.fill('#00aa90')

        self.itemsurf.blit(self.background,(1,1))
        self.itemsurf.blit(self.image,(5,5))
        # self.itemsurf.blit(self.font_surface, (self.image.get_width()+9, 7))
        self.itemsurf.blit(self.decssurf,(100,0))
        

        self.itemsurf.blit(self.button_image,self.remove_rect)
        self.itemsurf.blit(self.button_image,self.load_rect)


        self.itemsurf.blit(self.button_text, (self.remove_rect.x + 10, self.remove_rect.y ))
        self.itemsurf.blit(self.button_text2, (self.load_rect.x + 10, self.load_rect.y))

        window.blit(self.itemsurf, (x, y))
    # from main import Game
    # def button_action(self,game:Game):
    def button_action2(self,game_data):
        
        save_game_data = game_data
        tmp = [game_data.allplayers,
        game_data.allevents,
        game_data.allbuildingmenu]
        # print(tmp)

        with open('save/gameinfo.bin', 'wb') as f:
            from gameplay import Player,Camera
            f.write(str(game_data.size).encode() + b'\n')
            f.write(str(game_data.PlayerCount).encode() + b'\n')
            f.write(str(game_data.Fog).encode() + b'\n')
            f.write(str(Player.ID).encode() + b'\n')
            f.write(str(Player.MAX).encode() + b'\n')
            f.write(str(Player.castle_hex).encode() + b'\n')
            f.write(str(Player.use_castle).encode() + b'\n')
            f.write(str(Camera.camera_x).encode() + b'\n')
            f.write(str(Camera.camera_y).encode() + b'\n')
        

        # Save Map
        with open('save/hexmap.csv', 'w',encoding='utf-8') as f:
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
        with open('save/HexRect.csv', 'w',encoding='utf-8') as f:
            f.write('x;y;w;h\n')
            for hexagon in range(len(save_game_data.map.allrect)):
                f.write(str(save_game_data.map.allrect['hex',hexagon].x)+';')
                f.write(str(save_game_data.map.allrect['hex',hexagon].y)+';')
                f.write(str(save_game_data.map.allrect['hex',hexagon].w)+';')
                f.write(str(save_game_data.map.allrect['hex',hexagon].h)+';')
                f.write('\n')
        
        with open('save/playerStats.csv', 'w',encoding='utf-8') as f:
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
        
        import pickle

        # Otwórz pliki wejściowe
        with open('save/gameinfo.bin', 'rb') as file_gameinfo, \
            open('save/playerStats.csv', 'r') as file_playerStats, \
            open('save/HexRect.csv', 'r') as file_HexRect, \
            open('save/hexmap.csv', 'r') as file_hexmap:

            # Wczytaj dane z plików
            gameinfo_data = file_gameinfo.read()
            playerStats_data = file_playerStats.read()
            HexRect_data = file_HexRect.read()
            hexmap_data = file_hexmap.read()

            # Połącz dane w jeden słownik
            data = {
                'gameinfo': gameinfo_data,
                'playerStats': playerStats_data,
                'HexRect': HexRect_data,
                'hexmap': hexmap_data
            }

            # Zapisz dane w pliku binarnym
            with open(f'save/save_{self.name}.bin', 'wb') as file_combined:
                pickle.dump(data, file_combined)

            data = None
            from os import remove

            # Usuń pliki
        remove('save/gameinfo.bin')
        remove('save/playerStats.csv')
        remove('save/HexRect.csv')
        remove('save/hexmap.csv')
    
        pass
    def button_action(self,game):
        
        gameinfo_file = os.path.join('save', f'save_{self.name}.bin')
        if not os.path.exists(gameinfo_file):
            return 0
        
            # Usuń pliki
        os.remove(f'save/save_{self.name}.bin')

    
        pass

class SaveMenu:
    active = False
    def __init__(self, window:pygame.Surface, items:list[ItemSave], menu_width:int, menu_height:int):
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
        self.backtext = pygame.font.Font('fonts/PirataOne-Regular.ttf',30).render("BACK",True,(0,0,0))
        self.scrollbar_rect = pygame.Rect(0,0,0,0)
    def draw_menu(self):
        # Rysowanie menu (inne elementy pominięte dla uproszczenia)
        
        pygame.draw.rect(self.window,(255,255,0),self.back_rect)
        self.window.blit(self.backtext,self.back_rect)
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
                    item_y = item.remove_rect.y + self.scrollbar_margin + (i - self.menu_top_item_index) * \
                        (self.menu_item_height + self.item_spacing)
                    item_rect = pygame.Rect(item.remove_rect.x+offset, item_y, item.remove_rect.width, item.remove_rect.height)
                    item_rect2 = pygame.Rect(item.load_rect.x+offset, item_y+item.remove_rect.height *2, item.load_rect.width, item.load_rect.height)
                    
                    
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

class ItemLoad:
    itemId = 0
    
    def __init__(self, name:str="",description:str="Zapis gry nr ", image:pygame.Surface=None, cost:int=0):
        self.available = True
        ItemLoad.itemId += 1
        self.item_id = ItemLoad.itemId
        self.name = name + str(self.item_id)
        self.image = pygame.Surface((90, 90))
        self.image.fill((255, 170, 20))

        self.FONT = pygame.font.Font('fonts/PirataOne-Regular.ttf', 24)
        self.cost = random.randint(10,100)
        # self.font_surface = self.FONT.render(f"ID) {self.item_id}", True, (0, 0, 0))
        self.background = pygame.Surface((pygame.display.get_window_size()[0]/2.1,100-2))
        self.background.fill((0, 55, 107))
        self.itemsurf = pygame.Surface((pygame.display.get_window_size()[0]/2-2,100),pygame.SRCALPHA)

        self.description = description+str(self.item_id)


        self.remove_rect = pygame.Rect(self.itemsurf.get_width() - 130, (self.itemsurf.get_height()-60) // 2 , 100, 60)
        self.load_rect = pygame.Rect(self.itemsurf.get_width() - 130, (self.itemsurf.get_height()-60) // 2 , 100, 60)
        self.load_rect.right = self.remove_rect.left-30
        self.remove_txt = self.FONT.render("REMOVE", True, (255, 255, 255))
        self.load_txt = self.FONT.render("LOAD", True, (255, 255, 255))

        self.image_width = self.image.get_width()
        self.decssurf_width = self.itemsurf.get_width() - self.image_width - self.remove_rect.width-25

        self.decssurf = pygame.Surface((self.decssurf_width, 91), pygame.SRCALPHA)

        self.button_image = pygame.Surface((self.remove_rect.width,self.remove_rect.height),SRCALPHA)
        gameinfo_file = os.path.join('save', f'save_{self.name}.bin')
        if not os.path.exists(gameinfo_file):
            self.button_image.fill('#000000')
        else:
            self.button_image.fill('#00aa90')


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
        
        gameinfo_file = os.path.join('save', f'save_{self.name}.bin')
        if not os.path.exists(gameinfo_file):
            self.button_image.fill('#000000')
        else:
            self.button_image.fill('#00aa90')
        self.itemsurf.blit(self.background,(1,1))
        self.itemsurf.blit(self.image,(5,5))
        # self.itemsurf.blit(self.font_surface, (self.image.get_width()+9, 7))
        self.itemsurf.blit(self.decssurf,(100,0))
        

        self.itemsurf.blit(self.button_image,self.remove_rect)
        self.itemsurf.blit(self.button_image,self.load_rect)


        self.itemsurf.blit(self.remove_txt, (self.remove_rect.x + 15, self.remove_rect.y+15 ))
        self.itemsurf.blit(self.load_txt, (self.load_rect.x + 30, self.load_rect.y+15))

        window.blit(self.itemsurf, (x, y))
    
    def button_action(self,game):
        import time
        
        gameinfo_file = os.path.join('save', f'save_{self.name}.bin')
        if not os.path.exists(gameinfo_file):
            return 0
        with open(f'save/save_{self.name}.bin', 'rb') as file_combined:
            # Wczytaj dane
            data = pickle.load(file_combined)

        # Odzyskaj dane z słownika
        gameinfo_data = data['gameinfo']
        playerStats_data = data['playerStats']
        HexRect_data = data['HexRect']
        hexmap_data = data['hexmap']

        # Wykonaj odpowiednie operacje na danych...
        with open('save/gameinfo.bin', 'wb') as file_gameinfo:
            file_gameinfo.write(gameinfo_data)

        with open('save/playerStats.csv', 'w') as file_playerStats:
            file_playerStats.write(playerStats_data)

        with open('save/HexRect.csv', 'w') as file_HexRect:
            file_HexRect.write(HexRect_data)

        with open('save/hexmap.csv', 'w') as file_hexmap:
            file_hexmap.write(hexmap_data)

        from gameplay import Player,Camera
        self.button_image.fill('#00aa90')
        
        with open('save/gameinfo.bin', 'rb') as f:
            game.size = int(f.readline().decode().rstrip('\n'))
            game.PlayerCount = int(f.readline().decode().rstrip('\n'))
            game.Fog = True if str(f.readline().decode().rstrip('\n')) == 'True' else False
            ID = int(f.readline().decode().rstrip('\n'))
            MAX = int(f.readline().decode().rstrip('\n'))
            castle_hex = eval(f.readline().decode().rstrip('\n'))
            use_castle = eval(f.readline().decode().rstrip('\n'))
            Camera.camera_x = int(f.readline().decode().rstrip('\n'))
            Camera.camera_y = int(f.readline().decode().rstrip('\n'))
        game.allplayers = []
        time.sleep(1)
        for _ in range(game.PlayerCount):
            game.allplayers.append(Player('tmp','tmp'))
        with open('save/playerStats.csv', 'r',encoding='utf-8') as csvfile:
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
                grain = int(row[24])
                resource_sell_bonus = int(row[25])
                field_bonus = True if (row[26]) == 'True' else False
                building_buy_bonus = int(row[27])
                licznik = int(row[28])
                barbarian_bonus = True if (row[29]) == 'True' else False
                crypt_bonus = True if (row[30]) == 'True' else False
                new_pick = True if (row[31]) == 'True' else False
                game.allplayers[i].set_data(player_name, home, home_x, home_y, nacja, wyb, turn_stop, field_status, camera_stop, player_hex_status,
                     atack_stop, attack_fail, gold_count, army_count, terrain_count, turn_count, army_count_bonus, gold_count_bonus,
                     clay, mine_diamonds, mine_rocks, mine_iron, mine_gold, fish_port, grain, resource_sell_bonus,
                     field_bonus, building_buy_bonus, licznik, barbarian_bonus, crypt_bonus, new_pick, MAX, ID,
                use_castle, castle_hex)
                i+=1
                # Wykonaj operacje na odczytanych danych
                # np. przypisz je do obiektów Player, wyświetl, itp.
                LoadMenu.active = False
        time.sleep(1)
        
                
                
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
        
        
        game.alldec = []
        

        game.allevents = []
        game.allbuildingmenu =[]
        from gameplay import Decision
        for i in range(Player.MAX):
            game.alldec.append(Decision(game.screen,game.map,game.allplayers[i]))
        for p in range(len(game.allplayers)):
            game.alldec[p].fupdate.start(game.allplayers[p])

        from gameplay import EventMenagment
        for e in range(len(game.allplayers)):
            game.allevents.append(EventMenagment(game.screen, game.allplayers[e]))
            game.allevents[e].start_event_list()
            game.allbuildingmenu.append(BuildingMenu(game.screen,game.allbuildingList[e],SCREEN_WIDTH/2,
                                                     500,int(0.25*SCREEN_WIDTH),int(0.2*SCREEN_HEIGHT)))
            if game.allplayers[e].nacja == "kupcy":
                for i in game.allbuildingList[e]:
                    i.cost = i.cost - int(i.cost/100 * 30)

        game.currentplayer = game.allplayers[Player.ID]
        game.currentevent = game.allevents[Player.ID]
        game.currentmenu = game.allbuildingmenu[Player.ID]
        game.currentdec = game.alldec[Player.ID]
        
        # game.map.allhex = {}
        # game.map.allhex['hex',i] =  Hex((polozenie_hex_x), (polozenie_hex_y), i, game.map, False, False,False,False,-1)
        import time
        time.sleep(1)
        gameinfo_file = os.path.join('save', f'save_{self.name}.bin')
        if not os.path.exists(gameinfo_file):
            return 0
        with open(f'save/save_{self.name}.bin', 'rb') as file_combined:
            # Wczytaj dane
            data = pickle.load(file_combined)

        # Odzyskaj dane z słownika
        gameinfo_data = data['gameinfo']
        playerStats_data = data['playerStats']
        HexRect_data = data['HexRect']
        hexmap_data = data['hexmap']

        # Wykonaj odpowiednie operacje na danych...
        with open('save/gameinfo.bin', 'wb') as file_gameinfo:
            file_gameinfo.write(gameinfo_data)

        with open('save/playerStats.csv', 'w') as file_playerStats:
            file_playerStats.write(playerStats_data)

        with open('save/HexRect.csv', 'w') as file_HexRect:
            file_HexRect.write(HexRect_data)

        with open('save/hexmap.csv', 'w') as file_hexmap:
            file_hexmap.write(hexmap_data)

        from gameplay import Player,Camera
        self.button_image.fill('#00aa90')
        
        with open('save/gameinfo.bin', 'rb') as f:
            game.size = int(f.readline().decode().rstrip('\n'))
            game.PlayerCount = int(f.readline().decode().rstrip('\n'))
            game.Fog = True if str(f.readline().decode().rstrip('\n')) == 'True' else False
            ID = int(f.readline().decode().rstrip('\n'))
            MAX = int(f.readline().decode().rstrip('\n'))
            castle_hex = eval(f.readline().decode().rstrip('\n'))
            use_castle = eval(f.readline().decode().rstrip('\n'))
            Camera.camera_x = int(f.readline().decode().rstrip('\n'))
            Camera.camera_y = int(f.readline().decode().rstrip('\n'))
        game.allplayers = []
        time.sleep(1)
        for _ in range(game.PlayerCount):
            game.allplayers.append(Player('tmp','tmp'))
        with open('save/playerStats.csv', 'r',encoding='utf-8') as csvfile:
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
                
                grain = int(row[24])
                resource_sell_bonus = int(row[25])
                field_bonus = True if (row[26]) == 'True' else False
                building_buy_bonus = int(row[27])
                licznik = int(row[28])
                barbarian_bonus = True if (row[29]) == 'True' else False
                crypt_bonus = True if (row[30]) == 'True' else False
                new_pick = True if (row[30]) == 'True' else False
                game.allplayers[i].set_data(player_name, home, home_x, home_y, nacja, wyb, turn_stop, field_status, camera_stop, player_hex_status,
                     atack_stop, attack_fail, gold_count, army_count, terrain_count, turn_count, army_count_bonus, gold_count_bonus,
                     clay, mine_diamonds, mine_rocks, mine_iron, mine_gold, fish_port, grain, resource_sell_bonus,
                     field_bonus, building_buy_bonus, licznik, barbarian_bonus, crypt_bonus, new_pick, MAX, ID,
                use_castle, castle_hex)
                i+=1
                # Wykonaj operacje na odczytanych danych
                # np. przypisz je do obiektów Player, wyświetl, itp.

        time.sleep(1)
                
                
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
        
        
        game.alldec = []
        

        game.allevents = []
        game.allbuildingmenu =[]
        from gameplay import Decision
        for i in range(Player.MAX):
            game.alldec.append(Decision(game.screen,game.map,game.allplayers[i]))
        for p in range(len(game.allplayers)):
            game.alldec[p].fupdate.start(game.allplayers[p])

        from gameplay import EventMenagment
        for e in range(len(game.allplayers)):
            game.allevents.append(EventMenagment(game.screen, game.allplayers[e]))
            game.allevents[e].start_event_list()
            game.allbuildingmenu.append(BuildingMenu(game.screen,game.allbuildingList[e],SCREEN_WIDTH/2,
                                                     500,int(0.25*SCREEN_WIDTH),int(0.2*SCREEN_HEIGHT)))
            if game.allplayers[e].nacja == "kupcy":
                for i in game.allbuildingList[e]:
                    i.cost = i.cost - int(i.cost/100 * 30)

        game.currentplayer = game.allplayers[Player.ID]
        game.currentevent = game.allevents[Player.ID]
        game.currentmenu = game.allbuildingmenu[Player.ID]
        game.currentdec = game.alldec[Player.ID]
        
        # game.map.allhex = {}
        # game.map.allhex['hex',i] =  Hex((polozenie_hex_x), (polozenie_hex_y), i, game.map, False, False,False,False,-1)
        from graphics import Hex
        with open('save/hexmap.csv', 'r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Pomijanie pierwszego wiersza z tytułami kolumn
            i = 0 
            for row in reader:
                polozenie_hex_x= int(row[0])
                polozenie_hex_y= int(row[1])
                number= int(row[2])
                obwodka = True if row[3] == 'True' else False
                zajete = True if row[4] == 'True' else False
                odkryte  = True if row[5] == 'True' else False
                field_add   = True if row[6] == 'True' else False
                texture_index = int(row[7])
                rodzaj= row[8]
                rodzaj_surowca_var = row[9]
                player= (row[10])  # Odczytanie jako listy, używając funkcji eval()
                playerable = eval(row[11])  # Odczytanie jako listy, używając funkcji eval()
                atack = eval(row[12])  # Odczytanie jako listy, używając funkcji eval()
                
                game.map.allhex['hex',i].data_update(polozenie_hex_x,polozenie_hex_y,number,
                    obwodka,zajete,odkryte,field_add,texture_index,
                    rodzaj,rodzaj_surowca_var,player,playerable,
                    atack)
                i+=1
        time.sleep(1)
        # ###########
        
        with open('save/HexRect.csv', 'r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Pomijanie pierwszego wiersza z tytułami kolumn
            i = 0 
            for row in reader:
                x= int(row[0])
                y= int(row[1])
                w= int(row[2])
                h= int(row[3])
                game.map.set_allrect(i,x,y,w,h)
                i+=1
        time.sleep(1)

        os.remove('save/gameinfo.bin')
        os.remove('save/hexmap.csv')
        os.remove('save/HexRect.csv')
        os.remove('save/playerStats.csv')
        

        pass

    def button_action2(self):
        gameinfo_file = os.path.join('save', f'save_{self.name}.bin')
        if not os.path.exists(gameinfo_file):
            return 0
        os.remove(f'save/save_{self.name}.bin')
        pass

class LoadMenu:
    active = False

    def __init__(self, window: pygame.Surface, items: list[ItemLoad], menu_width: int, menu_height: int):
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

        self.menu_items_per_page = (self.menu_height - self.scrollbar_margin * 2) // (
                    self.menu_item_height + self.item_spacing)
        self.menu_x = 0  # Set the desired x-coordinate of the menu
        self.menu_y = 0  # Set the desired y-coordinate of the menu

        self.back_rect = pygame.Rect(self.scrollbar_x - 200, 50, 150, 50)
        self.backtext = pygame.font.Font('fonts/PirataOne-Regular.ttf', 30).render("BACK", True, (0, 0, 0))
        self.scrollbar_rect = pygame.Rect(255, 0, 255, 0)

        # Load the images
        self.left_side_art = pygame.image.load('texture/ui/load_menu/heroine_left.png')
        self.left_side_art = pygame.transform.scale(self.left_side_art, (350, 720))
        self.right_side_art = pygame.image.load('texture/ui/load_menu/warior_right.png')
        self.right_side_art = pygame.transform.scale(self.right_side_art, (350, 720))

        # Set the initial position of the side art
        self.left_side_rect = self.left_side_art.get_rect(topleft=(self.window.get_width() - 1320, 0))
        self.right_side_rect = self.right_side_art.get_rect(topleft=(self.window.get_width() - 350, 0))

    def draw_menu(self):
        self.window.fill((0, 16, 31))  # Ustawia kolor tła na czarny (RGB: 0, 0, 0)
        # Draw the left side art
        self.window.blit(self.left_side_art, self.left_side_rect)

        # Draw the right side art
        self.window.blit(self.right_side_art, self.right_side_rect)

        # Draw the rest of the menu (omitted for simplicity)
        pygame.draw.rect(self.window, (255, 170, 20), self.back_rect)
        self.window.blit(self.backtext, self.back_rect)
        for i, item in enumerate(self.menu_items):
            item_y = self.menu_y + self.scrollbar_margin + (i - self.menu_top_item_index) * (
                    self.menu_item_height + self.item_spacing)
            item_rect = pygame.Rect(self.menu_width / 4, item_y, self.menu_width / 2.1, self.menu_item_height)
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                # Zaznaczony przedmiot
                pygame.draw.rect(self.window, (192, 192, 255), item_rect)
            pygame.draw.rect(self.window, (255, 170, 20), item_rect, 1)

            item.draw(self.window, item_rect.x, item_y)

        # Scrollbar
        pygame.draw.rect(self.window, (0, 28, 56),
                         (self.scrollbar_x, self.scrollbar_y, self.scrollbar_width, self.scrollbar_height))
        self.scrollbar_rect = pygame.Rect(self.scrollbar_x, self.scrollbar_y, self.scrollbar_width,
                                           self.scrollbar_height)
        # Calculate the position and height of the scrollbar thumb
        self.thumb_height = self.scrollbar_height / len(self.menu_items) * self.menu_items_per_page
        self.thumb_y = self.scrollbar_y + (self.menu_top_item_index / len(self.menu_items)) * self.scrollbar_height

        # Draw the scrollbar thumb
        pygame.draw.rect(self.window, (255, 170, 20), (self.scrollbar_x, self.thumb_y, self.scrollbar_width,
                                                       self.thumb_height))

    def handle_event(self, event, game):
        offset = self.menu_width / 4
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Kliknięcie lewym przyciskiem myszy
                mouse_pos = pygame.mouse.get_pos()
                for i, item in enumerate(self.menu_items):
                    item_y = item.remove_rect.y + self.scrollbar_margin + (i - self.menu_top_item_index) * (
                            self.menu_item_height + self.item_spacing)
                    item_rect = pygame.Rect(item.remove_rect.x + offset, item_y, item.remove_rect.width,
                                            item.remove_rect.height)
                    item_rect2 = pygame.Rect(item.load_rect.x + offset, item_y, item.load_rect.width,
                                             item.load_rect.height)

                    if self.back_rect.collidepoint(mouse_pos):
                        LoadMenu.active = False
                    if item_rect.collidepoint(mouse_pos) and item.available:
                        item.button_action2()

                    if item_rect2.collidepoint(mouse_pos) and item.available:
                        print(item.name)
                        self.window.fill('#000000')
                        item.button_action(game)
                        pygame.time.Clock().tick(2)

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
                    self.menu_top_item_index = int((thumb_position / max_thumb_position) * (
                            len(self.menu_items) - self.menu_items_per_page))

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
                        self.menu_top_item_index = int((thumb_position / max_thumb_position) * (
                                len(self.menu_items) - self.menu_items_per_page))





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
        
        if event.type == MOUSEBUTTONDOWN:
            if self.load_rect.collidepoint(pos):
                MenuPause.Active = False
                Stats.camera_stop = False
                LoadMenu.active = True
        pass