import zipfile
import pygame
import time,os,sys

build_stauts = True
build = True
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


class Camera:

    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0

        self.mouse_x = 0
        self.mouse_y = 0

    def mouse(self):

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        predkosc = 2
        press = pygame.key.get_pressed()
        if camera_stop is False:
            if not press[pygame.K_LCTRL]:
                if self.mouse_x < 30:
                    self.camera_x += (predkosc + 10)
                elif self.mouse_x < 80:
                    self.camera_x += (predkosc + 5)
                elif self.mouse_x < 160:
                    self.camera_x += predkosc

                if self.mouse_x > 1240:
                    self.camera_x -= predkosc + 10
                elif self.mouse_x > 1190:
                    self.camera_x -= predkosc + 5
                elif self.mouse_x > 1110:
                    self.camera_x -= predkosc

                if self.mouse_y < 30:
                    self.camera_y += predkosc + 10
                elif self.mouse_y < 80:
                    self.camera_y += predkosc + 5
                elif self.mouse_y < 160:
                    self.camera_y += predkosc

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
        self.up_bar_surface = pygame.Surface((1280, 30))
        self.up_bar_texture = pygame.image.load("texture/ui/up_bar/bar.png")
        self.screen = screen
        self.FONT_SIZE = 18
        self.FONT_NAME = 'timesnewroman'

    def score(self):
        FONT_NAME = 'timesnewroman'
        FONT_SIZE = 17
        # grafiki
        bar_main = pygame.image.load('texture/ui/up_bar/bar.png').convert_alpha()
        bar_gold = pygame.image.load('texture/ui/up_bar/bar_zloto.png').convert_alpha()
        bar_army = pygame.image.load('texture/ui/up_bar/bar_wojsko.png').convert_alpha()
        bar_field = pygame.image.load('texture/ui/up_bar/bar_pola.png').convert_alpha()

        self.up_bar_surface.blit(bar_main, (0, 0))

        # money
        money = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.up_bar_surface.blit(bar_gold, (10, 2))
        money_score = money.render("Ilość Złota: " + str(gold_count), True, "white")
        self.up_bar_surface.blit(money_score, (20, 2))

        # wojsko
        army = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.up_bar_surface.blit(bar_army, (200, 2))
        army_score = army.render("Ilość Wojska: " + str(army_count), True, "white")
        self.up_bar_surface.blit(army_score, (210, 2))
        # pola
        tiles = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.up_bar_surface.blit(bar_field, (390, 2))
        tiles_score = tiles.render("Ilość Posiadanych Pól: " + str(terrain_count), True, "white")
        self.up_bar_surface.blit(tiles_score, (400, 2))

        turn = pygame.font.SysFont(self.FONT_NAME, self.FONT_SIZE)
        turn_score = turn.render("Tura: " + str(turn_count), True, "white")
        self.up_bar_surface.blit(turn_score, (1100, 4))

        # Wyświetlenie powierzchni górnej belki na ekranie
        self.screen.blit(self.up_bar_surface, (0, 0))


class Timer:
    def __init__(self, res, main_surface, screen,game):
        self.game = game
        self.res = res
        self.mainSurface = main_surface
        self.screen = screen
        self.FONT_SIZE = 18
        self.FONT_NAME = 'timesnewroman'
        self.font_timer = pygame.font.SysFont(self.FONT_NAME, self.FONT_SIZE)
        self.start_time = time.time()
    def autosave_game(self):
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
            for h in self.game.map.sprites():
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
    
    def update(self):
        # Update the timer
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)

        if minutes%10==0 and not minutes == 0:

            self.autosave_game()

        # Draw the timer box
        timer_box = pygame.Rect(self.res[0] - 90, self.res[1] - 720, 90, 30)
        # pygame.draw.rect(self.mainSurface, (255, 255, 255), timer_box)
        # pygame.draw.rect(self.mainSurface, (0, 0, 0), timer_box, 2)

        # Draw the timer text
        timer_text = self.font_timer.render('{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds), True,
                                            (255, 255, 255))
        text_rect = timer_text.get_rect(center=timer_box.center)
        self.mainSurface.blit(timer_text, text_rect)
        self.screen.blit(self.mainSurface, (0, 0))
        # Update the display
        pygame.display.update()


class Hourglass:

    def __init__(self, screen):
        self.hourglass_surface = pygame.transform.scale((pygame.image.load("texture/ui/turn/klepsydra.jpg")),
                                                        (173, 184))
        self.hourglass_rect = self.hourglass_surface.get_rect(center=(100, 600))
        self.screen = screen

    def draw(self):
        self.screen.blit(self.hourglass_surface, self.hourglass_rect)

    def turn(self):
        global wyb
        global turn_count
        colision = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.hourglass_rect.collidepoint(colision) and mouse_pressed[0] and wyb is False:
            turn_count += 1
            wyb = True


class Decision:
    def __init__(self, screen):
        self.background_image = pygame.image.load('texture/ui/turn/tlo_wybor.png').convert_alpha()
        self.army_button = pygame.image.load("texture/ui/turn/wojsko_button.png").convert_alpha()
        self.gold_button = pygame.image.load("texture/ui/turn/zloto_button.png").convert_alpha()
        self.field_button = pygame.image.load("texture/ui/turn/zajmij_button.png").convert_alpha()

        self.bacground_rect = self.background_image.get_rect(midright=(775, 350))
        self.army_rect = self.gold_button.get_rect(midright=(700, 350))
        self.gold_rect = self.army_button.get_rect(midleft=(403, 250))
        self.field_rect = self.field_button.get_rect(midleft=(403, 450))

        self.screen = screen

    def draw(self):
        global camera_stop
        if wyb:
            camera_stop = True
            self.screen.blit(self.background_image, self.bacground_rect)
            self.screen.blit(self.gold_button, self.gold_rect)
            self.screen.blit(self.army_button, self.army_rect)
            self.screen.blit(self.field_button, self.field_rect)

    def click(self):
        global gold_count
        global wyb
        global army_count
        global camera_stop
        global player_hex_status

        colision = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.gold_rect.collidepoint(colision) and mouse_pressed[0] and wyb:
            wyb = False
            camera_stop = False
            gold_count += 10 + gold_count_bonus

        if self.army_rect.collidepoint(colision) and mouse_pressed[0] and wyb:
            wyb = False
            camera_stop = False
            army_count += 10 + army_count_bonus

        if self.field_rect.collidepoint(colision) and mouse_pressed[0] and wyb:
            wyb = False
            camera_stop = False
            player_hex_status = True


class SideMenu:
    def __init__(self, screen):
        self.texture_main = "texture/ui/side_bar/praweUI_glowne.png"
        self.texture_up = "texture/ui/side_bar/praweUI_gorne.png"
        self.texture_down = "texture/ui/side_bar/praweUI_dolne.png"
        self.texture_button = "texture/ui/side_bar/praweUI_srodek.png"

        self.main_surfarce = pygame.image.load(self.texture_main)
        self.main_rect = self.main_surfarce.get_rect(topleft=(1024, 30))
        self.up_surfarce = pygame.image.load(self.texture_up)
        self.down_surfarce = pygame.image.load(self.texture_down)
        self.button_surfarce = pygame.image.load(self.texture_button)
        self.button_rect = self.button_surfarce.get_rect(topleft=(1034, 288))

        self.screen = screen

    def draw(self):
        self.screen.blit(self.main_surfarce, self.main_rect)
        self.screen.blit(self.up_surfarce, (1034, 42))
        self.screen.blit(self.button_surfarce, self.button_rect)
        self.screen.blit(self.down_surfarce, (1034, 440))

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

    def draw(self):

        if self.build_stauts:
            self.screen.blit(self.build_menu_surf, self.build_rect)
            self.screen.blit(self.item_menu_surf, self.build_rect)
            exit_button_rect = self.exit_button_surf.get_rect()
            exit_button_rect.topright = self.build_rect.topright
            self.screen.blit(self.exit_button_surf, exit_button_rect)
            colision = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if exit_button_rect.collidepoint(colision) and mouse_pressed[0]:
                Build_Menu.build_stauts = False
            


class BuildItem:
    def __init__(self, menu, koszt, texture, opis, army_bonus, gold_bonus):
        self.FONT_SIZE = 18
        self.FONT_NAME = 'timesnewroman'
        self.font_opis = pygame.font.SysFont(self.FONT_NAME, self.FONT_SIZE)

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
        # pygame.draw.rect(rect=self.button_rect, color='#fff000', surface=pygame.display.get_surface())
        item_offset.x += 1

    def draw(self):

        self.item_surf.blit(self.image, (5, self.item_h / 2 - self.image.get_size()[1] / 2))
        self.item_surf.blit(self.button,
                            (self.image.get_size()[0] + 10, self.item_h / 2 - self.button.get_size()[1] / 2))
        self.item_surf.blit(self.description_surf, (self.image.get_size()[0] + 20 + self.button.get_size()[0],
                                                    self.item_h / 2 - self.description_surf.get_size()[1] / 2))
        self.description_surf.blit(self.font_opis_s, (5, 5))
        self.menu.blit(self.item_surf, (self.wymiary.x / 2 - self.item_w / 2, 10 + item_offset.y * self._id))
        # pygame.draw.rect(rect=self.button_rect, color='#fff000', surface=pygame.display.get_surface())

    def buy(self):
        global gold_count
        global army_count_bonus
        global gold_count_bonus
        press = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(pos) and press[0]:
            if not gold_count < self.koszt:
                self.posiadanie = True
                gold_count -= self.koszt
                army_count_bonus += self.army_bonus
                gold_count_bonus += self.gold_bonus
            pygame.time.Clock().tick(5)
        pass
