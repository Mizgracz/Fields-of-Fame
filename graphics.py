

import pygame

import random
from gameplay import Stats


class Hex(pygame.sprite.Sprite):

    def __init__(self, x, y, tex , num, group, obw, zaj,tex_id):
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
        if self.number == 137:
            self.zajete =True
    def texturing(self,group):
        if self.number ==137:
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
            return group.dirt_surface
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
    def update_texture(self):
        self.texture = self.texturing(self.group)

class Map(pygame.sprite.Group):

    def __init__(self, numx, numy, screen, camera):
        super().__init__()

        self.colision_surface = pygame.Surface(pygame.display.get_window_size(), pygame.SRCALPHA)
        self.colision_rect = self.colision_surface.get_rect()

        self.hex_obwodka_surface = pygame.image.load("texture/hex/hex_obwodka.png").convert_alpha()

        self.hex_zajete_surface = pygame.image.load("texture/hex/hex_zajete_pole.png").convert_alpha()
        self.hex_zajete_surface.set_alpha(100)

        self.grass_surface = pygame.image.load("texture/hex/hex_trawa.png", ).convert_alpha()
        self.grass2_surface = pygame.image.load("texture/hex/trawa_hex_2.png", ).convert_alpha()
        self.grass3_surface = pygame.image.load("texture/hex/trawa_hex_3.png").convert_alpha()
        self.dirt_surface = pygame.image.load("texture/hex/budynki.png").convert_alpha()
        self.cereal_surface = pygame.image.load("texture/hex/zboze_hex.png").convert_alpha()
        self.castle_surface = pygame.image.load("texture/hex/zamek.png", ).convert_alpha()

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

        self.elements = [((self.grass_surface,1), 20), ((self.grass2_surface,2), 20), ((self.grass3_surface,3), 20),
                         ((self.forest_surface,4), 15), ((self.mountain_surface,5), 4), ((self.water_surface,6), 3),
                         ((self.water2_surface,7), 1), ((self.water3_surface,8), 1), ((self.cereal_surface,9), 1),
                         ((self.dirt_surface,10), 0.5), ((self.mountain_pass_surface,11), 2), ((self.mountain2_surface,12), 4),
                         ((self.forest_full_surface,13), 0), ((self.forest3_surface,14), 8), ((self.forest4_surface,15), 8)]

        self.num_hex_x = numx
        self.num_hex_y = numy
        self.allhex = {}
        self.alltex = {}
        self.screen = screen
        self.camera = camera
        self.allmask = {}
        self.allrect = {}
        self.camerax = self.camera.camera_x
        self.cameray = self.camera.camera_y
        self.tex_id = []
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
            x = -1625
            y = (j * 152) - 10
            for i in range(self.num_hex_x):
                
                self.allhex["hex", licz] = Hex((x + przesuniecie_x), (y + przesuniecie_y), self.alltex["hex", licz],licz, self, False, False,self.tex_id[licz])

                self.allrect['hex', licz] = self.allhex["hex", licz].texture.get_rect(midleft=(self.allhex["hex", licz].polozenie_hex_x, self.allhex["hex", licz].polozenie_hex_y + 75))
                self.allmask['hex', licz] = pygame.mask.from_surface(self.allhex["hex", licz].texture)
                x += self.allhex["hex", licz].szerokosc

                
                licz += 1

            if j % 2 != 0:
                przesuniecie_x = 0
            else:
                przesuniecie_x += -65
            przesuniecie_y += -40

    def draw(self):  # wyświetlanie mapy na ekranie
        for h in self.sprites():
            self.screen.blit(h.texture, (h.polozenie_hex_x + self.camera.camera_x, h.polozenie_hex_y + 
                                         self.camera.camera_y))
            


    def rysuj_obwodke_i_zajete(self):
        for i in range(self.num_hex_y * self.num_hex_y):
            if self.allhex["hex", i].obwodka:
                self.screen.blit(self.hex_obwodka_surface, (self.allhex["hex", i].polozenie_hex_x + self.camera.camera_x,
                                                            self.allhex["hex", i].polozenie_hex_y + self.camera.camera_y))
            if self.allhex["hex", i].zajete:
                self.screen.blit(self.hex_zajete_surface, (self.allhex["hex", i].polozenie_hex_x + self.camera.camera_x,
                                                            self.allhex["hex", i].polozenie_hex_y + self.camera.camera_y))
    
    def colision_detection_obwodka(self):
        pos = pygame.mouse.get_pos()
        for c in range(self.num_hex_y * self.num_hex_x):

            if self.camerax != self.camera.camera_x:
                for ca in range(self.num_hex_y * self.num_hex_x):
                    if self.camerax < self.camera.camera_x:
                        div = self.camera.camera_x - self.camerax
                        self.allrect['hex', ca].x += div
                    else:
                        div = self.camerax - self.camera.camera_x
                        self.allrect['hex', ca].x -= div

            if self.cameray != self.camera.camera_y:
                for co in range(self.num_hex_y * self.num_hex_x):
                    if self.cameray < self.camera.camera_y:
                        div = self.camera.camera_y - self.cameray
                        self.allrect['hex', co].y += div
                    else:
                        div = self.cameray - self.camera.camera_y
                        self.allrect['hex', co].y -= div

            self.camerax = self.camera.camera_x
            self.cameray = self.camera.camera_y

            pos_in_mask = pos[0] - self.allrect['hex', c].x, pos[1] - self.allrect['hex', c].y
            try:

                touching = self.allrect['hex', c].collidepoint(*pos) and self.allmask['hex', c].get_at(pos_in_mask)
                if touching:

                    self.allhex["hex", c].obwodka = True

                else:
                    
                    self.allhex["hex", c].obwodka = False

            except IndexError as e:
                print("Wystąpił błąd :", e)

    def zajmij_pole(self):
        if Stats.player_hex_status:
            mouse_presses = pygame.mouse.get_pressed()

            if mouse_presses[0]:
                pos1 = pygame.mouse.get_pos()
                for i in range(self.num_hex_y * self.num_hex_x):
                    pos_in_mask1 = pos1[0] - self.allrect['hex', i].x, pos1[1] - self.allrect['hex', i].y
                    touching = self.allrect['hex', i].collidepoint(*pos1) and self.allmask['hex', i].get_at(pos_in_mask1)

                    if touching:
                        self.allhex["hex", i].zajete = True
                        Stats.player_hex_status = False
                        Stats.terrain_count += 1
