
import pygame

import random
from gameplay import Player, Stats


class Hex(pygame.sprite.Sprite):
    allsurowiec = [17 ,18 ,19 ,20 ,21 ,22 ,23 ,24]
    def __init__(self, x, y, num, group, obw, zaj ,tex_id):
        super().__init__(group)
        self.szerokosc = 130
        self.wysokosc = 152
        self.polozenie_hex_x = x
        self.polozenie_hex_y = y
        self.number = num
        self.obwodka = obw
        self.zajete = zaj
        self.group = group
        self.texture_index = tex_id
        self.texture = self.texturing(self.group)
        self.rodzaj = self.surowiec(  )  # self.czy_to_surowiec()
        self.rodzaj_surowca_var = None
        if self.number == 137:
            self.zajete = True
        if self.rodzaj == 'hex':
            self.rodzaj_surowca_var = None
        else:
            self.rodzaj_surowca_var = self.zwroc_liste()

    def rodzaj_surowca(self):
        return self.texture

    def texturing(self, group):
        if self.number == 137:
            return group.castle_surface
        if self.texture_index == 1:
            return group.grass_surface
        elif self.texture_index == 2:
            return group.grass2_surface
        elif self.texture_index == 3:
            return group.grass3_surface
        elif self.texture_index == 4:
            return group.forest_surface
        elif self.texture_index == 5:
            return group.mountain_surface
        elif self.texture_index == 6:
            return group.water_surface
        elif self.texture_index == 7:
            return group.water2_surface
        elif self.texture_index == 8:
            return group.water3_surface
        elif self.texture_index == 9:
            return group.cereal_surface
        elif self.texture_index == 10:
            return group.willage_surface
        elif self.texture_index == 11:
            return group.mountain_pass_surface
        elif self.texture_index == 12:
            return group.mountain2_surface
        elif self.texture_index == 13:
            return group.forest_full_surface
        elif self.texture_index == 14:
            return group.forest3_surface
        elif self.texture_index == 15:
            return group.forest4_surface
        elif self.texture_index == 16:
            return group.forest4_surface
        elif self.texture_index == 17:
            return group.clay
        elif self.texture_index == 18:
            return group.mine_diamonds
        elif self.texture_index == 19:
            return group.fish_port
        elif self.texture_index == 20:
            return group.sawmill
        elif self.texture_index == 21:
            return group.grain
        elif self.texture_index == 22:
            return group.mine_rocks
        elif self.texture_index == 23:
            return group.mine_iron
        elif self.texture_index == 24:
            return group.mine_gold

    def surowiec(self):
        if self.texture_index in Hex.allsurowiec:
            return 'surowiec'
        else:
            return 'hex'

    def update_texture(self):
        self.texture = self.texturing(self.group)

    def zwroc_liste(self):
        for k in range(len(self.group.surowce_lista)):
            if self.texture == self.group.surowce_lista[k][0]:
                return self.group.surowce_lista[k][1]


class Map(pygame.sprite.Group):

    def __init__(self, numx, numy, screen, camera):
        super().__init__()

        self.colision_surface = pygame.Surface(pygame.display.get_window_size(), pygame.SRCALPHA)
        self.colision_rect = self.colision_surface.get_rect()

        # obwodka, zajety hex i alpha
        self.hex_obwodka_surface = pygame.image.load("texture/hex/hex_obwodka.png").convert_alpha()
        self.hex_zajete_surface = pygame.image.load("texture/hex/hex_zajete_pole.png").convert_alpha()
        self.hex_zajete_surfaceNIE = pygame.image.load("texture/hex/hex_zajete_pole.png").convert_alpha()
        self.hex_zajete_surface.set_alpha(100)

        # BUDYNKI
        self.willage_surface = pygame.image.load("texture/hex/budynki.png").convert_alpha()
        self.castle_surface = pygame.image.load("texture/hex/zamek.png", ).convert_alpha()

        # SUROWCE
        self.clay = pygame.image.load("texture/surowce/hex_glina_surowiec.png").convert_alpha()
        self.mine_diamonds = pygame.image.load("texture/surowce/hex_kopalnia_diax.png").convert_alpha()
        self.mine_rocks = pygame.image.load("texture/surowce/hex_kopalnia_kamien.png").convert_alpha()
        self.mine_iron = pygame.image.load("texture/surowce/hex_kopalnia_zelazo.png").convert_alpha()
        self.mine_gold = pygame.image.load("texture/surowce/hex_kopalnia_kamien.png").convert_alpha()
        self.fish_port = pygame.image.load("texture/surowce/hex_port_surowiec.png").convert_alpha()
        self.sawmill = pygame.image.load("texture/surowce/hex_tartak_surowiec.png").convert_alpha()
        self.grain = pygame.image.load("texture/surowce/hex_zboze_surowiec_trawa.png").convert_alpha()

        # zwykle hexy
        self.grass_surface = pygame.image.load("texture/hex/hex_trawa.png", ).convert_alpha()
        self.grass2_surface = pygame.image.load("texture/hex/trawa_hex_2.png", ).convert_alpha()
        self.grass3_surface = pygame.image.load("texture/hex/trawa_hex_3.png").convert_alpha()
        self.cereal_surface = pygame.image.load("texture/hex/zboze_hex.png").convert_alpha()
        self.forest_surface = pygame.image.load("texture/hex/las_hex.png", ).convert_alpha()
        self.forest_full_surface = pygame.image.load("texture/hex/las_hex_pelny.png", ).convert_alpha()
        self.forest3_surface = pygame.image.load("texture/hex/las_hex_3_drzewka.png", ).convert_alpha()
        self.forest4_surface = pygame.image.load("texture/hex/las_hex_4_drzewka_wystajace.png", ).convert_alpha()
        self.mountain_surface = pygame.image.load("texture/hex/gory_hex.png", ).convert_alpha()
        self.mountain_pass_surface = pygame.image.load("texture/hex/gory_hex_pas.png", ).convert_alpha()
        self.mountain2_surface = pygame.image.load("texture/hex/gory_hex_bez_sniegu.png", ).convert_alpha()
        self.water_surface = pygame.image.load("texture/hex/woda_hex_1.png", ).convert_alpha()
        self.water2_surface = pygame.image.load("texture/hex/woda_hex_2.png", ).convert_alpha()
        self.water3_surface = pygame.image.load("texture/hex/woda_hex_statek.png", ).convert_alpha()
        self.water3_surface2 = self.water3_surface
        print(self.water3_surface == self.water3_surface2)

        self.elements = [((self.grass_surface, 1), 20), ((self.grass2_surface, 2), 20), ((self.grass3_surface, 3), 20),
                         ((self.forest_surface, 4), 15), ((self.mountain_surface, 5), 4), ((self.water_surface, 6), 3),
                         ((self.water2_surface, 7), 1), ((self.water3_surface, 8), 1),
                         ((self.willage_surface, 10), 0.7), ((self.mountain_pass_surface, 11), 2),
                         ((self.mountain2_surface, 12), 4),
                         ((self.forest_full_surface, 13), 0), ((self.forest3_surface, 14), 8),
                         ((self.forest4_surface, 15), 8),
                         ((self.castle_surface, 16), 0.7), ((self.clay, 17), 0.3), ((self.mine_diamonds, 18), 0.1),
                         ((self.fish_port, 19), 0.8), ((self.sawmill, 20), 0.5), ((self.grain, 21), 0.65),
                         ((self.mine_rocks, 22), 0.3), ((self.mine_iron, 23), 0.3), ((self.mine_gold, 24), 0.3)]

        self.num_hex_x = numx
        self.num_hex_y = numy
        self.num_hex_all = numx * numy
        self.allhex = {}
        self.alltex = {}
        self.screen = screen
        self.camera = camera
        self.allmask = {}
        self.allrect = {}
        self.camerax = self.camera.camera_x
        self.cameray = self.camera.camera_y
        self.tex_id = []
        # lista z surowcami, trzecie pole w kazdym rzedzie to "wartosc" tego pola
        self.surowce_lista = [(self.clay, "clay", 10), (self.mine_diamonds, "mine_diamonds", 200),
                              (self.mine_rocks, "mine_rocks", 60), (self.mine_iron, "mine_iron", 80),
                              (self.mine_gold, "mine_gold", 140), (self.fish_port, "fish_port", 20),
                              (self.sawmill, "sawmill", 40), (self.grain, "grain", 10)]
        self.visible_hex = {}

    def texture(self):

        for i in range(self.num_hex_y * self.num_hex_x):
            if i == 137:
                self.alltex['hex', i] = self.castle_surface

            else:
                self.tex_id += [random.choices(*zip(*self.elements), k=1)[0][1]]
                self.alltex['hex', i] = random.choices(*zip(*self.elements), k=1)[0]

    def generate(self):
        licz = 0
        przesuniecie_x = 0
        przesuniecie_y = 0
        self.texture()
        for j in range(self.num_hex_y):  # tworzenie hexów (jako nowy obiekt) nadawanie im położenia
            x = -1640
            y = j * 152
            for i in range(self.num_hex_x):

                # elif self.alltex["hex", licz] == self.castle_surface or self.alltex["hex", licz] == self.willage_surface:
                #     self.allhex["hex", licz] = Budynek((x + przesuniecie_x), (y + przesuniecie_y), self.alltex["hex", licz], licz, self, False, False,self.tex_id[licz])
                # else:
                self.allhex["hex", licz] = Hex((x + przesuniecie_x), (y + przesuniecie_y), licz, self, False, False,
                                               self.tex_id[licz])

                self.allrect['hex', licz] = self.allhex["hex", licz].texture.get_rect(
                    midleft=(self.allhex["hex", licz].polozenie_hex_x, self.allhex["hex", licz].polozenie_hex_y + 75))
                self.allmask['hex', licz] = pygame.mask.from_surface(self.allhex["hex", licz].texture)
                x += self.allhex["hex", licz].szerokosc
                # if self.allhex['hex',licz].rodzaj == 'surowiec':
                #     buff = self.zwroc_liste(licz)
                #     self.allhex["hex", licz] = Surowiec((x + przesuniecie_x),\
                #     (y + przesuniecie_y), self.alltex["hex", licz], licz, self, False, False,self.tex_id[licz]    )
                #     self.allhex["hex", licz].rodzaj_surowca(buff)
                if licz == 137:
                    self.allhex["hex", licz].zajete = True
                licz += 1

            if j % 2 != 0:
                przesuniecie_x = 0
            else:
                przesuniecie_x += -65
            przesuniecie_y += -38

    def Draw(self, width, height):  # wyświetlanie mapy na ekranie

        licznik = -1
        camera_x = self.camera.camera_x
        camera_y = self.camera.camera_y
        k = 0
        for h in self.sprites():
            licznik += 1
            position_x = h.polozenie_hex_x + camera_x
            if width > position_x > -200:
                position_y = h.polozenie_hex_y + camera_y
                if height > position_y > -200:
                    self.screen.blit(h.texture, (position_x, position_y))
                    self.visible_hex['hex', k] = licznik
                    k += 1



    def rysuj_obwodke_i_zajete(self):

        for i in self.sprites():
            if i.obwodka:
                self.screen.blit(self.hex_obwodka_surface, [i.polozenie_hex_x + self.camera.camera_x,
                                                            i.polozenie_hex_y + self.camera.camera_y])
            if i.zajete:
                self.screen.blit(self.hex_zajete_surface, (i.polozenie_hex_x + self.camera.camera_x,
                                                           i.polozenie_hex_y + self.camera.camera_y))

    def colision_detection_obwodka(self):
        pos = pygame.mouse.get_pos()

        if self.camerax != self.camera.camera_x or self.cameray != self.camera.camera_y:

            dx = self.camera.camera_x - self.camerax
            dy = self.camera.camera_y - self.cameray


            for rect in self.allrect.values():
                rect.x += dx
                rect.y += dy


            self.camerax = self.camera.camera_x
            self.cameray = self.camera.camera_y


        for c, rect in self.allrect.items():
            pos_in_mask = pos[0] - rect.x, pos[1] - rect.y

            if rect.collidepoint(*pos) and self.allmask[c].get_at(pos_in_mask):
                self.allhex[c].obwodka = True
            else:
                self.allhex[c].obwodka = False

    def zajmij_pole(self,player):
        import gameplay
        if player.player_hex_status:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                pos1 = pygame.mouse.get_pos()
                for i in range(self.num_hex_all):
                    pos_in_mask1 = pos1[0] - self.allrect['hex', i].x, pos1[1] - self.allrect['hex', i].y
                    touching = self.allrect['hex', i].collidepoint(*pos1) and self.allmask['hex', i].get_at(
                        pos_in_mask1)

                    if touching:
                        if self.allhex["hex", i].rodzaj == "surowiec":
                            print(self.allhex["hex", i].rodzaj_surowca_var)
                            gameplay.dopisz_surowiec(self.allhex["hex", i].rodzaj_surowca_var,player)
                        if self.allhex["hex", i].rodzaj == "budynek":
                            print("budynek")
                            # dodawanie bonusu do zarabiania
                            if self.allhex["hex", i].texture == self.castle_surface:
                                player.army_count_bonus += 10
                            elif self.allhex["hex", i].texture == self.willage_surface:
                                player.gold_count_bonus += 10
                        self.allhex["hex", i].zajete = True
                        player.player_hex_status = False
                        player.terrain_count += 1
                        if Player.ID == Player.MAX_ID-1:
                            Player.ID = 0
                        else:
                            Player.ID += 1


