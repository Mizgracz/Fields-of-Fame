import zipfile
from graphics import MapGenerator
from gameplay import*
from menu import *
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
max_tps = 6000

folder_path = "save"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

pygame.init()
fps_on = True
pygame.mixer.music.load("music/main.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0)


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
        self.new_game = False
        while not self.new_game :
            self.start_menu = Menu(screen, clock, max_tps,self.new_game)  # wyświetlanie i obsługa menu
            self.new_game = self.start_menu.new_game

        # budynki
        allbuilding1 = [
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10)
        ]
        allbuilding2 = [
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10)
        ]
        allbuilding3 = [
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10)
        ]
        allbuilding4 = [
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("mlyn","Stary młyn (+ 10 złota na ture)",'mlyn.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'wieza.png',50,10,10),
            BuildingItem("wieza","Wieża strażniczą (+10 wojska na turę)",'mlyn.png',50,10,10)
        ]

        self.allbuildingList = [allbuilding1,allbuilding2,allbuilding3,allbuilding4]
        
        self.size = self.start_menu.MAP_SIZE
        self.Fog = self.start_menu.SWITCH_FOG
        self.PlayerCount = self.start_menu.PLAYER_COUNT

        self.camera = Camera()
        
        self.up_bar = UpBar(screen)
        self.klepsydra1 = Hourglass(screen, frame_rate, animation_frame_interval)

        
        self.timer = Timer(screen, self)
        self.sd = SideMenu(screen)

        # gracz
        self.allplayers = []
        # for dla stworzenia graczy
        self.allplayers.append(Player("Lucyferiusz"))
        self.allplayers.append(Player("Patry"))
        self.allplayers.append(Player("Kacper"))
        self.allplayers.append(Player("Maciej"))

        self.map = MapGenerator(self.size, self.size, screen, self.camera,self.allplayers)

        self.map.texture()
        self.map.generate()
        self.dec = Decision(screen,self.camera,self.map)
        # definiowanie eventów dla graczy

        for p in range(len(self.allplayers)):
            self.dec.fupdate.start(self.allplayers[p])
        
        self.allevents = []
        self.allbuildingmenu =[]
        for e in range(len(self.allplayers)):
            self.allevents.append(EventMenagment(screen,self.allplayers[e]))
            self.allevents[e].start_event_list()
            self.allbuildingmenu.append(BuildingMenu(screen,self.allbuildingList[e],screen.get_width()/2,500,int(0.25*screen.get_width()),int(0.2*screen.get_height())))


        self.currentplayer = self.allplayers[Player.ID]
        self.currentevent = self.allevents[Player.ID]
        self.currentmenu = self.allbuildingmenu[Player.ID]
        


        self.music_on = 1

        self.loadmenu = LoadMenu(screen, self)
        self.savemenu = SaveMenu2(screen, self)

        Buildings = []
        for i in range(30):
            Buildings.append(Item())
        self.newSaveM = SaveMenu(screen,Buildings,SCREEN_WIDTH,SCREEN_HEIGHT)


        
    def handle_events(self):
        global fps_on
        POZ = pygame.mouse.get_pos()
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
        press = pygame.key.get_pressed()
        if press[pygame.K_ESCAPE]:
            Menu.status = True
        if press[pygame.K_s]:
            # self.save_game()
            print(f"{Camera.camera_x } {Camera.camera_y }")
        if press[pygame.K_HOME]:
            Camera.camera_x = self.currentplayer.home_x*(-1)+600
            Camera.camera_y = self.currentplayer.home_y*(-1)+300
            if Camera.camera_x > 1600:
                Camera.camera_x -= (Camera.camera_x-1600)
            print(f"{Camera.camera_x } {Camera.camera_y }")
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
                self.handle_events()
                self.newSaveM.draw_menu()

                pygame.display.flip()
                clock.tick(max_tps)
                
            
            self.currentplayer = self.allplayers[Player.ID]
            self.currentevent = self.allevents[Player.ID]
            self.currentmenu = self.allbuildingmenu[Player.ID]

            screen.fill((255, 255, 255))
            self.handle_events()
            self.camera.mouse(self.size)
            self.camera.keybord(self.size)
            self.map.Draw(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.map.fog_draw(self.Fog, SCREEN_WIDTH, SCREEN_HEIGHT)

            if self.currentplayer.field_status:
                self.dec.fchoice.draw()
            
            self.currentplayer.zajmij_pole(self.map.allrect,self.map.allmask,self.map.allhex,self.dec) 
            self.map.odkryj_pole(self.Fog)
            self.map.colision_detection_obwodka()
            self.currentevent.random_event()
            self.map.rysuj_obwodke_i_zajete()



            self.up_bar.draw(self.currentplayer)
            self.sd.draw(self.currentplayer)
            if BuildingMenu.active:
                self.currentmenu.draw_menu()
            if not BuildingMenu.active:
                self.dec.click(self.currentplayer)

            self.klepsydra1.draw()
            if not BuildingMenu.active:
                if not self.currentplayer.wyb:
                    self.klepsydra1.turn(self.currentplayer)
                if self.currentplayer.wyb:
                    self.dec.draw(self.currentplayer)
            self.timer.update()

            fps()
            pygame.display.flip()
            clock.tick(max_tps)


# wykonywanie
if __name__ == '__main__':
    game = Game()
    game.run()
    
