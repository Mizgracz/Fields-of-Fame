from graphics import Map
from gameplay import Camera, UpBar, Hourglass, Decision, Build_Menu, BuildItem, Timer, SideMenu 
from gameplay import build
from menu import Menu, LoadMenu
import zipfile,os

import pygame
import sys

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Game:
    def __init__(self):
        pygame.init()
        self.status = False
        self.clock = pygame.time.Clock()
        self.res = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.res)
        self.max_tps = 60.0
        self.camera = Camera()
        self.map = Map(30, 30, self.screen, self.camera)
        self.map.generate()
        self.up_bar = UpBar(self.screen)
        self.klepsydra1 = Hourglass(self.screen)
        self.dec = Decision(self.screen)
        self.bm = Build_Menu(self.screen)
        self.timer = Timer(self.res, self.screen, self.screen,self)
        self.startmenu = Menu(self.screen, self.clock, self.max_tps)
        self.lm  =LoadMenu(self.screen,self)
        self.sd = SideMenu(self.screen)
        self.allItem = [
            BuildItem(self.bm.item_menu_surf, 50, 'wieza', 'Wieża strażniczą (+10 wojska na turę)', 10, 0),
            BuildItem(self.bm.item_menu_surf, 50, 'tartak', 'Farma (+ 10 złota na ture)', 0, 10)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        press = pygame.key.get_pressed()

        if press[pygame.K_b]:
            Build_Menu.build_stauts = True
            pygame.time.Clock().tick(3)
        if press[pygame.K_s]:
            self.save_game()
        if press[pygame.K_l]:
            # self.load_game()
            self.lm.status = True
            self.status = False
            self.lm.update()
            self.lm.draw()
        if press[pygame.K_ESCAPE]:
            self.status = False
            self.startmenu.status = True
    def save_game(self):
        import gameplay
        print('SaveGame')

        folder_path = "save"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder {folder_path} został utworzony.")
        else:
            print(f"Folder {folder_path} już istnieje.")

        with open('save/map.csv','w') as savefile:
            savefile.write('x;y;number;texture_index;verticles\n')
            for h in self.map.sprites():
                savefile.write(f'{h.polozenie_hex_x};{h.polozenie_hex_y};{h.number};{h.texture_index};{h.verticles}')
                savefile.write('\n')
        with open('save/stats.txt','w') as savefile:
            
            
            
            savefile.write(f'build_stauts:{gameplay.build_stauts}\n')
            savefile.write(f'build:{gameplay.build}\n')
            savefile.write(f'gold_count:{gameplay.gold_count}\n')
            savefile.write(f'army_count:{gameplay.army_count}\n')
            savefile.write(f'terrain_count:{gameplay.terrain_count}\n')
            savefile.write(f'wyb:{gameplay.wyb}\n')
            savefile.write(f'player_hex_status:{gameplay.player_hex_status}\n')
            savefile.write(f'army_count_bonus:{gameplay.army_count_bonus}\n')
            savefile.write(f'gold_count_bonus:{gameplay.gold_count_bonus}\n')
            savefile.write(f'turn_count:{gameplay.turn_count}\n')
        pygame.time.Clock().tick(1)
        with zipfile.ZipFile("save/QSave.zip", "w") as zip:
            zip.write("save/stats.txt")
            zip.write("save/map.csv")
        os.remove("save/stats.txt")
        os.remove("save/map.csv")
        pass
    def load_game(self):
        import gameplay
        print('LoadGame')
        import csv
        with zipfile.ZipFile("save/QSave.zip", "r") as zip:
            zip.extractall()
        with open('save/map.csv','r') as savefile:
            csvfile = csv.reader(savefile,delimiter=';')
            i = -1
            for row in csvfile:
                if i !=-1:
                    self.map.allhex["hex", i].polozenie_hex_x = int(row[0])
                    self.map.allhex["hex", i].polozenie_hex_y = int(row[1])
                    self.map.allhex["hex", i].number = int(row[2])
                    self.map.allhex["hex", i].texture_index = int(row[3])
                    self.map.allhex["hex", i].verticles = (row[4]) 
                    self.map.allhex['hex',i].update_texture()
                i+=1
            
            pass
        with open('save/stats.txt','r') as savefile:
            # csvfile = csv.reader(savefile,delimiter=':')
            stats,col2 = [],[]
            for line in savefile:
                stats += [line.strip().split(":")]
                
            gameplay.build_stauts = bool(stats[0][1])
            gameplay.build =bool(stats[1][1])
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
            while self.startmenu.status:
                choose = self.startmenu.run()
                
                if choose == 'new_game':
                    self.startmenu.status = False
                    self.status = True
                elif choose == 'load_game':
                    self.lm.status =True
                    self.startmenu.status = False
                    self.status = True
                elif choose == 'save_game':
                    
                    self.startmenu.status = False
                    self.status = True
                elif choose == 'quit':
                    sys.exit(0)
            while self.lm.status:
                self.lm.draw()
                self.handle_events()
            self.handle_events()
            ### NIE DZIAŁA TO ROBIE OBJEJSCIE
            self.status = True
            ####
            while self.status:
                self.sd.button()
                self.screen.fill((255, 255, 255))
                self.handle_events()
                self.camera.mouse()
                self.camera.keybord()
                self.map.draw()
                self.up_bar.score()
                self.dec.draw()
                self.sd.draw()
                if self.bm.build_stauts:
                    self.bm.draw()
                    for item in self.allItem:
                        item.draw()
                        item.buy()
                if not self.bm.build_stauts:
                    self.dec.click()

                self.klepsydra1.draw()
                self.klepsydra1.turn()
                self.timer.update()
                pygame.display.flip()

                self.clock.tick(self.max_tps)


if __name__ == '__main__':
    game = Game()
    game.run()
