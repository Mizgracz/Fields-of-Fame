import pygame
import random


class Hex(pygame.sprite.Sprite):

    def __init__(self, x, y, num, group):
        super().__init__(group)
        self.group = group
        self.szerokosc = 130
        self.wysokosc = 152
        self.polozenie_hex_x = x
        self.polozenie_hex_y = y
        self.number = num
        self.texture_index =  random.choices(*zip(*group.elements), k=1)[0][1]
        self.texture = self.texturing(group)
        self.type = None
        self.verticles = [
            (self.polozenie_hex_x + self.szerokosc / 2 + group.camera.camera_x,
             self.polozenie_hex_y + 30 + group.camera.camera_y),
            (self.polozenie_hex_x + self.szerokosc + group.camera.camera_x,
             self.polozenie_hex_y + self.wysokosc / 4 + 30 + group.camera.camera_y),
            (self.polozenie_hex_x + self.szerokosc + group.camera.camera_x,
             self.polozenie_hex_y + self.wysokosc - self.wysokosc / 4 + 30 + group.camera.camera_y),
            (self.polozenie_hex_x + self.szerokosc / 2 + group.camera.camera_x,
             self.polozenie_hex_y + self.wysokosc + 30 + group.camera.camera_y),
            (self.polozenie_hex_x + group.camera.camera_x,
             self.polozenie_hex_y + self.wysokosc - self.wysokosc / 4 + 30 + group.camera.camera_y),
            (self.polozenie_hex_x + group.camera.camera_x,
             self.polozenie_hex_y + self.wysokosc / 4 + 30 + group.camera.camera_y),
        ]
        self.verticles_texture = [
            (self.szerokosc / 2, 0),  # v1
            (self.szerokosc, self.wysokosc / 4),  # v2
            (self.szerokosc, self.wysokosc - self.wysokosc / 4),  # v2
            (self.szerokosc / 2, self.wysokosc),  # v4
            (0, self.wysokosc - self.wysokosc / 4),  # v2
            (0, self.wysokosc / 4),  # v2
        ]

        self.owner_color = pygame.Surface((130, 152), pygame.SRCALPHA)
        self.owner_rect = self.owner_color.get_rect(topleft=(self.polozenie_hex_x, self.polozenie_hex_y))
        self.owner_color.set_alpha(255 * (30 / 100))
        if self.number == 137:
            pygame.draw.polygon(self.owner_color, (255, 13, 16), self.verticles_texture)
        self.texture.blit(self.owner_color, (0, 0))
        
    def update_texture(self):
        self.texture = self.texturing(self.group)
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
class Map(pygame.sprite.Group):

    def __init__(self, numx, numy, screen, camera):
        super().__init__()

        self.colision_surface = pygame.Surface(pygame.display.get_window_size(), pygame.SRCALPHA)
        self.colision_rect = self.colision_surface.get_rect()

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


    def generate(self):
        licz = 0
        przesuniecie_x = 0
        przesuniecie_y = 0

        for j in range(self.num_hex_y):  # tworzenie hexów (jako nowy obiekt) nadawanie im położenia
            x = -1640
            y = j * 152
            for i in range(self.num_hex_x):
                self.allhex["hex", licz] = Hex((x + przesuniecie_x), (y + przesuniecie_y), licz, self)

                x += self.allhex["hex", licz].szerokosc
                licz += 1

            if j % 2 != 0:
                przesuniecie_x = 0
            else:
                przesuniecie_x += -65
            przesuniecie_y += -40

    def draw(self):  # wyświetlanie mapy na ekranie

        for h in self.sprites():
            self.screen.blit(h.texture,
                             (h.polozenie_hex_x + self.camera.camera_x, h.polozenie_hex_y + self.camera.camera_y))
