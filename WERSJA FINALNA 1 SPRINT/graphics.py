import pygame
import random


class Hex:
    def __init__(self, x, y, tex, num):
        self.szerokosc = 130
        self.wysokosc = 152
        self.polozenie_hex_x = x
        self.polozenie_hex_y = y
        self.texture = tex
        self.type = None
        self.number = num


class Map:

    def __init__(self, numx, numy):

        self.grass_surface = pygame.image.load("hex_trawa.png", ).convert_alpha()
        self.grass2_surface = pygame.image.load("trawa_hex_2.png", ).convert_alpha()
        self.grass3_surface = pygame.image.load("trawa_hex_3.png").convert_alpha()
        self.dirt_surface = pygame.image.load("budynki.png").convert_alpha()
        self.cereal_surface = pygame.image.load("zboze_hex.png").convert_alpha()
        self.castle_surface = pygame.image.load("zamek.png", ).convert_alpha()
        self.forest_surface = pygame.image.load("las_hex.png", ).convert_alpha()
        self.mountain_surface = pygame.image.load("gory_hex.png", ).convert_alpha()
        self.water_surface = pygame.image.load("woda_hex_1.png", ).convert_alpha()
        self.water2_surface = pygame.image.load("woda_hex_2.png", ).convert_alpha()
        self.water3_surface = pygame.image.load("woda_hex_statek.png", ).convert_alpha()

        self.elements = [(self.grass_surface, 20),  (self.grass2_surface, 20),   (self.grass3_surface, 20),
                         (self.forest_surface, 30), (self.mountain_surface, 10), (self.water_surface, 3),
                         (self.water2_surface, 1),  (self.water3_surface, 1),    (self.cereal_surface, 8),
                         (self.dirt_surface, 1)]

        self.num_hex_x = numx
        self.num_hex_y = numy
        self.allhex = {}
        self.alltex = {}

    def texture(self):

        for i in range(self.num_hex_y * self.num_hex_x):
            if i == 137:
                self.alltex['hex', i] = self.castle_surface
            else:
                self.alltex['hex', i] = random.choices(*zip(*self.elements), k=1)[0]
            print()

    def generate(self):
        licz = 0
        przesuniecie_x = 0
        przesuniecie_y = 0

        for j in range(self.num_hex_y):  # tworzenie hexów (jako nowy obiekt) nadawanie im położenia
            x = -1640
            y = j * 152
            for i in range(self.num_hex_x):
                self.allhex["hex", licz] = Hex((x + przesuniecie_x), (y + przesuniecie_y), self.alltex["hex", licz], licz)
                x += self.allhex["hex", licz].szerokosc
                licz += 1

            if j % 2 != 0:
                przesuniecie_x = 0
            else:
                przesuniecie_x += -65
            przesuniecie_y += -40

    def draw(self, screen, camera):  # wyświetlanie mapy na ekranie

        for h in self.allhex.values():
            screen.blit(h.texture, (h.polozenie_hex_x + camera.camera_x, h.polozenie_hex_y + camera.camera_y))

    # def decision():
    #
    #
    #     if wyb:
    #
    #         dec_rect = imageDEC_surface.get_rect(center=(640, 360))
    #         button1_rect = button1_surface.get_rect(midleft=(670, 360))
    #         button2_rect = button2_surface.get_rect(midright=(610, 360))
    #         screen.blit(imageDEC_surface, dec_rect)
    #         screen.blit(button1_surface, button1_rect)
    #         screen.blit(button2_surface, button2_rect)
    #         colision = pygame.mouse.get_pos()
    #         mouse_pressed = pygame.mouse.get_pressed()
    #         if button1_rect.collidepoint(colision) and mouse_pressed[0]:
    #             m_score += 10
    #             wyb = False
    #         if button2_rect.collidepoint(colision) and mouse_pressed[0]:
    #             a_score += 10
    #             wyb = False
    #
    # def turn():
    #     global wyb
    #     turn_rect = button3_surface.get_rect(center=(100, 600))
    #     screen.blit(button3_surface, turn_rect)
    #     colision = pygame.mouse.get_pos()
    #     mouse_pressed = pygame.mouse.get_pressed()
    #     if turn_rect.collidepoint(colision) and mouse_pressed[0]:
    #         wyb = True

