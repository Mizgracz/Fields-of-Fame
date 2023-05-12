import zipfile
from graphics import Map
from gameplay import*
from menu import Menu, LoadMenu, SaveMenu
import pygame
from pygame.locals import *
import sys
import os

# config
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
clock = pygame.time.Clock()
res = (SCREEN_WIDTH, SCREEN_HEIGHT)
frame_rate = 60
animation_frame_interval = 5
flags = DOUBLEBUF #| pygame.FULLSCREEN
screen = pygame.display.set_mode(res, flags, 32)
max_tps = 6000.0

folder_path = "save"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

pygame.init()
fps_on = True
pygame.mixer.music.load("music/main.mp3")
pygame.mixer.music.play(-1)


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

        self.start_menu = Menu(screen, clock, max_tps)  # wyświetlanie i obsługa menu
        self.size = self.start_menu.MAP_SIZE
        self.Fog = self.start_menu.SWITCH_FOG
        self.PlayerCount = self.start_menu.PLAYER_COUNT
        self.camera = Camera()
        self.map = Map(self.size, self.size, screen, self.camera)
        self.map.texture()
        self.map.generate()
        self.up_bar = UpBar(screen)
        self.klepsydra1 = Hourglass(screen, frame_rate, animation_frame_interval)
        self.dec = Decision(screen)
        self.bm = Build_Menu(screen)
        self.timer = Timer(screen, self)
        self.sd = SideMenu(screen)
        self.event = EventMenagment(screen)
        self.event.start_event_list()


        self.music_on = 1


        self.allItem = [  # Budynki
            BuildItem(self.bm.item_menu_surf, 50, 'wieza', 'Wieża strażniczą (+10 wojska na turę)', 10, 0),
            BuildItem(self.bm.item_menu_surf, 50, 'tartak', 'Farma (+ 10 złota na ture)', 0, 10)]

        self.loadmenu = LoadMenu(screen, self)
        self.savemenu = SaveMenu(screen, self)


    def handle_events(self):
        global fps_on



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
                fps_on = not fps_on
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if self.music_on == 1:
                    pygame.mixer.music.set_volume(0.0)
                    self.music_on = 0

                elif self.music_on == 0:
                    pygame.mixer.music.set_volume(1.0)
                    self.music_on = 1

        press = pygame.key.get_pressed()

        if press[pygame.K_ESCAPE]:
            Menu.status = True
        if press[pygame.K_b]:
            Build_Menu.build_stauts = True
        if press[pygame.K_s]:
            self.save_game()
        if press[pygame.K_HOME]:
            self.camera.camera_x = 0
            self.camera.camera_y = 0

    def save_game(self):
        folder_path = "save"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder {folder_path} został utworzony.")

        with open('save/map.csv', 'w') as savefile:
            savefile.write('x;y;number;texture_index;verticles\n')
            for h in self.map.sprites():
                savefile.write(f'{h.polozenie_hex_x};{h.polozenie_hex_y};{h.number};{h.texture_index}')
                savefile.write('\n')
        with open('save/stats.txt', 'w') as savefile:

            savefile.write(f'gold_count:{Stats.gold_count}\n')
            savefile.write(f'army_count:{Stats.army_count}\n')
            savefile.write(f'player_hex_status:{Stats.player_hex_status}\n')
            savefile.write(f'army_count_bonus:{Stats.army_count_bonus}\n')
            savefile.write(f'gold_count_bonus:{Stats.gold_count_bonus}\n')
            savefile.write(f'turn_count:{Stats.turn_count}\n')
        pygame.time.Clock().tick(1)
        with zipfile.ZipFile("save/QSave.zip", "w") as zip:
            zip.write("save/stats.txt")
            zip.write("save/map.csv")
        os.remove("save/stats.txt")
        os.remove("save/map.csv")
        pass
        import gameplay
        print('LoadGame')
        import csv
        with zipfile.ZipFile("save/QSave.zip", "r") as zip:
            zip.extractall()
        with open('save/map.csv', 'r') as savefile:
            csvfile = csv.reader(savefile, delimiter=';')
            i = -1
            for row in csvfile:
                if i != -1:
                    self.map.allhex["hex", i].polozenie_hex_x = int(row[0])
                    self.map.allhex["hex", i].polozenie_hex_y = int(row[1])
                    self.map.allhex["hex", i].number = int(row[2])
                    self.map.allhex["hex", i].texture_index = int(row[3])
                    self.map.allhex["hex", i].zajete = (row[4])
                    self.map.allhex['hex', i].update_texture()
                i += 1

            pass
        with open('save/stats.txt', 'r') as savefile:
            # csvfile = csv.reader(savefile,delimiter=':')
            stats, col2 = [], []
            for line in savefile:
                stats += [line.strip().split(":")]

            gameplay.build_stauts = bool(stats[0][1])
            gameplay.build = bool(stats[1][1])
            gameplay.gold_count = int(stats[2][1])
            gameplay.army_count = int(stats[3][1])
            gameplay.terrain_count = int(stats[4][1])
            gameplay.wyb = bool(stats[5][1])
            gameplay.player_hex_status = bool(stats[6][1])
            gameplay.army_count_bonus = int(stats[7][1])
            gameplay.gold_count_bonus = int(stats[8][1])
            gameplay.turn_count = int(stats[9][1])

        pygame.time.Clock().tick(1)
        os.remove("save/stats.txt")
        os.remove("save/map.csv")
        pass

    def run(self):

        while True:
            while Menu.status:
                self.start_menu.run()
            while LoadMenu.status:
                self.loadmenu.draw()
                self.loadmenu.update()
            while SaveMenu.status:
                self.savemenu.draw()
                self.savemenu.update()

            screen.fill((255, 255, 255))
            self.handle_events()
            self.camera.mouse(self.size)
            self.camera.keybord()
            self.map.Draw(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.map.fog_draw(self.Fog, SCREEN_WIDTH, SCREEN_HEIGHT)
            Stats.zajmij_pole(Stats,self.map.allrect,self.map.allmask,self.map.allhex) # TODO: zamienić na 
            self.map.odkryj_pole(self.Fog)
            self.map.colision_detection_obwodka()
            self.event.random_event()
            self.map.rysuj_obwodke_i_zajete()



            self.up_bar.draw()
            self.sd.draw()
            self.sd.button()
            if Build_Menu.build_stauts:
                self.bm.draw()
                for item in self.allItem:
                    item.draw()
                    item.buy()
            if not self.bm.build_stauts:
                self.dec.click()

            self.klepsydra1.draw()
            if not Stats.wyb:
                self.klepsydra1.turn()
            if Stats.wyb:
                self.dec.draw()
            self.timer.update()





            fps()



            pygame.display.flip()



            clock.tick(max_tps)


# wykonywanie
if __name__ == '__main__':
    game = Game()
    game.run()
