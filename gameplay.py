import zipfile
import pygame
import time, os
import random
from menu import *
from event_description import *

item_offset = pygame.Vector2(0, 115)
pygame.mixer.init()

class Stats:
    item_offset = pygame.Vector2(0, 115)
    gold_count = 0
    army_count = 0
    army_count_bonus = 0
    gold_count_bonus = 0

    terrain_count = 1
    turn_count = 1

    wyb = False
    field_status = False
    camera_stop = False
    player_hex_status = False
    turn_stop = False
    
    def __init__(self) -> None:
        pass

class Player:
    start_turn = False
    MAX = 0
    ID =0
    castle_hex = [137,137*2,137*5,137*6]
    # castle_hex = [137*2,137*2,137*2,137*2,137*2]
    use_castle = []
    def __init__(self, name: str) -> None:
        Player.MAX += 1
        self.confirm = False
        self.buildMenu = None 
        self.home = random.choice(Player.castle_hex)
        self.home_x = 0
        self.home_y = 0

        Player.castle_hex.remove(self.home)
        Player.use_castle.append(self.home)
        self.player_name = name
        self.nacja =  None 
        self.wyb = False
        self.turn_stop = False
        self.field_status = False
        self.camera_stop = False
        self.player_hex_status = False
        self.item_offset = pygame.Vector2(0, 115)
        
        self.gold_count = 0
        self.army_count = 100
        self.terrain_count = 1
        self.turn_count = 1
        self.army_count_bonus = 0
        self.gold_count_bonus = 0
        self.surowce_ilosc = [["clay", 0, "glina: "], ["mine_diamonds", 0, "diamenty: "], ["mine_rocks", 0, "kamień: "],
                              ["mine_iron", 0, "żelazo: "], ["mine_gold", 0, "złoto: "], ["fish_port", 0, "ryby: "],
                              ["sawmill", 0, "drewno: "], ["grain", 0, "zboże: "]]
    
    
    @staticmethod
    def next_player():
        if Player.ID == Player.MAX-1:
            Player.ID = 0
        else:
            Player.ID += 1
        Player.start_turn = False
        
    def dopisz_surowiec(self, surowiec):
        for i in range(len(self.surowce_ilosc)):
            if surowiec == self.surowce_ilosc[i][0]:
                self.surowce_ilosc[i][1] += 100

    def zajmij_pole(self, allrect, allmask, allhex, dec):
        if self.player_hex_status:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                pos1 = pygame.mouse.get_pos()
                for i in range(len(allhex)):
                    pos_in_mask1 = pos1[0] - allrect['hex', i].x, pos1[1] - allrect['hex', i].y
                    touching = allrect['hex', i].collidepoint(*pos1) and allmask['hex', i].get_at(
                        pos_in_mask1)

                    if touching and allhex["hex", i].field_add and self.player_name in allhex["hex", i].playerable:
                        if allhex["hex", i].rodzaj == "surowiec":
                            print(allhex["hex", i].rodzaj_surowca_var)
                            self.dopisz_surowiec(allhex["hex", i].rodzaj_surowca_var)
                        if allhex["hex", i].rodzaj == "budynek":
                            print("budynek")
                            # dodawanie bonusu do zarabiania
                            if allhex["hex", i].texture_index == -2: # ruiny 
                                enemy = random.randint(10,50)
                                self.army_count += (self.army_count-enemy if enemy > self.army_count else self.army_count-enemy )
                                if self.army_count > enemy:
                                    self.gold_count += 10*random.randint(1,25)
                                self.army_count_bonus += 10
                            if allhex["hex", i].texture_index == -3: # oboz 
                                enemy = random.randint(10,50)
                                self.army_count += (self.army_count-enemy if enemy > self.army_count else self.army_count-enemy )
                                if self.army_count > enemy:
                                    self.gold_count += 10*random.randint(1,3)
                                    allhex["hex", i].texture_index = 10
                                    allhex["hex", i].update_texture()
                                    self.gold_count_bonus +=10
                                    self.surowce_ilosc[1][1] = random.randint(0,5)
                                    self.surowce_ilosc[7][1] = random.randint(50,200)
                                    
                                self.army_count_bonus += 10
                            elif allhex["hex", i].texture_index == 10: # wioska 
                                self.gold_count_bonus += 10
                        allhex["hex", i].zajete = True
                        allhex["hex", i].field_add = False
                        dec.fupdate.new_hex(i,self)
                        self.field_status = False
                        self.player_hex_status = False
                        self.terrain_count += 1
                        self.turn_stop = False
                        allhex['hex',i].player = self.player_name
                        self.confirm = True
                        


class Camera:
    camera_x = 0
    camera_y = 0
    def player_camera_update(player):
        """
        Purpose: 
        """
        Camera.camera_x = player.home_x*(-1)+600
        Camera.camera_y = player.home_y*(-1)+300
        if Camera.camera_x > 1600:
            Camera.camera_x -= (Camera.camera_x-1600)
            print(f"{Camera.camera_x } {Camera.camera_y }")
        
    # end def
    def __init__(self):

        self.mouse_x = 0
        self.mouse_y = 0
        self.move_mouse_max = 160

    def mouse(self, mapsize):

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        predkosc = 5
        press = pygame.key.get_pressed()
        if Stats.camera_stop is False:
            if not press[pygame.K_LCTRL]:
                if Camera.camera_x < 1600:
                    if self.mouse_x < 30:
                        Camera.camera_x += (predkosc + 10)
                    elif self.mouse_x < 80:
                        Camera.camera_x += (predkosc + 5)
                    elif self.mouse_x < self.move_mouse_max:
                        Camera.camera_x += predkosc
                if Camera.camera_x > 1640 - (mapsize * 130) + 1110:
                    if self.mouse_x > 1240:
                        Camera.camera_x -= predkosc + 10
                    elif self.mouse_x > 1190:
                        Camera.camera_x -= predkosc + 5
                    elif self.mouse_x > 1110:
                        Camera.camera_x -= predkosc

                if Camera.camera_y < - 20:
                    if self.mouse_y < 30:
                        Camera.camera_y += predkosc + 10
                    elif self.mouse_y < 80:
                        Camera.camera_y += predkosc + 5
                    elif self.mouse_y < 160:
                        Camera.camera_y += predkosc

                if Camera.camera_y > (-152 * mapsize / 2) - (75 * mapsize / 2) + 825:
                    if self.mouse_y > 670:
                        Camera.camera_y -= predkosc + 10
                    elif self.mouse_y > 620:
                        Camera.camera_y -= predkosc + 5
                    elif self.mouse_y > 540:
                        Camera.camera_y -= predkosc

    def keybord(self,mapsize):
        press = pygame.key.get_pressed()
        if press[pygame.K_RIGHT]:
            if Camera.camera_x > 1640 - (mapsize * 130) + 1110:
                Camera.camera_x -= 5
        if press[pygame.K_LEFT]:
            if Camera.camera_x < 1600:
                Camera.camera_x += 5
        if press[pygame.K_DOWN]:
            if Camera.camera_y > (-152 * mapsize / 2) - (75 * mapsize / 2) + 825:
                Camera.camera_y -= 5
        if press[pygame.K_UP]:
            if Camera.camera_y < - 20:
                Camera.camera_y += 5


class UpBar:

    def __init__(self, screen: pygame.Surface):
        # SCREEN#
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
        self.bar_main = pygame.transform.scale(pygame.image.load('texture/ui/up_bar/bar.png').convert_alpha(),
                                               (self.SCREEN_WIDTH, 30))
        self.screen = screen

    def draw(self,player):
        # Wyświetlenie powierzchni górnej belki na ekranie
        self.screen.blit(self.bar_main, (0, 0))
        self.update(player)

    def update(self,player):
        money_score = self.font.render("Ilość Złota: " + str(player.gold_count), True, "white")
        army_score = self.font.render("Ilość Wojska: " + str(player.army_count), True, "white")
        tiles_score = self.font.render("Ilość Posiadanych Pól: " + str(player.terrain_count), True, "white")
        turn_score = self.font.render("Tura: " + str(player.turn_count), True, "white")

        self.screen.blit(money_score, (20, 2))
        self.screen.blit(army_score, (210, 2))
        self.screen.blit(tiles_score, (400, 2))
        self.screen.blit(turn_score, (1100, 4))


class Timer:
    def __init__(self, screen: pygame.Surface, game):
        # SCREEN#
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
        if minutes % 1 == 0 and not minutes == 0 and seconds == 0:
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

        with open('save/map.csv', 'w') as savefile:
            savefile.write('x;y;number;texture_index;zajete\n')
            for h in self.game.map.sprites():
                savefile.write(f'{h.polozenie_hex_x};{h.polozenie_hex_y};{h.number};{h.texture_index};{h.zajete}')
                savefile.write('\n')
        with open('save/stats.txt', 'w') as savefile:

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
    button_sound_hourglass = pygame.mixer.Sound('music/music_ambient/hourglass.mp3')
    button_sound_hourglass.set_volume(1.0)
    def __init__(self, screen: pygame.Surface, frame_rate: int, animation_frame_interval: int):
        self.SCREEN_WIDTH = screen.get_size()[0]
        self.SCREEN_HEIGHT = screen.get_size()[1]
        self.screen = screen
        self.hourglass_rect = pygame.Rect(10, self.SCREEN_HEIGHT - 190, 173, 184)
        # Load animation frames
        path_to_images = "texture/ui/klepsydra"
        self.animation_frames = []
        for file_name in sorted(os.listdir(path_to_images)):
            if file_name.endswith(".png"):
                image = pygame.image.load(os.path.join(path_to_images, file_name))
                self.animation_frames.append(pygame.transform.scale(image, (173, 184)).convert_alpha())
        self.frame_index = 0
        self.frame_rate = frame_rate
        self.animation_frame_interval = animation_frame_interval
        self.last_frame_time = pygame.time.get_ticks()

    def draw(self):
        self.screen.blit(self.animation_frames[self.frame_index], self.hourglass_rect)

    def next_frame(self):
        # Switch to the next animation frame
        self.frame_index += 1
        if self.frame_index >= len(self.animation_frames):
            self.frame_index = 0

    def turn(self,player):
        collision = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.hourglass_rect.collidepoint(collision) and mouse_pressed[0]:
            Hourglass.button_sound_hourglass.play()
            if player.wyb == False and not player.turn_stop:
                player.wyb = True
                player.turn_count += 1
                self.next_frame()
                self.last_frame_time = pygame.time.get_ticks()

        # Check if it's time to switch animation frame
        current_time = pygame.time.get_ticks()
        time_since_last_frame = current_time - self.last_frame_time
        if time_since_last_frame >= 1000 / self.frame_rate * self.animation_frame_interval:
            self.next_frame()
            self.last_frame_time = current_time


class Decision:
    button_sound_money = pygame.mixer.Sound('music/music_ambient/coins.mp3')
    button_sound_money.set_volume(1.0)
    button_sound_army = pygame.mixer.Sound('music/music_ambient/army.mp3')
    button_sound_army.set_volume(1.0)
    button_sound_field = pygame.mixer.Sound('music/music_ambient/sand.mp3')
    button_sound_field.set_volume(1.0)


    def __init__(self, screen: pygame.Surface, map,player):

        self.SCREEN_WIDTH = screen.get_size()[0] - 256
        self.SCREEN_HEIGHT = screen.get_size()[1]
        self.background_image = pygame.image.load('texture/ui/turn/tlo_wybor.png').convert_alpha()
        self.army_button = pygame.image.load("texture/ui/turn/wojsko_button.png").convert_alpha()
        self.gold_button = pygame.image.load("texture/ui/turn/zloto_button.png").convert_alpha()
        self.field_button = pygame.image.load("texture/ui/turn/zajmij_button.png").convert_alpha()
        self.screen = screen
        self.map = map

        # ilośc hexów w rzędzie
        self.numhex = self.map.num_hex_right_side

        self.fupdate = FieldUpdate(self.map.sprites(), self.numhex)
        
        self.fchoice = FieldChoice(self.map.sprites(), self.screen,player)

        self.bacground_rect = self.background_image.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2))
        self.gold_rect = self.gold_button.get_rect(midtop=(self.SCREEN_WIDTH / 2, 230))
        self.army_rect = self.army_button.get_rect(midtop=(self.SCREEN_WIDTH / 2, 330))
        self.field_rect = self.field_button.get_rect(midtop=(self.SCREEN_WIDTH / 2, 430))

        self.background_image.blit(self.gold_button, (self.gold_button.get_size()[0] / 4 - 2, 50))
        self.background_image.blit(self.army_button, (self.army_button.get_size()[0] / 4 - 2, 150))
        self.background_image.blit(self.field_button, (self.field_button.get_size()[0] / 4 - 2, 250))

    def draw(self,player):
        if player.confirm:
            player.confirm = False
            Player.next_player()
        else:
            if player.wyb:
                player.camera_stop = True
                self.screen.blit(self.background_image, self.bacground_rect)

    def click(self,player):
        colision = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.gold_rect.collidepoint(colision) and mouse_pressed[0] and player.wyb:
            Decision.button_sound_money.play()
            player.wyb = False
            player.camera_stop = False
            player.gold_count += 10 + player.gold_count_bonus
            player.confirm = True

        if self.army_rect.collidepoint(colision) and mouse_pressed[0] and player.wyb:
            Decision.button_sound_army.play()
            player.wyb = False
            player.camera_stop = False
            player.army_count += 10 + player.army_count_bonus
            player.confirm = True

        if self.field_rect.collidepoint(colision) and mouse_pressed[0] and player.wyb:
            Decision.button_sound_field.play()
            player.wyb = False
            player.camera_stop = False
            player.turn_stop = True
            self.fchoice.check()
            player.field_status = True
            player.player_hex_status = True
            pygame.time.Clock().tick(3)


class FieldUpdate:
    sound_diamond = pygame.mixer.Sound('music/music_ambient/diamond.mp3')
    sound_diamond.set_volume(1.0)

    def __init__(self, sprites, num):
        self.sprites = sprites
        self.num_sprites = len(sprites)
        self.quantity_hex = num

    def start(self,player:Player):
        if player.home%2==1:
            prev_index = (player.home - 1) % self.num_sprites
            next_index = (player.home + 1) % self.num_sprites
            c = (player.home - self.quantity_hex) % self.num_sprites
            d = (player.home + 1 - self.quantity_hex) % self.num_sprites
            e = (player.home + self.quantity_hex) % self.num_sprites
            f = (player.home + self.quantity_hex + 1) % self.num_sprites
        elif player.home%2 ==0:
            prev_index = (player.home - 1) % self.num_sprites
            next_index = (player.home + 1) % self.num_sprites
            c = (player.home - self.quantity_hex-1) % self.num_sprites
            d = (player.home + 1 - self.quantity_hex-1) % self.num_sprites
            
            e = (player.home + self.quantity_hex-1) % self.num_sprites
            f = (player.home + self.quantity_hex ) % self.num_sprites

        if not self.sprites[prev_index].zajete and self.sprites[player.home].player == player.player_name:
            FieldUpdate.sound_diamond.play()
            self.sprites[prev_index].field_add = True
            self.sprites[prev_index].playerable += [player.player_name]

        if not self.sprites[next_index].zajete and self.sprites[player.home].player == player.player_name:
            FieldUpdate.sound_diamond.play()
            self.sprites[next_index].field_add = True
            self.sprites[next_index].playerable += [player.player_name]
        
        if not self.sprites[c].zajete and self.sprites[player.home].player == player.player_name:
            self.sprites[c].field_add = True
            self.sprites[c].playerable += [player.player_name]
        
        if not self.sprites[d].zajete and self.sprites[player.home].player == player.player_name:
            self.sprites[d].field_add = True
            self.sprites[d].playerable += [player.player_name]
        
        if not self.sprites[e].zajete and self.sprites[player.home].player == player.player_name:
            self.sprites[e].field_add = True
            self.sprites[e].playerable += [player.player_name]
        
        if not self.sprites[f].zajete and self.sprites[player.home].player == player.player_name:
            self.sprites[f].field_add = True
            self.sprites[f].playerable += [player.player_name]
    def new_hex(self, hex,player):

        column = hex // self.quantity_hex
        if hex % self.quantity_hex == 0:
            column + 1

        if column % 2 == 0:
            prev_index = (hex - 1) % self.num_sprites
            next_index = (hex + 1) % self.num_sprites
            c = (hex - self.quantity_hex) % self.num_sprites
            d = (hex + 1 - self.quantity_hex) % self.num_sprites
            e = (hex + self.quantity_hex) % self.num_sprites
            f = (hex + self.quantity_hex + 1) % self.num_sprites
        else:
            prev_index = (hex - 1) % self.num_sprites
            next_index = (hex + 1) % self.num_sprites
            c = (hex - self.quantity_hex) % self.num_sprites
            d = (hex - 1 - self.quantity_hex) % self.num_sprites
            e = (hex + self.quantity_hex) % self.num_sprites
            f = (hex + self.quantity_hex - 1) % self.num_sprites

        if not self.sprites[prev_index].zajete :
            self.sprites[prev_index].field_add = True
            if not player.player_name is self.sprites[prev_index].playerable:
                self.sprites[prev_index].playerable += [player.player_name]

        if not self.sprites[next_index].zajete :
            self.sprites[next_index].field_add = True
            if not player.player_name is self.sprites[next_index].playerable:
                self.sprites[next_index].playerable += [player.player_name]
            

        if not self.sprites[c].zajete :
            self.sprites[c].field_add = True
            if not player.player_name is self.sprites[c].playerable:
                self.sprites[c].playerable += [player.player_name]

        if not self.sprites[d].zajete :
            self.sprites[d].field_add = True
            if not player.player_name is self.sprites[d].playerable:
                self.sprites[d].playerable += [player.player_name]

        if not self.sprites[e].zajete :
            self.sprites[e].field_add = True
            if not player.player_name is self.sprites[e].playerable:
                self.sprites[e].playerable += [player.player_name]

        if not self.sprites[f].zajete :
            self.sprites[f].field_add = True
            if not player.player_name is self.sprites[f].playerable:
                self.sprites[f].playerable += [player.player_name]


class FieldChoice:

    def __init__(self, sprites, screen,player:Player):
        self.Field_add_surface = pygame.image.load("texture/hex/hex_add.png").convert_alpha()
        self.Field_add_surface.set_alpha(100)
        self.sprites = sprites
        self.screen = screen
        self.player = player
        self.avalible_hex = []

    def check(self):
        self.avalible_hex = []
        for i in self.sprites:
            if i.field_add and self.player.player_name in i.playerable:
                self.avalible_hex.append(i)

    def draw(self):
        for i in self.avalible_hex:
            self.screen.blit(self.Field_add_surface, [i.polozenie_hex_x + Camera.camera_x,
                                                      i.polozenie_hex_y + Camera.camera_y])


class SideMenu:

    def __init__(self, screen: pygame.Surface):
        # SCREEN#
        self.SCREEN_WIDTH = screen.get_size()[0]
        self.SCREEN_HEIGHT = screen.get_size()[1]
        ########
        FONT_SIZE = 18
        FONT_NAME = 'timesnewroman'
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        ########
        self.texture_main = "texture/ui/side_bar/sideUI.png"
        self.texture_button_build = "texture/ui/side_bar/sideUIBud.png"
        self.texture_button_resource = "texture/ui/side_bar/sideUISur.png"
        self.main_surfarce = pygame.image.load(self.texture_main).convert_alpha()

        self.button_surfarce = pygame.transform.smoothscale(pygame.image.load(self.texture_button_build).convert_alpha(),(236,68))
        self.button_resource_surfarce = pygame.transform.smoothscale(pygame.image.load(self.texture_button_resource).convert_alpha(),(236,68))
        self.main_rect = self.main_surfarce.get_rect(topleft=(self.SCREEN_WIDTH - 256, 30))
        self.button_rect = self.button_surfarce.get_rect(topleft=(self.SCREEN_WIDTH - 246, 258 + 100))
        self.button_resource_rect = self.button_surfarce.get_rect(topleft=(self.SCREEN_WIDTH - 246, 258))
        self.screen = screen

        #####
        self.clay_icon = "texture/surowce/surowce_icons/glina.png"
        self.diax_icon = "texture/surowce/surowce_icons/diax.png"
        self.rocks_icon = "texture/surowce/surowce_icons/kamien.png"
        self.iron_icon = "texture/surowce/surowce_icons/zelazo.png"
        self.gold_icon = "texture/surowce/surowce_icons/zloto.png"
        self.fish_icon = "texture/surowce/surowce_icons/ryba.png"
        self.wood_icon = "texture/surowce/surowce_icons/tartak.png"
        self.cereal_icon = "texture/surowce/surowce_icons/klos.png"

        self.clay_icon_surface = pygame.image.load(self.clay_icon).convert_alpha()
        self.diax_icon_surface = pygame.image.load(self.diax_icon).convert_alpha()
        self.rocks_icon_surface = pygame.image.load(self.rocks_icon).convert_alpha()
        self.iron_icon_surface = pygame.image.load(self.iron_icon).convert_alpha()
        self.gold_icon_surface = pygame.image.load(self.gold_icon).convert_alpha()
        self.fish_icon_surface = pygame.image.load(self.fish_icon).convert_alpha()
        self.wood_icon_surface = pygame.image.load(self.wood_icon).convert_alpha()
        self.cereal_icon_surface = pygame.image.load(self.cereal_icon).convert_alpha()

        self.surowce_icons = []
        self.surowce_icons.append(self.clay_icon_surface)
        self.surowce_icons.append(self.diax_icon_surface)
        self.surowce_icons.append(self.rocks_icon_surface)
        self.surowce_icons.append(self.iron_icon_surface)
        self.surowce_icons.append(self.gold_icon_surface)
        self.surowce_icons.append(self.fish_icon_surface)
        self.surowce_icons.append(self.wood_icon_surface)
        self.surowce_icons.append(self.cereal_icon_surface)

        ####
        self.main_surface = pygame.Surface((256, self.SCREEN_HEIGHT - 30), pygame.SRCALPHA)
        self.main_surface.blit(self.main_surfarce, (0, 0))
        self.main_surface.blit(self.button_surfarce, (10, 335))
        self.main_surface.blit(self.button_resource_surfarce, (10, 253))
        ####

    def surowce_staty(self, x: int, y: int, tekst: str):
        self.tekst = tekst

        self.font_opis_s = self.font.render(self.tekst, True, (255, 255, 255))

        self.screen.blit(self.font_opis_s, (x, y))

    def surowce_staty_blituj(self,player):
        x = self.SCREEN_WIDTH - 210
        y = 67
        for i in range(len(player.surowce_ilosc)):
            self.surowce_staty(x, y, f"{player.surowce_ilosc[i][2]} {player.surowce_ilosc[i][1]}")
            self.surowce_icons[i] = pygame.transform.scale(self.surowce_icons[i], (21, 25))
            self.screen.blit(self.surowce_icons[i], (x - 30, y))
            y += 26

    def draw(self,player:Player):

        self.screen.blit(self.main_surface, self.main_rect)
        self.surowce_staty(self.SCREEN_WIDTH - 190, 47, f"{player.player_name}:")
        self.surowce_staty_blituj(player)



# EVENTY
class EventMenagment:
    def __init__(self, screen: pygame.Surface, player):
        self.chance = 0
        self.screen = screen
        self.turn = player.turn_count
        self.player = player
        self.events = []
        self.results = []
        self.placeholder = "texture/Events/placeholder.png"
    def start_event_list(self):

        najemnicy = Event(self.screen, opis_najemnicy, "texture/Events/najemnicy_img.png", 3, select_najemnicy, "Najemnicy", self)
        self.events.append(najemnicy)
        ruiny = Event(self.screen,opis_ruiny,self.placeholder, 2, select_ruiny, "Ruiny", self)
        self.events.append(ruiny)

    def random_event(self):

        if self.turn < self.player.turn_count:
            if self.events:
                if random.randint(0, 99) < self.chance:

                    x = random.choice(self.events)
                    x.execute()
                    self.events.remove(x)
                    self.turn = self.player.turn_count
                    self.chance = 0

                else:
                    self.chance += 20

                    self.turn = self.player.turn_count

    def add_result(self, result):
        self.results.append(result)

    def check_result(self):
        if not self.results == []:
            self.results[0].execute()
            if self.results[0].stop:
                self.results = []


class Event:
    sound_horn = pygame.mixer.Sound('music/music_ambient/horn.mp3')
    sound_horn.set_volume(1.0)
    sound_sword = pygame.mixer.Sound('music/music_ambient/sword.mp3')
    sound_sword.set_volume(1.0)
    sound_coin = pygame.mixer.Sound('music/music_ambient/coin.mp3')
    sound_coin.set_volume(1.0)
    sound_slice = pygame.mixer.Sound('music/music_ambient/slice.mp3')
    sound_slice.set_volume(1.0)

    def __init__(self, ekran: pygame.Surface, opis: str, grafika, ilosc_opcji: int, opisy_opcji: str, nazwa: str,
                 managment: EventMenagment):
        self.ekran = ekran
        self.opis = opis
        self.grafika = grafika
        self.ilosc_opcji = ilosc_opcji
        self.opisy_opcji = opisy_opcji
        self.nazwa = nazwa
        self.managment = managment


    def execute(self):
        Event.sound_horn.play()
        Render = EventRender(self.ekran, self.opis, self.grafika,self.nazwa)
        Render.draw()
        self.Choose = EventOptions(self.ilosc_opcji, self.opisy_opcji, self.ekran)
        self.Choose.draw()
        self.Wybor = self.Choose.colision_check(None)
        getattr(self, self.nazwa)(self.managment)




    def Najemnicy(self, managment):

        if self.Wybor == 1:
            Event.sound_slice.play()
            x = random.randint(0, 99)
            if x < 60:
                self.managment.player.gold_count += 100  # Zabij ich
                self.managment.player.army_count -= 10
                opis = " Udało ci się zabić najemników niewielkim\n nakładem sił ! \n\n Zrabowałeś ich złoto otrzymujesz : \n\n +100 złota!\n\n -10 Wojska"
                Result = EventResults(opis,self.ekran,self.managment)
                managment.add_result(Result)
            else:
                self.managment.player.army_count -= 50
                opis = " Niestety Najemnicy okazali sie zbyt mocni,\n zdołali stawić opór twoim żołnierzom  \n\n Tracisz : \n\n - 50 Wojska"
                Result = EventResults(opis, self.ekran,self.managment)
                managment.add_result(Result)


        if self.Wybor == 2:
            Event.sound_coin.play()
            self.managment.player.gold_count -= 200  # Zaplać im
            self.managment.player.army_count += 100

            opis = " Wynajęci najemnicy zasilają twoje szeregi! \n\n Zyskujesz : \n\n + 100 Wojska!\n\n Tracisz : \n\n - 200 złota"
            Result = EventResults(opis, self.ekran,self.managment)
            managment.add_result(Result)


            x = random.randint(0, 99)
            if x < 30:

                opisy = [" OK "]
                najemnicy_thief = Event(managment.screen, opis_najemnicy_thief, "texture/Events/najemnicy_img.png", 1, opisy,
                                        "najemnicy_thief", managment)
                managment.events.append(najemnicy_thief)

    def najemnicy_thief(self, managment):
        if self.Wybor == 0:
            Event.sound_slice.play()
            self.managment.player.army_count -= 100
            self.managment.player.gold_count -= 50

    def Ruiny(self, managment):
        if self.Wybor == 0:
            x = random.randint(0, 99)
            if x < 50:
                self.managment.player.army_count -= 25
                opis = " Niestety w ruinach chyba czaił sie jakiś \n potwór gdy obserwowałeś sytuacje z \n daleka dosięgły cię jedynie krzyki twoich \n żołnierzy którzy już nie wrócili\n\n\n Tracisz : - 25 wojska "
                Result = EventResults(opis,self.ekran,self.managment)
                managment.add_result(Result)
            if x > 50:
                self.managment.player.gold_count += 100
                opis = " Po całym dniu przeszukiwaniu ruin twoi\n żołnierze znaleźli trochę kosztowności \n\n\n Zyskujesz : + 100 złota !"
                Result = EventResults(opis, self.ekran,self.managment)
                managment.add_result(Result)



class EventRender:
    def __init__(self, screen: pygame.Surface, opis: str, grafika,nazwa):
        self.screen = screen
        screen_x, screen_y = self.screen.get_size()
        self.font = pygame.font.SysFont("cambria", 20)
        self.font2 = pygame.font.SysFont("cambria", 25)
        # wizualne rzeczy config
        wysokosc_background = screen_y * (92 / 100)
        szerokosc_background = screen_x * (64 / 100)
        wysokosc_img = wysokosc_background * (60 / 100)
        szerokosc_img = szerokosc_background * (57 / 100)
        self.nazwa = nazwa
        # pozycja
        self.x = (screen_x / 2) - (szerokosc_background / 2)
        self.y = (screen_y / 2) - (wysokosc_background / 2)
        self.img_posx = self.x - 10
        self.img_posy = self.y + screen_y * 0.149
        self.opis_posy = wysokosc_img + self.img_posy + 40
        self.opis_posx = self.img_posx

        # tekst i obrazki
        self.event_back = pygame.transform.smoothscale(pygame.image.load('texture/Events/back.png'),
                                                       (szerokosc_background, wysokosc_background))

        self.event_img = pygame.transform.scale(pygame.image.load(grafika),
                                                (szerokosc_img, wysokosc_img))
        self.opis_linie = opis.split('\n')

    def draw(self):
        self.screen.blit(self.event_back, (self.x - 36, self.y + 15))
        self.screen.blit(self.event_img, (self.img_posx, self.img_posy))
        odstep = 0
        for linia in self.opis_linie:
            tekst = self.font.render(linia, True, 'white')

            self.screen.blit(tekst, (self.opis_posx, self.opis_posy + odstep))
            odstep += 20
        title = self.font2.render("Event : ", True, 'white')
        title2 = self.font2.render(self.nazwa, True, 'white')
        self.screen.blit(title, (self.x * 2.20, self.y+45 ))
        self.screen.blit(title2, (self.x * 2.55, self.y + 45))


class EventOptions:

    def __init__(self, licz, opisy, screen):
        self.licz = licz
        self.x, self.y = screen.get_size()
        self.screen = screen
        self.event_options = pygame.transform.scale(pygame.image.load('texture/Events/option.png'),
                                                    (self.x * 0.22, self.y * 0.13))
        self.option_high = self.y * 0.82
        self.font = pygame.font.SysFont("georgia", 14)
        self.option_detecion = True
        self.rects = []
        self.option_selected = False
        self.opisy = opisy
        self.mid_text = self.y * 0.1

    def draw(self):
        if not self.option_selected:
            for i in range(self.licz):
                event_options_posx = self.x / 1.8
                event_options_posy = self.y / 5.5
                self.screen.blit(self.event_options, (event_options_posx, event_options_posy))
                if i < len(self.opisy):
                    opis = self.opisy[i]
                    opis_lines = opis.split('\n')
                    y_offset = 0
                    for line in opis_lines:
                        self.screen.blit(self.font.render(line, True, (255, 255, 255)), (self.x / 2 * 1.13,
                                                                                         event_options_posy + self.mid_text / 2 + y_offset))
                        y_offset += self.font.get_height()
                else:
                    opis = "Brak Opisu"
                    self.screen.blit(self.font.render(opis, True, (255, 255, 255)),
                                     (self.x / 2 * 1.13, event_options_posy + 6))

                img_rect = self.event_options.get_rect()
                img_rect[0] = event_options_posx
                img_rect[1] = event_options_posy
                self.rects.append(img_rect)
                self.y += self.option_high


    def colision_check(self,Results):



        while not self.option_selected:
            pygame.event.get()
            collision = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            pygame.display.flip()

            for i in range(len(self.rects)):
                if self.rects[i].collidepoint(collision) and mouse_pressed[0]:

                    self.option_selected = True
                    return i


class EventResults:

    def __init__(self, opis, screen, managment):
        self.background_result = pygame.transform.scale(pygame.image.load("texture/Events/Gui_eventy_wynik_pusty.png"),(1080/2.5,1200/2.5))
        self.opis = opis
        self.screen = screen
        self.font = pygame.font.SysFont("cambria", 20)
        self.opis_linie = self.opis.split('\n')
        self.stop = False
        self.managment = managment

    def execute(self):
        self.managment.player.turn_stop = True
        screen_x, screen_y = self.screen.get_size()
        background_rect = self.background_result.get_rect()
        background_x = (screen_x - background_rect.width) // 2
        background_y = (screen_y - background_rect.height) // 2
        self.rect = pygame.draw.rect(self.screen, "red", (background_x + 30, background_y * 4.23, 369, 50))
        self.screen.blit(self.background_result, (background_x, background_y))

        odstep = 0


        for linia in self.opis_linie:
            tekst = self.font.render(linia, True, 'white')

            self.screen.blit(tekst, (background_x*1.08, background_y*2 + odstep))
            odstep += 20

        collision = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.rect.collidepoint(collision) and mouse_pressed[0]:
            self.stop = True
            self.managment.player.turn_stop = False


class ResourceSell:
    active = False
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.transform.smoothscale(pygame.image.load("texture/ui/Resources/ResourceSell_back.png").convert_alpha(),(1000/1.4,800/1.4))
        self.button = pygame.transform.smoothscale(pygame.image.load("texture/ui/Resources/button sprzedaj.png").convert_alpha(),
                                                       (250 , 50 ))
        self.screen_rect = screen.get_rect()
        self.font = pygame.font.Font(None, 30)
        self.down_arrow = pygame.transform.smoothscale(pygame.image.load("texture/ui/Resources/down_arrow.png").convert_alpha(),(80,40))
        self.up_arrow = pygame.transform.smoothscale(
            pygame.image.load("texture/ui/Resources/up_arrow.png").convert_alpha(), (80, 40))

    def draw(self):
        if ResourceSell.active:
            background_rect = self.background.get_rect()
            background_rect.center = self.screen_rect.center
            self.screen.blit(self.background, background_rect)
            self.res_stats = ResourceSellStats(self.screen,self.font,self.button,self.down_arrow,self.up_arrow)

class ResourceSellStats:
    def __init__(self,screen,font,button,arrow_down,arrow_up):
        self.screen = screen
        self.font = font
        self.button = button
        self.up_arrow = arrow_up
        self.down_arrow = arrow_down
        prize = ["Cena : 20","Cena : 5","Cena : 7","Cena : 3","Cena : 2","Cena : 1","Cena : 10","Cena : 15"] # diamenty,glina,kamień,zboże,ryba,drewno,żelazo,ryda złota
        text = "0"
        text_color = (255, 255, 255)

        text_spacing = 50
        text_y = 170  # Początkowe położenie Y

        for i in range(8):
            text_surface = self.font.render(text, True, text_color)
            prize_surface = self.font.render(prize[i], True, text_color)
            text_rect = text_surface.get_rect()
            prize_rect = prize_surface.get_rect()
            button_rect = self.button.get_rect()
            down_arrow_rect = self.down_arrow.get_rect()
            up_arrow_rect = self.up_arrow.get_rect()
            text_rect.centerx = screen.get_rect().centerx
            prize_rect.centerx = screen.get_rect().centerx - 110
            button_rect.centerx = screen.get_rect().centerx + 170
            down_arrow_rect.centerx = screen.get_rect().centerx + 20
            up_arrow_rect.centerx = screen.get_rect().centerx - 20
            text_rect.y = text_y
            prize_rect.y = text_y
            button_rect.y = text_y - 15
            down_arrow_rect.y = text_y - 15
            up_arrow_rect.y = text_y - 15

            self.screen.blit(text_surface, text_rect)
            self.screen.blit(self.button, button_rect)
            self.screen.blit(prize_surface,prize_rect)
            self.screen.blit(self.up_arrow, up_arrow_rect)
            self.screen.blit(self.down_arrow, down_arrow_rect)
            text_y += text_spacing


