import configparser
import zipfile
from graphics import MapGenerator
from gameplay import*
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
FULLSCREEN_SWITCH = True if config.get('Ustawienia','fullscreen') == 'True' else False
MUSIC_VOLUME = int(config.get('Ustawienia','volume'))/100
SOUND_VOLUME = int(config.get('Ustawienia','sound'))/100


clock = pygame.time.Clock()
res = (SCREEN_WIDTH, SCREEN_HEIGHT)
frame_rate = 60
animation_frame_interval = 5
flags = DOUBLEBUF | (pygame.FULLSCREEN if FULLSCREEN_SWITCH else 0)
screen = pygame.display.set_mode(res, flags, 32)
max_tps = 6000

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
        while not Menu.new_game :
            self.start_menu = Menu(screen, clock, max_tps)  # wyświetlanie i obsługa menu
        
        self.pause_menu = MenuPause(screen,SCREEN_WIDTH/4,SCREEN_HEIGHT/1.5)
        self.okno1 = Okno(500,300)

        # budynki
        allbuilding1 = [
            BuildingItem("Targowisko","Targowisko (+20 złota na turę)",'buddynki_targowisko.png',300,20,0),
            BuildingItem("Karczma","Karczma (+ 10 złota na ture)",'buddynki_karczma_krita.png',100,10,0),
            BuildingItem("Koszary","Koszary (+20 wojska na turę)",'buddynki_koszary_krita.png',300,0,20),
            BuildingItem("Kowal","Kowal  (+10 wojska na turę)",'boddynki_kowal.png',100,10,0),
            BuildingItem("Bank", "Bank  (+100 złota na turę)", 'buddynki_bank_krita.png', 1000, 100, 0),
            BuildingItem("Bank", "TEST 101  (+100000 złota na turę)", 'buddynki_bank_krita.png', 1000, 100, 0),
        ]
        allbuilding2 = [
            BuildingItem("Targowisko", "Targowisko (+20 złota na turę)", 'buddynki_targowisko.png', 300, 20, 0),
            BuildingItem("Karczma", "Karczma (+ 10 złota na ture)", 'buddynki_karczma_krita.png', 100, 10, 0),
            BuildingItem("Koszary", "Koszary (+20 wojska na turę)", 'buddynki_koszary_krita.png', 300, 0, 20),
            BuildingItem("Kowal", "Kowal  (+10 wojska na turę)", 'boddynki_kowal.png', 100, 10, 0),
            BuildingItem("Bank", "Bank  (+100 złota na turę)", 'buddynki_bank_krita.png', 1000, 100, 0),
        ]
        allbuilding3 = [
            BuildingItem("Targowisko", "Targowisko (+20 złota na turę)", 'buddynki_targowisko.png', 300, 20, 0),
            BuildingItem("Karczma", "Karczma (+ 10 złota na ture)", 'buddynki_karczma_krita.png', 100, 10, 0),
            BuildingItem("Koszary", "Koszary (+20 wojska na turę)", 'buddynki_koszary_krita.png', 300, 0, 20),
            BuildingItem("Kowal", "Kowal  (+10 wojska na turę)", 'boddynki_kowal.png', 100, 10, 0),
            BuildingItem("Bank", "Bank  (+100 złota na turę)", 'buddynki_bank_krita.png', 1000, 100, 0),
        ]
        allbuilding4 = [
            BuildingItem("Targowisko", "Targowisko (+20 złota na turę)", 'buddynki_targowisko.png', 300, 20, 0),
            BuildingItem("Karczma", "Karczma (+ 10 złota na ture)", 'buddynki_karczma_krita.png', 100, 10, 0),
            BuildingItem("Koszary", "Koszary (+20 wojska na turę)", 'buddynki_koszary_krita.png', 300, 0, 20),
            BuildingItem("Kowal", "Kowal  (+10 wojska na turę)", 'boddynki_kowal.png', 100, 10, 0),
            BuildingItem("Bank", "Bank  (+100 złota na turę)", 'buddynki_bank_krita.png', 1000, 100, 0),
        ]

        self.allbuildingList = [allbuilding1, allbuilding2, allbuilding3, allbuilding4]

        self.size = self.start_menu.MAP_SIZE
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

            self.allplayers.append(Player(name,self.PlayerNation[x]))
            x += 1

        self.map = MapGenerator(self.size, self.size, screen,\
                                 self.camera,self.allplayers)
        #
        #
        self.start = True
        self.map.texture()
        self.map.generate()
        self.alldec = []



        for i in range(Player.MAX):
            self.alldec.append(Decision(screen,self.map,self.allplayers[i]))

        # definiowanie eventów dla graczy

        for p in range(len(self.allplayers)):
            self.alldec[p].fupdate.start(self.allplayers[p])

        self.allevents = []
        self.allbuildingmenu =[]
        for e in range(len(self.allplayers)):
            self.allevents.append(EventMenagment(screen, self.allplayers[e]))
            self.allevents[e].start_event_list()
            self.allbuildingmenu.append(BuildingMenu(screen,self.allbuildingList[e],screen.get_width()/2,500,int(0.25*screen.get_width()),int(0.2*screen.get_height())))
            if self.allplayers[e].nacja == "kupcy":
                for i in self.allbuildingList[e]:
                    i.cost = i.cost - int(i.cost/100 * 30)


        self.currentplayer = self.allplayers[Player.ID]
        self.currentevent = self.allevents[Player.ID]
        self.currentmenu = self.allbuildingmenu[Player.ID]
        self.currentdec = self.alldec[Player.ID]


        self.music_on = 1
        self.resource = ResourceSell(screen,self.currentplayer)
        self.loadmenu = LoadMenu(screen, self)

        Buildings = []
        for i in range(30):
            Buildings.append(Item())
        self.newSaveM = SaveMenu(screen,Buildings,SCREEN_WIDTH,SCREEN_HEIGHT)



    def handle_events(self):
        global fps_on
        POZ = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if MenuPause.Active ==True:
                self.pause_menu.handle_event(event)
            if Okno.active:
                if self.okno1.window_rect.collidepoint(POZ) and event.type == pygame.MOUSEBUTTONDOWN:
                    Okno.active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MenuPause.Active = True
                    BuildingMenu.active = False
                    ResourceSell.active = False
                    
            if event.type == pygame.QUIT:
                    sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                Camera.camera_always_on = not Camera.camera_always_on

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
                    fps_on = not fps_on
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if self.music_on == 1:
                    pygame.mixer.music.set_volume(0.0*MUSIC_VOLUME)
                    self.music_on = 0
                elif self.music_on == 0:
                    pygame.mixer.music.set_volume(1.0*MUSIC_VOLUME)
                    self.music_on = 1
            if SaveMenu.active:
                self.newSaveM.handle_event(event,self)
            else:
                if BuildingMenu.active:
                    self.currentmenu.handle_event(event,self.currentplayer)
                if self.sd.button_rect.collidepoint(POZ) and event.type == pygame.MOUSEBUTTONDOWN:
                    BuildingMenu.active = not BuildingMenu.active
                    if BuildingMenu.active:
                        Stats.camera_stop = True
                    else:
                        Stats.camera_stop = False
                    pygame.time.Clock().tick(3)
                if ResourceSell.active == True:
                    if self.sd.button_resource_rect.collidepoint(POZ) and event.type == pygame.MOUSEBUTTONDOWN:
                        ResourceSell.active = False
                else:
                    if self.sd.button_resource_rect.collidepoint(POZ) and event.type == pygame.MOUSEBUTTONDOWN:
                        ResourceSell.active = True
        press = pygame.key.get_pressed()
        
        if press[pygame.K_s]:
            # self.save_game()
            print(f"{Camera.camera_x } {Camera.camera_y }")
        if press[pygame.K_HOME]:
            Camera.player_camera_update(self.currentplayer)



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
            while SaveMenu.active:
                screen.fill((128, 0, 0))
                self.newSaveM.draw_menu()
                self.handle_events()

                pygame.display.flip()
                clock.tick(max_tps)
            if not Player.start_turn:
                Camera.player_camera_update(self.allplayers[Player.ID])
                Player.start_turn = True
                if self.currentplayer.nacja == "nomadzi":
                    self.currentplayer.field_bonus = True

            self.currentplayer = self.allplayers[Player.ID]
            self.currentevent = self.allevents[Player.ID]
            self.currentmenu = self.allbuildingmenu[Player.ID]
            self.currentdec = self.alldec[Player.ID]
            screen.fill((255, 255, 255))

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

            self.currentplayer.zajmij_pole(self.map.allrect,self.map.allmask,self.map.allhex,self.currentdec,screen,self.currentevent,self.map.num_hex_right_side,self.allplayers)
            self.currentplayer.nomad_bonus(self.currentdec.fchoice)
            self.map.odkryj_pole(self.Fog)
            self.map.colision_detection_obwodka()
            self.currentevent.random_event()
            self.map.rysuj_obwodke_i_zajete()

            self.currentevent.check_result()


            self.up_bar.draw(self.currentplayer)
            self.sd.draw(self.currentplayer)
            if BuildingMenu.active:
                self.currentmenu.draw_menu()
            if not BuildingMenu.active:
                self.currentdec.click(self.currentplayer)

            self.resource.update_player(self.currentplayer)
            self.resource.draw()
            self.klepsydra1.nation(self.currentplayer)
            self.klepsydra1.draw(self.currentplayer)
            self.map.draw_text_box(self.Fog)

            if not BuildingMenu.active and not ResourceSell.active and not MenuPause.Active:
                if not self.currentplayer.wyb:
                    self.klepsydra1.turn(self.currentplayer)
                if self.currentplayer.wyb and self.currentevent.results == []:
                    self.currentdec.draw(self.currentplayer)
            self.timer.update()
            if MenuPause.Active:
                Stats.camera_stop = True
                self.pause_menu.draw()
            if Okno.active:
                self.okno1.draw(screen,self.currentplayer)
            fps()
            pygame.display.flip()
            clock.tick(max_tps)


# wykonywanie
if __name__ == '__main__':
    game = Game()
    game.run()

