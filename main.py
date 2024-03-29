import configparser
import zipfile
from graphics import MapGenerator
from gameplay import *
from menu import *

import pygame
from pygame.locals import *
import sys
import os

# config
config = configparser.ConfigParser()
config.read('settings.ini')
SCREEN_WIDTH = int(config.get('Ustawienia', 'width'))
SCREEN_HEIGHT = int(config.get('Ustawienia', 'height'))
FULLSCREEN_SWITCH = True if config.get('Ustawienia', 'fullscreen') == 'True' else False
MUSIC_VOLUME = int(config.get('Ustawienia', 'volume')) / 100
SOUND_VOLUME = int(config.get('Ustawienia', 'sound')) / 10

clock = pygame.time.Clock()
res = (SCREEN_WIDTH, SCREEN_HEIGHT)
frame_rate = 60
animation_frame_interval = 5
flags = DOUBLEBUF | (pygame.FULLSCREEN if FULLSCREEN_SWITCH else 0)
screen = pygame.display.set_mode(res, flags, 32)
max_tps = 100

folder_path = "save"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

pygame.init()
pygame.display.set_caption("Fields of Fame")
icon_image = pygame.image.load('texture/icon.png')
pygame.display.set_icon(icon_image)

fps_on = True
pygame.mixer.music.load("music/main.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(MUSIC_VOLUME)


def fps():
    if fps_on:
        fps_str = str(int(clock.get_fps()))
        font = pygame.font.Font(None, 30)
        fps_text = font.render(fps_str, True, pygame.Color('red'))
        screen.blit(fps_text, (10, 40))


# class game
class Game:
    def __init__(self):

        pygame.init()
        self.screen = screen
        while not Menu.new_game:
            self.start_menu = Menu(screen, clock, max_tps)  # wyświetlanie i obsługa menu

        self.pause_menu = MenuPause(screen, SCREEN_WIDTH / 4, SCREEN_HEIGHT / 1.5)
        self.okno1 = Okno(500, 300)

        # budynki
        allbuilding1 = [
            BuildingItem("Karczma", "Karczma (+ 10 złota na ture)", 'buddynki_karczma_krita.png', 100, 10, 0),
            BuildingItem("Targowisko", "Targowisko (+20 złota na turę)", 'buddynki_targowisko.png', 300, 20, 0),
            BuildingItem("Bank", "Bank  (+30 złota na turę)", 'buddynki_bank_krita.png', 1000, 100, 0),
            BuildingItem("Szlaki Handlowe", "Szlaki Handlowe  (+50 złota na turę)", 'szlak handlowy.png', 2000, 50, 0),
            BuildingItem("Kowal", "Kowal  (+10 wojska na turę)", 'boddynki_kowal.png', 100, 0, 10),
            BuildingItem("Koszary", "Koszary (+20 wojska na turę)", 'buddynki_koszary_krita.png', 300, 0, 20),
            BuildingItem("Mury", "  (+30 wojska na turę)", 'mury.png', 1000, 0, 30),
            BuildingItem("Twierdza", "Twierdza  (+50 wojska na turę)", 'buddynki_twierdza.png', 2000, 0, 50),

        ]
        allbuilding2 = [
            BuildingItem("Karczma", "Karczma (+ 10 złota na ture)", 'buddynki_karczma_krita.png', 100, 10, 0),
            BuildingItem("Targowisko", "Targowisko (+20 złota na turę)", 'buddynki_targowisko.png', 300, 20, 0),
            BuildingItem("Bank", "Bank  (+30 złota na turę)", 'buddynki_bank_krita.png', 1000, 100, 0),
            BuildingItem("Szlaki Handlowe", "Szlaki Handlowe  (+50 złota na turę)", 'szlak handlowy.png', 2000, 50, 0),
            BuildingItem("Kowal", "Kowal  (+10 wojska na turę)", 'boddynki_kowal.png', 100, 0, 10),
            BuildingItem("Koszary", "Koszary (+20 wojska na turę)", 'buddynki_koszary_krita.png', 300, 0, 20),
            BuildingItem("Mury", "  (+30 wojska na turę)", 'mury.png', 1000, 0, 30),
            BuildingItem("Twierdza", "Twierdza  (+50 wojska na turę)", 'buddynki_twierdza.png', 2000, 0, 50),

        ]
        allbuilding3 = [
            BuildingItem("Karczma", "Karczma (+ 10 złota na ture)", 'buddynki_karczma_krita.png', 100, 10, 0),
            BuildingItem("Targowisko", "Targowisko (+20 złota na turę)", 'buddynki_targowisko.png', 300, 20, 0),
            BuildingItem("Bank", "Bank  (+30 złota na turę)", 'buddynki_bank_krita.png', 1000, 100, 0),
            BuildingItem("Szlaki Handlowe", "Szlaki Handlowe  (+50 złota na turę)", 'szlak handlowy.png', 2000, 50, 0),
            BuildingItem("Kowal", "Kowal  (+10 wojska na turę)", 'boddynki_kowal.png', 100, 0, 10),
            BuildingItem("Koszary", "Koszary (+20 wojska na turę)", 'buddynki_koszary_krita.png', 300, 0, 20),
            BuildingItem("Mury", "  (+30 wojska na turę)", 'mury.png', 1000, 0, 30),
            BuildingItem("Twierdza", "Twierdza  (+50 wojska na turę)", 'buddynki_twierdza.png', 2000, 0, 50),

        ]
        allbuilding4 = [
            BuildingItem("Karczma", "Karczma (+ 10 złota na ture)", 'buddynki_karczma_krita.png', 100, 10, 0),
            BuildingItem("Targowisko", "Targowisko (+20 złota na turę)", 'buddynki_targowisko.png', 300, 20, 0),
            BuildingItem("Bank", "Bank  (+30 złota na turę)", 'buddynki_bank_krita.png', 1000, 100, 0),
            BuildingItem("Szlaki Handlowe", "Szlaki Handlowe  (+50 złota na turę)", 'szlak handlowy.png', 2000, 50, 0),
            BuildingItem("Kowal", "Kowal  (+10 wojska na turę)", 'boddynki_kowal.png', 100, 0, 10),
            BuildingItem("Koszary", "Koszary (+20 wojska na turę)", 'buddynki_koszary_krita.png', 300, 0, 20),
            BuildingItem("Mury", "  (+30 wojska na turę)", 'mury.png', 1000, 0, 30),
            BuildingItem("Twierdza", "Twierdza  (+50 wojska na turę)", 'buddynki_twierdza.png', 2000, 0, 50),

        ]

        self.allbuildingList = [allbuilding1, allbuilding2, allbuilding3, allbuilding4]

        self.size = self.start_menu.MAP_SIZE
        if self.size == 50:
            Player.castle_hex = [356, 325, 392, 1257, 1275, 1292, 2157, 2175, 2192]

        if self.size == 60:
            Player.castle_hex = [1704, 2709, 2683, 704, 307, 269, 704]

        self.Fog = self.start_menu.SWITCH_FOG
        self.PlayerCount = self.start_menu.PLAYER_COUNT

        self.PlayerName = self.start_menu.PLAYER_NAME

        self.PlayerNation = self.start_menu.PLAYER_NATION

        self.camera = Camera()

        self.up_bar = UpBar(screen)
        self.klepsydra1 = Hourglass(screen, frame_rate, animation_frame_interval)

        self.timer = Timer(screen, self)
        self.sd = SideMenu(screen)

        # gracz
        self.allplayers = []

        x = 0
        for name in self.PlayerName:
            player = Player(name, self.PlayerNation[x], self.size)
            self.allplayers.append(player)

            x += 1
        if not self.allplayers:  #
            self.allplayers.append(Player("nazwa", "kupcy", self.size))
            self.allplayers.append(Player("nazwa1", "wojownicy", self.size))
            Player.MAX = 1

        if Menu.SAVE_START:
            with open('save/gameinfo.bin', 'rb') as f:
                size = int(f.readline().decode().rstrip('\n'))
            self.map = MapGenerator(size, size, screen,
                                    self.camera, self.allplayers)
        else:
            self.map = MapGenerator(self.size, self.size, screen,
                                    self.camera, self.allplayers)
        self.start = True
        self.map.texture()
        self.map.generate()
        self.alldec = []

        for i in range(Player.MAX):
            self.alldec.append(Decision(screen, self.map, self.allplayers[i]))

        # definiowanie eventów dla graczy

        for p in range(len(self.allplayers)):

            if p < len(self.alldec):
                self.alldec[p].fupdate.updatefield(self.allplayers[p], self.map.allhex)

        self.allevents = []
        self.allbuildingmenu = []
        for e in range(len(self.allplayers)):
            self.allevents.append(EventMenagment(screen, self.allplayers[e]))
            self.allevents[e].start_event_list()
            if SCREEN_WIDTH == 1366:
                self.allbuildingmenu.append(
                    BuildingMenu(screen, self.allbuildingList[e], screen.get_width() / 2, 500,
                                 int(0.25 * screen.get_width()), int(0.2 * screen.get_height())))
            else:
                self.allbuildingmenu.append(BuildingMenu(screen, self.allbuildingList[e], screen.get_width() / 2,
                                                         SCREEN_HEIGHT * 0.7, int(0.25 * screen.get_width()),
                                                         int(0.2 * screen.get_height())))
            if self.allplayers[e].nacja == "budowniczowie":
                for i in self.allbuildingList[e]:
                    i.cost = i.cost - int(i.cost / 100 * 30)

        self.music_on = 1

        SaveSlot = []
        SaveSlot2 = []
        for i in range(10):
            SaveSlot.append(ItemSave())
        for i in range(10):
            SaveSlot2.append(ItemLoad())

        self.newSaveM = SaveMenu(screen, SaveSlot, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.loadmenu = LoadMenu(screen, SaveSlot2, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.start_menu.SAVE_START

        if self.start_menu.SAVE_START:
            LoadMenu.Save_Select.button_action(self)

        self.currentdec = self.alldec[Player.ID]
        self.currentplayer = self.allplayers[Player.ID]
        self.currentevent = self.allevents[Player.ID]
        self.currentmenu = self.allbuildingmenu[Player.ID]
        self.resource = ResourceSell(screen, self.currentplayer)

    def handle_events(self):
        global fps_on
        POZ = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if MenuPause.Active:
                self.pause_menu.handle_event(event)
            if Okno.active:
                if self.okno1.window_rect.collidepoint(POZ) and event.type == pygame.MOUSEBUTTONDOWN:
                    Okno.active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MenuPause.Active = True
                    BuildingMenu.active = False
                    ResourceSell.active = False
                    self.currentplayer.turn_stop = True

            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                Camera.camera_always_on = not Camera.camera_always_on

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
                fps_on = not fps_on
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if self.music_on == 1:
                    pygame.mixer.music.set_volume(0.0 * MUSIC_VOLUME)
                    self.music_on = 0
                elif self.music_on == 0:
                    pygame.mixer.music.set_volume(1.0 * MUSIC_VOLUME)
                    self.music_on = 1
            if SaveMenu.active:
                self.newSaveM.handle_event(event, self)
            if LoadMenu.active:
                self.loadmenu.handle_event(event, self)
            else:
                if BuildingMenu.active:
                    self.currentmenu.handle_event(event, self.currentplayer)
                if self.sd.button_rect.collidepoint(POZ) and event.type == pygame.MOUSEBUTTONDOWN:
                    if not ResourceSell.active:
                        SOUND.sound_click.play()
                        BuildingMenu.active = not BuildingMenu.active
                        if BuildingMenu.active:
                            Stats.camera_stop = True
                        else:
                            Stats.camera_stop = False
                    pygame.time.Clock().tick(3)
                if ResourceSell.active:
                    if self.sd.button_resource_rect.collidepoint(POZ) and event.type == pygame.MOUSEBUTTONDOWN:
                        SOUND.sound_click.play()
                        ResourceSell.active = False
                    if self.resource.close_button_rect.collidepoint(POZ) and event.type == pygame.MOUSEBUTTONDOWN:
                        ResourceSell.active = False
                else:
                    if self.sd.button_resource_rect.collidepoint(
                            POZ) and event.type == pygame.MOUSEBUTTONDOWN and not BuildingMenu.active:
                        SOUND.sound_click.play()
                        ResourceSell.active = True
        press = pygame.key.get_pressed()

        if press[pygame.K_HOME]:
            Camera.player_camera_update(self.currentplayer)

    def run(self):
        pygame.mixer.music.load("music/music_background/2.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        while True:
            while LoadMenu.active:
                screen.fill((128, 128, 128))
                self.loadmenu.draw_menu()
                self.handle_events()
                pygame.display.flip()
                clock.tick(max_tps)

            while Menu.status:
                self.start_menu.run()

            while MenuSettings.Active:
                self.start_menu.options.draw()

            while SaveMenu.active:
                screen.fill((128, 50, 128))
                self.newSaveM.draw_menu()
                self.handle_events()

                pygame.display.flip()
                clock.tick(max_tps)

            if not Player.start_turn:
                Camera.player_camera_update(self.allplayers[Player.ID])
                Player.start_turn = True
                if self.currentplayer.nacja == "nomadzi":
                    self.currentplayer.field_bonus = True

            self.allindex = {}
            x = 0
            for i in self.allplayers:
                self.allindex[i] = x
                x += 1

            self.currentplayer = self.allplayers[Player.ID]

            self.currentevent = self.allevents[Player.ID]
            self.currentmenu = self.allbuildingmenu[Player.ID]
            self.currentdec = self.alldec[Player.ID]

            screen.fill((0, 0, 0))

            self.handle_events()
            self.camera.mouse(self.size)
            self.camera.keybord(self.size)
            self.map.Draw(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.map.fog_draw(self.Fog, SCREEN_WIDTH, SCREEN_HEIGHT)

            if self.start:
                for i in self.allplayers:
                    i.castle_nation(self.map.allhex)
                self.start = False

            if self.currentplayer.field_status:
                self.currentdec.fchoice.draw()

            self.currentplayer.zajmij_pole(self.map.allrect, self.map.allmask, self.map.allhex, self.currentdec,
                                           screen, self.currentevent, self.map.num_hex_right_side, self.allplayers,
                                           self.alldec, self.allindex)

            self.currentplayer.nomad_bonus(self.currentdec.fchoice)
            self.map.odkryj_pole(self.Fog)
            self.map.colision_detection_obwodka()
            self.map.rysuj_obwodke_i_zajete()
            if Okno.active:
                if Player.MAX == 1:
                    Okno.active = False
                else:
                    self.okno1.draw(screen, self.currentplayer)
            if not Okno.active:
                self.currentevent.random_event()
                self.currentevent.check_result()

            self.up_bar.draw(self.currentplayer)

            self.sd.draw(self.currentplayer)
            if BuildingMenu.active:
                self.currentmenu.draw_menu()
            if not BuildingMenu.active and not ResourceSell.active:
                self.currentdec.click(self.currentplayer)

            self.resource.update_player(self.currentplayer)
            self.resource.draw()
            self.klepsydra1.nation(self.currentplayer)
            self.klepsydra1.draw(self.currentplayer)
            self.map.draw_text_box(self.Fog)

            if not BuildingMenu.active and not ResourceSell.active and not MenuPause.Active:
                if not self.currentplayer.wyb and not self.currentplayer.turn_stop:
                    self.klepsydra1.turn(self.currentplayer)
                if self.currentplayer.wyb and self.currentevent.results == []:
                    self.currentdec.draw(self.currentplayer)
            self.timer.update()
            if MenuPause.Active:
                Stats.camera_stop = True
                self.pause_menu.draw()
                self.currentplayer.turn_stop = False

            fps()
            pygame.display.flip()
            clock.tick(max_tps)


# wykonywanie
if __name__ == '__main__':
    game = Game()
    game.run()
