import sys, os
import zipfile

import pygame

from gameplay import Stats

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MAP_SIZE = 30
SWITCH_FOG = False
PLAYER_COUNT = 1


class Menu:
    status = True
    resume = False


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
        self.MAP_SIZE = 30
        self.run()


    def handle_events(self):
        self.event = pygame.event.get()
        for event in self.event:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                Menu.status = False
                self.config1.Active = False
                return 'quit'

            elif event.type == pygame.MOUSEBUTTONUP:

                if self.config1.Button_Start_Rect.collidepoint(pos) and self.config1.Active == True:

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


                        return 'resume'
                    else:

                        Menu.resume = True

                        print("new game")
                        return 'new_game'


                elif self.config1.Button_Back_Rect.collidepoint(pos):
                    self.config1.Active = False
                    Menu.resume = False
                    Menu.status = True

                elif self.quit_rect.collidepoint(pos):
                    Menu.status = False
                    return 'quit'

                elif self.load_rect.collidepoint(pos):
                    Menu.status = False
                    print('load')
                    return 'load_game'
                elif self.save_rect.collidepoint(pos) and Menu.resume:
                    Menu.status = False

                    print('save')
                    return 'save_game'

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
            300, 223, 180, 60, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(None, 30),
            ["Mała (30x30)", "Średnia (50x50)", "Duża (60x60)"])
        self.text_fog_on_off = self.font.render("Mgła Wojny : ", True, (255, 255, 255))
        self.fog_on_off = OptionBox(
            700, 223, 180, 60, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(None, 30),
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
