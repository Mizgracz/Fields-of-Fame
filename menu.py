import sys, os
import zipfile

import pygame
import pygame.mixer

from pygame.locals import * #Potrzebne do klasy Music

from gameplay import Stats

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MAP_SIZE = 30
SWITCH_FOG = False
PLAYER_COUNT = 1


class Menu:
    status = True
    resume = False
    button_sound_save= pygame.mixer.Sound('music/music_ambient/save.mp3')
    button_sound_save.set_volume(1.0)
    button_sound_load = pygame.mixer.Sound('music/music_ambient/load.mp3')
    button_sound_load.set_volume(1.0)

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, max_tps: int,new_game):
        pygame.init()
        self.screen = screen
        self.clock = clock
        self.max_tps = max_tps
        self.new_game = new_game
        Menu.status = True
        Menu.resume = False
        self.font = pygame.font.Font(None, 48)
        self.new_game_rect = pygame.Rect(SCREEN_WIDTH / 2 - 528, SCREEN_HEIGHT / 2 +10 , 255, 55)
        self.load_rect = pygame.Rect(SCREEN_WIDTH / 2 - 528, SCREEN_HEIGHT / 2 + 85, 255, 55)
        self.option_rect = pygame.Rect(SCREEN_WIDTH / 2 - 528, SCREEN_HEIGHT / 2 + 160, 255, 55)
        self.save_rect = pygame.Rect(SCREEN_WIDTH / 2 - 528, SCREEN_HEIGHT / 2 + 120, 255, 55)
        self.quit_rect = pygame.Rect(SCREEN_WIDTH / 2 - 528, SCREEN_HEIGHT / 2 + 235, 255, 55)
        self.background_texture = pygame.transform.smoothscale(pygame.image.load("texture/main_menu/background.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.SWITCH_FOG = SWITCH_FOG
        self.PLAYER_COUNT = 1
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
        self.gameplay = False
        self.config1 = Config(screen)
        music = Music(screen)
        # ambient = Music_ambient(screen)
        self.game_config = Gameconfig(screen, music)
        self.music = music
        # self.ambient = ambient
        self.MAP_SIZE = 30
        self.run()


    def handle_events(self):
        pygame.mixer.init()
        button_sound = pygame.mixer.Sound('music/music_ambient/button_sound.mp3')
        button_sound.set_volume(1.0)
        global SCREEN_WIDTH
        global SCREEN_HEIGHT
        self.event = pygame.event.get()
        for event in self.event:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                Menu.status = False
                self.config1.Active = False
                return 'quit'

            elif event.type == pygame.MOUSEBUTTONUP:

                if self.config1.Button_Start_Rect.collidepoint(pos) and self.config1.Active == True:

                    button_sound.play()
                    self.gameplay = True
                    self.config1.Active = False
                    Menu.status = False
                    self.MAP_SIZE = MAP_SIZE
                    self.SWITCH_FOG = SWITCH_FOG
                    self.PLAYER_COUNT = PLAYER_COUNT
                    self.new_game = True


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

                    button_sound.play()
                    Menu.status = False

                    print('save')
                    return 'save_game'

                elif self.option_rect.collidepoint(pos):
                    button_sound.play()
                    return 'game_options'

                elif self.game_config.Button_Back_Rect_conf.collidepoint(pos):
                    self.game_config.Active = False
                    button_sound.play()

                elif self.game_config.Button_Fullscreen_Rec.collidepoint(pos) and self.game_config.Active == True:
                    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    button_sound.play()

                elif self.game_config.Button_Window_Rec.collidepoint(pos) and self.game_config.Active == True:
                    self.screen = pygame.display.set_mode((1270, 720))
                    SCREEN_WIDTH,SCREEN_HEIGHT = 1270,720
                    button_sound.play()


                elif self.game_config.Button_res1366x768_Rec.collidepoint(pos) and self.game_config.Active == True:
                    self.screen = pygame.display.set_mode((1366, 768))
                    SCREEN_WIDTH, SCREEN_HEIGHT = 1270, 720
                    self.screen.fill('#000000')
                    background_image2 = pygame.image.load("texture/main_menu/gameconf/background.png")
                    background_image2 = pygame.transform.scale(background_image2, (1366, 768))
                    self.screen.blit(background_image2, (0, 0))
                    button_sound.play()

                elif self.game_config.Button_res1600x900_Rec.collidepoint(pos) and self.game_config.Active == True:
                    self.screen = pygame.display.set_mode((1600, 900), pygame.FULLSCREEN)
                    SCREEN_WIDTH, SCREEN_HEIGHT = 1600,900
                    button_sound.play()

                elif self.game_config.Button_res1920x1080_Rec.collidepoint(pos) and self.game_config.Active == True:
                    self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                    SCREEN_WIDTH, SCREEN_HEIGHT = 1920,1080
                    button_sound.play()

                elif self.game_config.Button_res1920x1200_Rec.collidepoint(pos) and self.game_config.Active == True:
                    self.screen = pygame.display.set_mode((1920, 1200), pygame.FULLSCREEN)
                    SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1200
                    button_sound.play()



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
                button_texture = self.resume_game_button_texture
                self.screen.blit(self.save_button_texture, self.save_rect)
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
                SaveMenu.status = True
                Menu.status = False
            if choice == 'game_options':
                self.game_config.Active = True
                while self.game_config.Active:
                    self.game_config.draw(self.event)
                    self.handle_events()
                    self.music.run()
                    # self.ambient.run_ambient()
            elif choice == 'quit':
                sys.exit(0)
            if choice:
                return choice
            self.draw()
            self.clock.tick(self.max_tps)


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


class Config:
    def __init__(self, screen: pygame.surface):
        FONT_NAME = 'timesnewroman'
        self.screen = screen
        self.Button_Back = pygame.image.load("texture/main_menu/config/Button_Back.png")
        self.Button_Start = pygame.image.load("texture/main_menu/config/Button_Start.png")
        self.Background = pygame.image.load("texture/main_menu/config/Background.png")
        self.Button_Back_Rect = self.Button_Back.get_rect(center=(80, 40))
        self.Button_Start_Rect = self.Button_Start.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80))
        self.Active = False
        self.font = pygame.font.Font(None, 36)
        self.text_map_size = self.font.render("Wielkość mapy : ", True, (255, 255, 255))
        self.map_size = OptionBox(
            300, 223, 180, 60, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(FONT_NAME, 30),
            ["Mała (30x30)", "Średnia (50x50)", "Duża (60x60)"])
        self.text_fog_on_off = self.font.render("Mgła Wojny : ", True, (255, 255, 255))
        self.fog_on_off = OptionBox(
            700, 223, 180, 60, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(FONT_NAME, 30),
            ["Wyłącz", "Włącz"])

    def draw(self, event):
        global MAP_SIZE

        self.screen.blit(self.Background, (0, 0))
        self.screen.blit(self.Button_Back, self.Button_Back_Rect)
        self.screen.blit(self.Button_Start, self.Button_Start_Rect)
        self.screen.blit(self.text_map_size, (60, 240))
        self.screen.blit(self.text_fog_on_off, (525, 240))
        self.map_size.draw(self.screen)
        self.fog_on_off.draw(self.screen)
        self.event_list = event
        self.Size()
        self.Switching_Fog()

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

    def Player_count(self):
        pass


#################################################################################################################

class Gameconfig:
    def __init__(self, s2, music):
        self.screen = s2
        self.music_config = music
        self.Button_Back_conf = pygame.image.load("texture/main_menu/gameconf/button_back.png")
        self.Button_Fullscreen = pygame.image.load("texture/main_menu/gameconf/button_fullscreen.png")
        self.background_image = pygame.image.load("texture/main_menu/gameconf/background.png")
        self.Button_Window = pygame.image.load("texture/main_menu/gameconf/button_window.png")
        self.Button_res1366x768= pygame.image.load("texture/main_menu/gameconf/button_res_1366x768.png")
        self.Button_res1600x900= pygame.image.load("texture/main_menu/gameconf/button_res_1600x900.png")
        self.Button_res1920x1080= pygame.image.load("texture/main_menu/gameconf/button_res_1920x1080.png")
        self.Button_res1920x1200= pygame.image.load("texture/main_menu/gameconf/button_res_1920x1200.png")
        self.scale_background = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.Background = self.scale_background
        self.Button_Back_Rect_conf = self.Button_Back_conf.get_rect(center=(170, 60))
        self.Button_Fullscreen_Rec = self.Button_Fullscreen.get_rect(center=(170, 180))
        self.Button_Window_Rec = self.Button_Window.get_rect(center=(480, 180))
        self.Button_res1366x768_Rec = self.Button_res1366x768.get_rect(center=(170, 300))
        self.Button_res1600x900_Rec = self.Button_res1600x900.get_rect(center=(480, 300))
        self.Button_res1920x1080_Rec = self.Button_res1920x1080.get_rect(center=(790, 300))
        self.Button_res1920x1200_Rec = self.Button_res1920x1200.get_rect(center=(1100, 300))
        self.Active = False
        self.font = pygame.font.Font(None, 36)


    def draw(self,event):
        self.screen.blit(self.Background, (0, 0))
        self.screen.blit(self.Button_Back_conf, self.Button_Back_Rect_conf)
        self.screen.blit(self.Button_Fullscreen, self.Button_Fullscreen_Rec)
        self.screen.blit(self.Button_Window, self.Button_Window_Rec)
        self.screen.blit(self.Button_res1366x768, self.Button_res1366x768_Rec)
        self.screen.blit(self.Button_res1600x900, self.Button_res1600x900_Rec)
        self.screen.blit(self.Button_res1920x1080, self.Button_res1920x1080_Rec)
        self.screen.blit(self.Button_res1920x1200, self.Button_res1920x1200_Rec)
        self.music_config.draw_window()
        self.music_config.draw_arrows()
        slider = pygame.Rect(50, 650, 300, 20)
        slider_button_x = 50 + int(300 * self.music_config.volume)
        slider_button_y = 250 + 20 // 2
        slider_button_radius = 10
        self.music_config.draw_slider(slider, slider_button_x, slider_button_y, slider_button_radius)
        self.event_list = event

        pygame.display.update()

class Music:
    def __init__(self, s2):
        pygame.init()
        FONT_NAME = 'timesnewroman'
        self.screen = s2
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONT_NAME, 48)
        self.value = 3
        self.music_playing = False
        self.volume = 0.5  # Początkowa głośność muzyki

    def run(self):
        pygame.mixer.init()
        self.play_music()
        # Slider variables
        slider_width, slider_height = 300, 20
        slider_x, slider_y = 50, 650
        slider = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
        slider_button_radius = 10
        slider_button_x = slider_x + int(slider_width * self.volume)
        slider_button_y = (slider_y + slider_height // 2) - 400
        dragging = False
        arrow_clicked = False

        running = True

        while running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    if self.left_arrow_rect.collidepoint(event.pos):
                        self.change_music('previous')
                        arrow_clicked = True
                    elif self.right_arrow_rect.collidepoint(event.pos):
                        self.change_music('next')
                        arrow_clicked = True
                    elif slider.collidepoint(event.pos):
                        dragging = True
                elif event.type == MOUSEBUTTONUP:
                    if dragging:
                        dragging = False
                    if arrow_clicked:
                        arrow_clicked = False
                elif event.type == MOUSEMOTION:
                    if dragging:
                        slider_button_x = event.pos[0]
                        if slider_button_x < slider_x:
                            slider_button_x = slider_x
                        elif slider_button_x > slider_x + slider_width:
                            slider_button_x = slider_x + slider_width
                        self.volume = ((slider_button_x - slider_x) / slider_width)
                        pygame.mixer.music.set_volume(self.volume)

            # Disable run() if no arrow or slider is clicked
            if not (arrow_clicked or dragging):
                running = False
                continue

            self.draw_window()
            self.draw_arrows()
            self.draw_slider(slider, slider_button_x, slider_button_y, slider_button_radius)
            pygame.display.flip()

    def draw_window(self):
        window_rect = pygame.Rect(100, 500, 200, 100)
        pygame.draw.rect(self.screen, (201, 184, 73), window_rect, 2)

        inner_rect = pygame.Rect(window_rect.left + 2, window_rect.top + 2, window_rect.width - 4, window_rect.height - 4)
        pygame.draw.rect(self.screen, (0, 0, 0), inner_rect)

        text = self.font.render(str(self.value), True, (201, 184, 73))
        text_rect = text.get_rect(center=window_rect.center)
        self.screen.blit(text, text_rect)

    def draw_arrows(self):
        arrow_size = 40
        arrow_thickness = 3

        left_arrow_start = (325, 550)
        left_arrow_end = (left_arrow_start[0] + arrow_size, left_arrow_start[1])
        pygame.draw.line(self.screen, (0, 0, 0), left_arrow_start, left_arrow_end, arrow_thickness)
        pygame.draw.polygon(self.screen, (0, 0, 0), [(left_arrow_end[0] - 10, left_arrow_end[1] - 10),
                                                      (left_arrow_end[0] - 10, left_arrow_end[1] + 10),
                                                      (left_arrow_end[0], left_arrow_end[1])])

        right_arrow_start = (75, 550)
        right_arrow_end = (right_arrow_start[0] - arrow_size, right_arrow_start[1])
        pygame.draw.line(self.screen, (0, 0, 0), right_arrow_start, right_arrow_end, arrow_thickness)
        pygame.draw.polygon(self.screen, (0, 0, 0), [(right_arrow_end[0] + 10, right_arrow_end[1] - 10),
                                                      (right_arrow_end[0] + 10, right_arrow_end[1] + 10),
                                                      (right_arrow_end[0], right_arrow_end[1])])

        self.left_arrow_rect = pygame.Rect(left_arrow_start[0], left_arrow_start[1] - arrow_size // 2,
                                            arrow_size, arrow_size)
        self.right_arrow_rect = pygame.Rect(right_arrow_end[0], right_arrow_end[1] - arrow_size // 2,
                                             arrow_size, arrow_size)

    def draw_slider(self, slider, button_x, button_y, button_radius):
        pygame.draw.rect(self.screen, (201, 184, 73), slider)
        pygame.draw.circle(self.screen, (0, 0, 0), (button_x, button_y + 400), button_radius)

    def change_music(self, direction):
        pygame.mixer.music.stop()
        if direction == 'next':
            self.value -= 1
            if self.value < 1:
                self.value = 5
        elif direction == 'previous':
            self.value += 1
            if self.value > 5:
                self.value = 1
        self.play_music()

    def play_music(self):
        pygame.mixer.music.load('music/music_background/' + str(self.value) + '.mp3')
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)
        self.music_playing = True

# class Music_ambient: Ignorujcie
#     def __init__(self, s2):
#         pygame.init()
#         FONT_NAME = 'timesnewroman'
#         self.screen = s2
#         self.clock = pygame.time.Clock()
#         self.font = pygame.font.SysFont(FONT_NAME, 48)
#         self.value_ambient = 1
#         self.music_playing_ambient = False
#         self.volume_ambient = 1.0  # Initial music volume
#         self.window_rect_ambient = pygame.Rect(700, 500, 200, 100)  # Declare window rectangle
#
#     def run_ambient(self):
#         pygame.mixer.init()
#         # Slider variables
#         slider_width_ambient, slider_height_ambient = 300, 20
#         slider_x_ambient, slider_y_ambient = 650, 650
#         slider_ambient = pygame.Rect(slider_x_ambient, slider_y_ambient, slider_width_ambient, slider_height_ambient)
#         slider_button_radius_ambient = 10
#         slider_button_x_ambient = slider_x_ambient + int(slider_width_ambient * self.volume_ambient)
#         slider_button_y_ambient = slider_y_ambient + slider_height_ambient // 2
#         dragging_ambient = False
#
#         running_ambient = True
#
#         while running_ambient:
#             self.clock.tick(30)
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     pygame.quit()
#                     return
#                 elif event.type == MOUSEBUTTONDOWN:
#                     if slider_ambient.collidepoint(event.pos):
#                         dragging_ambient = True
#                 elif event.type == MOUSEBUTTONUP:
#                     if dragging_ambient:
#                         dragging_ambient = False
#                 elif event.type == MOUSEMOTION:
#                     if dragging_ambient:
#                         slider_button_x_ambient = event.pos[0]
#                         if slider_button_x_ambient < slider_x_ambient:
#                             slider_button_x_ambient = slider_x_ambient
#                         elif slider_button_x_ambient > slider_x_ambient + slider_width_ambient:
#                             slider_button_x_ambient = slider_x_ambient + slider_width_ambient
#                         self.volume_ambient = (slider_button_x_ambient - slider_x_ambient) / slider_width_ambient
#                         self.play_music_ambient()
#
#             if not dragging_ambient:
#                 running_ambient = False
#                 continue
#
#             self.draw_window_ambient()
#             self.draw_slider_ambient(slider_ambient, slider_button_x_ambient, slider_button_y_ambient,
#                                      slider_button_radius_ambient)
#             pygame.display.flip()
#
#     def draw_window_ambient(self):
#         pygame.draw.rect(self.screen, (0, 0, 0), self.window_rect_ambient, 2)
#
#         text = self.font.render("Kliknij mnie", True, (0, 0, 0))
#         text_rect = text.get_rect(center=self.window_rect_ambient.center)
#         self.screen.blit(text, text_rect)
#
#     def draw_slider_ambient(self, slider_ambient, button_x_ambient, button_y_ambient, button_radius_ambient):
#         pygame.draw.rect(self.screen, (128, 128, 128), slider_ambient)
#         pygame.draw.circle(self.screen, (0, 0, 0), (button_x_ambient, button_y_ambient), button_radius_ambient)
#
#     def play_music_ambient(self):
#         pygame.mixer.Sound('music/music_ambient/falling.mp3').play()
#         self.music_playing_ambient = True


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
                Menu.button_sound_load.play()
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

class SaveMenu(object):
    """docstring for SaveMenu"""
    scroll = 0
    status = False

    def __init__(self, screen: pygame.Surface, GAME):
        super(SaveMenu, self).__init__()
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
        SaveItem.ID = 0

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
            self.allItem += [SaveItem(f'{onlyfiles[i]}', self.window)]
        self.allItem += [SaveItem(f'Save{SaveItem.ID + 1}', self.screen)]

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
                SaveMenu.status = False
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
                Menu.button_sound_save.play()
                self.save_game(item.tmpID)
                SaveMenu.status = False
                pygame.time.Clock().tick(3)
        # if self.RECT.collidepoint(pygame.mouse.get_pos()) :

    def save_game(self, index):
        import gameplay
        print('SaveGame')

        folder_path = "save"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open('save/map.csv', 'w') as savefile:
            savefile.write('x;y;number;texture_index;zajete\n')
            for h in self.game.map.sprites():
                savefile.write(f'{h.polozenie_hex_x};{h.polozenie_hex_y};{h.number};{h.texture_index};{h.zajete}')
                savefile.write('\n')
        with open('save/stats.txt', 'w') as savefile:

            savefile.write(f'gold_count:{Stats.gold_count}\n')
            savefile.write(f'army_count:{Stats.army_count}\n')
            savefile.write(f'player_hex_status:{Stats.terrain_count}\n')
            savefile.write(f'army_count_bonus:{Stats.army_count_bonus}\n')
            savefile.write(f'gold_count_bonus:{Stats.gold_count_bonus}\n')
            savefile.write(f'turn_count:{Stats.turn_count}\n')

        pygame.time.Clock().tick(1)
        if self.allItem[index].name[-4:] == '.zip':
            filename = f"save/{self.allItem[index].name}"
        else:
            filename = f"save/{self.allItem[index].name}.zip"
        with zipfile.ZipFile(filename, "w") as zip:
            zip.write("save/stats.txt")
            zip.write("save/map.csv")
        os.remove("save/stats.txt")
        os.remove("save/map.csv")
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


class SaveItem(object):
    ID = 0
    """docstring for Item"""

    def __init__(self, name, screen):
        FONT_SIZE = 25
        FONT_NAME = 'timesnewroman'
        font_text = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        super(SaveItem, self).__init__()
        self.screen = screen
        self.name = name
        self.tmpID = SaveItem.ID
        self.WIDTH = self.screen.get_size()[0] // 2
        self.HEIGHT = 100
        self.item_surface = pygame.image.load('texture/ui/load_menu/opis.png')
        self.item_surface = pygame.transform.scale(self.item_surface, (self.WIDTH, self.HEIGHT))

        self.del_surface = pygame.image.load('texture/ui/load_menu/CheckBoxFalse.png')
        self.del_surface = pygame.transform.scale(self.del_surface, (90, 90))

        self.rect_item = pygame.Rect(self.WIDTH / 2, 150 * self.tmpID + 50 + SaveMenu.scroll, self.WIDTH, 100)
        self.rect_del = pygame.Rect(self.WIDTH / 2 - 5, 150 * self.tmpID + 50 + SaveMenu.scroll + 5, 90, 90)

        self.rect_del.right = self.rect_item.right
        self.rect_item = pygame.Rect(self.WIDTH / 2, 150 * self.tmpID + 50 + SaveMenu.scroll, self.WIDTH - 100, 100)

        self.font_opis = font_text.render((f'{self.tmpID + 1}. {self.name}'), True, (255, 0, 0))

        SaveItem.ID += 1

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
        self.rect_item.top = 150 * self.tmpID + 50 + SaveMenu.scroll
        self.rect_del.top = 150 * self.tmpID + 50 + SaveMenu.scroll + 5
