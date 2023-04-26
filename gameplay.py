import zipfile
import pygame
import time,os


camera_stop = False
item_offset = pygame.Vector2(0, 115)


class Stats:
    
    gold_count = 0
    army_count = 0
    terrain_count = 1
    turn_count = 1
    wyb = False
    camera_stop = False
    item_offset = pygame.Vector2(0, 115)
    player_hex_status = False
    army_count_bonus = 0
    gold_count_bonus = 0
    surowce_ilosc = [["clay", 0, "glina: "], ["mine_diamonds", 0, "diamenty: "], ["mine_rocks", 0, "kamień: "], ["mine_iron", 0, "żelazo: "], ["mine_gold", 0, "złoto: "], ["fish_port", 0, "ryby: "], ["sawmill", 0, "drewno: "], ["grain", 0, "zboże: "]]
    def __init__(self) -> None:
        pass

def dopisz_surowiec(surowiec):
    for i in range(len(Stats.surowce_ilosc)):
        if surowiec == Stats.surowce_ilosc[i][0]:
            Stats.surowce_ilosc[i][1] += 100

class Camera:

    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0

        self.mouse_x = 0
        self.mouse_y = 0
        self.move_mouse_max = 160


    def mouse(self,mapsize):

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        predkosc = 5
        press = pygame.key.get_pressed()
        if camera_stop is False:
            if not press[pygame.K_LCTRL]:
                if self.camera_x < 1600:
                    if self.mouse_x < 30:
                        self.camera_x += (predkosc + 10)
                    elif self.mouse_x < 80:
                        self.camera_x += (predkosc + 5)
                    elif self.mouse_x < self.move_mouse_max:
                        self.camera_x += predkosc
                if self.camera_x > 1640 - (mapsize * 130)+1110:
                    if self.mouse_x > 1240:
                        self.camera_x -= predkosc + 10
                    elif self.mouse_x > 1190:
                        self.camera_x -= predkosc + 5
                    elif self.mouse_x > 1110:
                        self.camera_x -= predkosc

                if self.camera_y < - 20:
                    if self.mouse_y < 30:
                        self.camera_y += predkosc + 10
                    elif self.mouse_y < 80:
                        self.camera_y += predkosc + 5
                    elif self.mouse_y < 160:
                        self.camera_y += predkosc

                if self.camera_y > (-152*mapsize/2) - (75*mapsize/2) + 825:
                    if self.mouse_y > 670:
                        self.camera_y -= predkosc + 10
                    elif self.mouse_y > 620:
                        self.camera_y -= predkosc + 5
                    elif self.mouse_y > 540:
                        self.camera_y -= predkosc

    def keybord(self):
        press = pygame.key.get_pressed()
        if press[pygame.K_RIGHT]:
            self.camera_x -= 5
        if press[pygame.K_LEFT]:
            self.camera_x += 5
        if press[pygame.K_DOWN]:
            self.camera_y -= 5
        if press[pygame.K_UP]:
            self.camera_y += 5


class UpBar:

    def __init__(self, screen):
        #SCREEN#
        self.SCREEN_WIDTH = screen.get_size()[0]
        self.SCREEN_HEIGHT = screen.get_size()[1]
        ########
        FONT_NAME = 'timesnewroman'
        FONT_SIZE = 17
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        ########
        self.bar = pygame.Surface((self.SCREEN_WIDTH, 30))
        self.up_bar_surface = pygame.Surface((self.SCREEN_WIDTH, 30))
        # grafiki
        self.bar_main = pygame.image.load('texture/ui/up_bar/bar.png').convert_alpha()
        self.bar_gold = pygame.image.load('texture/ui/up_bar/bar_zloto.png').convert_alpha()
        self.bar_army = pygame.image.load('texture/ui/up_bar/bar_wojsko.png').convert_alpha()
        self.bar_field = pygame.image.load('texture/ui/up_bar/bar_pola.png').convert_alpha()

        self.screen = screen

        self.up_bar_surface.blit(self.bar_main, (0, 0))

        self.up_bar_surface.blit(self.bar_gold, (10, 2))
        self.up_bar_surface.blit(self.bar_army, (200, 2))
        self.up_bar_surface.blit(self.bar_field, (390, 2))
        self.bar.blit(self.up_bar_surface,(0,0))


    def draw(self):
        # Wyświetlenie powierzchni górnej belki na ekranie
        self.screen.blit(self.bar, (0, 0))
        self.update()
    def update(self):

        money_score = self.font.render("Ilość Złota: " + str(Stats.gold_count), True, "white")
        army_score = self.font.render("Ilość Wojska: " + str(Stats.army_count), True, "white")
        tiles_score = self.font.render("Ilość Posiadanych Pól: " + str(Stats.terrain_count), True, "white")
        turn_score = self.font.render("Tura: " + str(Stats.turn_count), True, "white")

        self.screen.blit(money_score, (20, 2))
        self.screen.blit(army_score, (210, 2))
        self.screen.blit(tiles_score, (400, 2))
        self.screen.blit(turn_score, (1100, 4))

class Timer:
    def __init__(self, screen,game):
        #SCREEN#
        self.SCREEN_WIDTH = screen.get_size()[0]
        self.SCREEN_HEIGHT = screen.get_size()[1]
        ########
        self.game = game
        self.screen = screen
        FONT_SIZE = 18
        FONT_NAME = 'timesnewroman'
        self.font_timer = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.start_time = time.time()
        self.timer_box = pygame.Rect(self.SCREEN_WIDTH - 90, 0, 90, 30)

    def update(self):
        # Update the timer
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        if minutes%1==0 and not minutes == 0 and seconds ==0:
            self.autosave_game()


        # Draw the timer text
        timer_text = self.font_timer.render('{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds), True,
                                            (255, 255, 255))
        
        text_rect = timer_text.get_rect(center=self.timer_box.center)
        self.screen.blit(timer_text, text_rect)
        
    def autosave_game(self):
        import gameplay
        print('SaveGame')

        folder_path = "save"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open('save/map.csv','w') as savefile:
            savefile.write('x;y;number;texture_index;zajete\n')
            for h in self.game.map.sprites():
                savefile.write(f'{h.polozenie_hex_x};{h.polozenie_hex_y};{h.number};{h.texture_index};{h.zajete}')
                savefile.write('\n')
        with open('save/stats.txt','w') as savefile:
            
            savefile.write(f'gold_count:{Stats.gold_count}\n')
            savefile.write(f'army_count:{Stats.army_count}\n')
            savefile.write(f'player_hex_status:{Stats.player_hex_status}\n')
            savefile.write(f'army_count_bonus:{Stats.army_count_bonus}\n')
            savefile.write(f'gold_count_bonus:{Stats.gold_count_bonus}\n')
            savefile.write(f'turn_count:{Stats.turn_count}\n')
            
        pygame.time.Clock().tick(1)
        with zipfile.ZipFile("save/AutoSave.zip", "w") as zip:
            zip.write("save/stats.txt")
            zip.write("save/map.csv")
        os.remove("save/stats.txt")
        os.remove("save/map.csv")
        pass

class Hourglass:

    def __init__(self, screen):
        #SCREEN#
        self.SCREEN_WIDTH = screen.get_size()[0]
        self.SCREEN_HEIGHT = screen.get_size()[1]
        ########
        self.hourglass_surface = pygame.transform.scale((pygame.image.load("texture/ui/turn/klepsydra.jpg")),
                                                        (173, 184)).convert_alpha()
        self.hourglass_rect = self.hourglass_surface.get_rect(center=(100, self.SCREEN_HEIGHT-100))
        self.screen = screen

    def draw(self):
        self.screen.blit(self.hourglass_surface, self.hourglass_rect)

    def turn(self):
        colision = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.hourglass_rect.collidepoint(colision) and mouse_pressed[0]:
            if Stats.wyb == False:    
                Stats.wyb = True
                Stats.turn_count += 1


class Decision:
    def __init__(self, screen):
        #SCREEN#
        self.SCREEN_WIDTH = screen.get_size()[0] - 256
        self.SCREEN_HEIGHT = screen.get_size()[1]
        ########
        self.background_image = pygame.image.load('texture/ui/turn/tlo_wybor.png').convert_alpha()
        self.army_button = pygame.image.load("texture/ui/turn/wojsko_button.png").convert_alpha()
        self.gold_button = pygame.image.load("texture/ui/turn/zloto_button.png").convert_alpha()
        self.field_button = pygame.image.load("texture/ui/turn/zajmij_button.png").convert_alpha()

        ##### CO TU SIĘ DZIEJE

        self.bacground_rect = self.background_image.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2))
        # self.bacground_rect = self.background_image.get_rect(topleft=(775, 350))
        self.gold_rect = self.gold_button.get_rect(midtop=(self.SCREEN_WIDTH/2, 230))
        self.army_rect = self.army_button.get_rect(midtop=(self.SCREEN_WIDTH/2, 330))
        self.field_rect = self.field_button.get_rect(midtop=(self.SCREEN_WIDTH/2, 430))

        self.screen = screen

        
        self.background_image.blit(self.gold_button, (self.gold_button.get_size()[0]/4-2,50))
        self.background_image.blit(self.army_button, (self.army_button.get_size()[0]/4-2,150))
        self.background_image.blit(self.field_button, (self.field_button.get_size()[0]/4-2,250))
        self.RED = (255,100,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
    def draw(self):
        global camera_stop
        if Stats.wyb:
            camera_stop = True
            self.screen.blit(self.background_image, self.bacground_rect)
            

    def click(self):
        global camera_stop
        colision = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.gold_rect.collidepoint(colision) and mouse_pressed[0] and Stats.wyb:
            Stats.wyb = False
            camera_stop = False
            Stats.gold_count += 10 + Stats.gold_count_bonus

        if self.army_rect.collidepoint(colision) and mouse_pressed[0] and Stats.wyb:
            Stats.wyb = False
            camera_stop = False
            Stats.army_count += 10 + Stats.army_count_bonus

        if self.field_rect.collidepoint(colision) and mouse_pressed[0] and Stats.wyb:
            Stats.wyb = False
            camera_stop = False
            Stats.player_hex_status = True
            pygame.time.Clock().tick(3)


class SideMenu:

    def __init__(self, screen):
        #SCREEN#
        self.SCREEN_WIDTH = screen.get_size()[0]
        self.SCREEN_HEIGHT = screen.get_size()[1]
        ########
        FONT_SIZE = 18
        FONT_NAME = 'timesnewroman'
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        ########
        self.texture_main = "texture/ui/side_bar/praweUI_glowne.png"
        self.texture_up = "texture/ui/side_bar/praweUI_gorne.png"
        self.texture_down = "texture/ui/side_bar/praweUI_dolne.png"
        self.texture_button = "texture/ui/side_bar/praweUI_srodek.png"

        self.main_surfarce = pygame.image.load(self.texture_main).convert_alpha()
        self.up_surfarce = pygame.image.load(self.texture_up).convert_alpha()
        self.down_surfarce = pygame.image.load(self.texture_down).convert_alpha()
        self.button_surfarce = pygame.image.load(self.texture_button).convert_alpha()
        self.main_rect = self.main_surfarce.get_rect(topleft=(self.SCREEN_WIDTH-256, 30))
        self.button_rect = self.button_surfarce.get_rect(topleft=(self.SCREEN_WIDTH-246, 258))
        self.up_rect = self.up_surfarce.get_rect(topleft=(10,12))
        self.down_rect = self.down_surfarce.get_rect(topleft=(10,410))
        self.screen = screen

        ####
        self.main_surface = pygame.Surface((256,self.SCREEN_HEIGHT-30),pygame.SRCALPHA)
        self.main_surface.blit(self.main_surfarce,(0,0))
        self.main_surface.blit(self.up_surfarce,self.up_rect)
        self.main_surface.blit(self.button_surfarce,(10, 258))
        self.main_surface.blit(self.down_surfarce,self.down_rect)
        ####


    def surowce_staty(self, x, y, tekst):
        self.tekst = tekst
        
        self.font_opis_s = self.font.render(self.tekst, True, (255, 255, 255))

        self.screen.blit(self.font_opis_s, (x,y))
    def surowce_staty_blituj(self):
        x = self.SCREEN_WIDTH-235
        y = 87
        for i in range(len(Stats.surowce_ilosc)):
            self.surowce_staty(x,y, f"{Stats.surowce_ilosc[i][2]} {Stats.surowce_ilosc[i][1]}")
            y += 22

    def draw(self):
        
        self.screen.blit(self.main_surface,self.main_rect)
        self.surowce_staty(self.SCREEN_WIDTH-235, 65, "SUROWCE:")
        self.surowce_staty_blituj()

    def button(self):
        colision = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.button_rect.collidepoint(colision) and mouse_pressed[0]:
            Build_Menu.build_stauts = True


class Build_Menu:
    build_stauts=False
    def __init__(self, screen):
        
        self.texture = "texture/ui/building/kuptlo.png"
        self.texture_button = "texture/ui/building/CheckBoxFalse.png"
        self.szerokosc = 700
        self.wysokos = 500
        self.x = 640
        self.y = 360
        self.build_menu_surf = pygame.transform.scale((pygame.image.load(self.texture)).convert_alpha(),
                                                      (self.szerokosc, self.wysokos))

        self.item_menu_surf = pygame.Surface((self.szerokosc, self.wysokos), pygame.SRCALPHA)

        self.exit_button_surf = pygame.transform.scale(pygame.image.load(self.texture_button).convert_alpha(), (40, 40))
        self.build_rect = self.build_menu_surf.get_rect(center=(self.x, self.y))
        self.build_menu_surf.set_alpha(230)
        self.screen = screen
        self.exit_button_rect = self.exit_button_surf.get_rect()
        self.exit_button_rect.topright = self.build_rect.topright
        # self.build_menu_surf.blit(self.item_menu_surf,(0,0))
        self.build_menu_surf.blit(self.exit_button_surf, (660,0))
    def draw(self):

        colision = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.build_stauts:
            self.screen.blit(self.build_menu_surf, self.build_rect)
            self.screen.blit(self.item_menu_surf, self.build_rect)
            
            
            
            if self.exit_button_rect.collidepoint(colision) and mouse_pressed[0]:
                Build_Menu.build_stauts = False
            


class BuildItem:
    def __init__(self, menu, koszt, texture, opis, army_bonus, gold_bonus):
        FONT_SIZE = 18
        FONT_NAME = 'timesnewroman'
        self.font_opis = pygame.font.SysFont(FONT_NAME,FONT_SIZE)

        self.font_opis_s = self.font_opis.render(opis, True,
                                                 (255, 255, 255))
        self.army_bonus = army_bonus
        self.gold_bonus = gold_bonus

        global item_offset
        self.text_description = opis
        self.menu = menu
        self.wymiary = pygame.Vector2(self.menu.get_size())
        self.item_w = self.wymiary.x * 0.9
        self.item_h = 110
        self.image = pygame.image.load(f'texture/ui/building/{texture}.png')
        # self.image = pygame.Surface((100, 100))
        self.button = pygame.Surface((150, 50))
        self.button_texture = pygame.image.load('texture/ui/building/button_kup.png')
        self.button.blit(self.button_texture, (0, 0))

        self.koszt = koszt
        self.posiadanie = False
        opis_texture = pygame.image.load('texture/ui/building/opis_tlo.png')
        opis_texture = pygame.transform.scale(opis_texture, (
            self.item_w - self.image.get_size()[0] - self.button.get_size()[0] - 30, self.item_h - 10))
        self.description_surf = pygame.Surface(
            (self.item_w - self.image.get_size()[0] - self.button.get_size()[0] - 30, self.item_h - 10),
            pygame.SRCALPHA)
        item_texture = pygame.image.load('texture/ui/building/kuptlo.png')
        self.item_surf = pygame.Surface((self.item_w, self.item_h), pygame.SRCALPHA)

        self.item_surf.blit(item_texture, (0, 0))

        self.description_surf.blit(opis_texture, (0, 0))

        self._id = item_offset.x
        self.button_rect = self.button.get_rect(bottomleft=(
            pygame.display.get_window_size()[0] / 2 - self.menu.get_size()[0] / 2 + self.image.get_size()[0] + 10 + 35,
            360 / 2 + 10 + item_offset.y * self._id))
        
        item_offset.x += 1
        self.item_surf.blit(self.image, (5, self.item_h / 2 - self.image.get_size()[1] / 2))
        self.description_surf.blit(self.font_opis_s, (5, 5))
        self.item_surf.blit(self.button,
                            (self.image.get_size()[0] + 10, self.item_h / 2 - self.button.get_size()[1] / 2))
        self.item_surf.blit(self.description_surf, (self.image.get_size()[0] + 20 + self.button.get_size()[0],
                                                    self.item_h / 2 - self.description_surf.get_size()[1] / 2))
    def draw(self):       
        self.menu.blit(self.item_surf, (self.wymiary.x / 2 - self.item_w / 2, 10 + item_offset.y * self._id))
        

    def buy(self):
        
        press = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(pos) and press[0]:
            if not Stats.gold_count < self.koszt:
                self.posiadanie = True
                Stats.gold_count -= self.koszt
                Stats.army_count_bonus +=  self.army_bonus
                Stats.gold_count_bonus += self.gold_bonus
            pygame.time.Clock().tick(5)
        pass
