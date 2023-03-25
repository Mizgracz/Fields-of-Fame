import pygame
import random
import math

class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg
        

class Map(pygame.sprite.Group):
    def __init__(self, numx, numy,screen):
        super().__init__()
        self.screen = screen
        self.grass_surface = pygame.image.load("tekstury/trawa_hex.png", ).convert_alpha()
        self.num_hex_x = numx
        self.num_hex_y = numy
        self.allhex = {}
        self.alltex = {}

    def texture(self):
        for i in range (self.num_hex_y * self.num_hex_x):
            print()
    def generate(self):

        licz = 0
        przesuniecie_x = 0
        przesuniecie_y = 0
        for j in range(self.num_hex_y):  # tworzenie hexów (jako nowy obiekt) nadawanie im położenia oraz tekstury
            x = -1640*0
            y = j * 152
            for i in range(self.num_hex_x):
                self.allhex["hex", licz] = Hex((x + przesuniecie_x), (y + przesuniecie_y), self.grass_surface, licz,self)
                x += self.allhex["hex", licz].szerokosc
                licz += 1

            if j % 2 != 0:
                przesuniecie_x = 0
            else:
                przesuniecie_x += -64
            przesuniecie_y += -38  #

    def draw(self):  # wyświetlanie mapy na ekranie
        self.s = pygame.Surface((self.num_hex_x*130.,self.num_hex_y*152))
        self.s.fill('#ffffff')
        for h in self.sprites():
            self.s.blit(h.texture, (h.polozenie_hex_x, h.polozenie_hex_y))
            
            # self.s.blit(h.owner, (h.polozenie_hex_x, h.polozenie_hex_y))
        self.screen.blit(self.s,(0,0))
class Hex(pygame.sprite.Sprite):
    def __init__(self, x, y, tex, num,group):
        super().__init__(group)
        self.szerokosc = 130
        self.wysokosc = 152
        self.polozenie_hex_x = x
        self.polozenie_hex_y = y
        self.texture = pygame.image.load("tekstury/trawa_hex.png", ).convert_alpha()
        self.verticles = [
        (self.polozenie_hex_x+self.szerokosc/2,self.polozenie_hex_y),#v1
        (self.polozenie_hex_x+self.szerokosc,self.polozenie_hex_y+self.wysokosc/4),#v2
        (self.polozenie_hex_x+self.szerokosc,self.polozenie_hex_y+self.wysokosc-self.wysokosc/4),#v2
        (self.polozenie_hex_x+self.szerokosc/2,self.polozenie_hex_y+self.wysokosc),#v4
        (self.polozenie_hex_x,self.polozenie_hex_y+self.wysokosc-self.wysokosc/4),#v2
        (self.polozenie_hex_x,self.polozenie_hex_y+self.wysokosc/4),#v2
        ]
        self.verticles_texture = [
        (self.szerokosc/2,0),#v1
        (self.szerokosc,self.wysokosc/4),#v2
        (self.szerokosc,self.wysokosc-self.wysokosc/4),#v2
        (self.szerokosc/2,self.wysokosc),#v4
        (0,self.wysokosc-self.wysokosc/4),#v2
        (0,self.wysokosc/4),#v2
        ]
        self.rect = self.texture.get_rect(topleft=(self.polozenie_hex_x , self.polozenie_hex_y))
        self.owner =pygame.Surface((130,152),pygame.SRCALPHA)

        self.owner_rect = self.owner.get_rect(topleft = (self.polozenie_hex_x , self.polozenie_hex_y) )
        
        # self.owner.blit(self.texture,(0,0))
        
        self.owner.set_alpha(255*(30/100))
        self.texture.blit(self.owner,(0,0))

        self.type = None
        self.number = num


    def is_point_inside_polygon(self,point):
        """
        Testuje, czy punkt znajduje się wewnątrz wielokąta o zadanych wierzchołkach.
        """
        # Obliczenie pola wielokąta
        polygon_area = 0
        n = len(self.verticles)
        for i in range(n):
            j = (i + 1) % n
            polygon_area += self.verticles[i][0] * self.verticles[j][1] - self.verticles[j][0] * self.verticles[i][1]
        polygon_area /= 2

        # Obliczenie sumy pól trójkątów tworzących wielokąt i punkt
        point_area = 0
        for i in range(n):
            j = (i + 1) % n
            triangle_area = abs(point[0] * self.verticles[i][1] + self.verticles[i][0] * self.verticles[j][1] + self.verticles[j][0] * point[1] -
                                point[1] * self.verticles[i][0] - self.verticles[i][1] * self.verticles[j][0] - self.verticles[j][1] * point[0]) / 2
            point_area += triangle_area

        # Jeśli suma pól trójkątów jest równa polu wielokąta, to punkt znajduje się wewnątrz
        return point_area == polygon_area
    def function(self,group):
        if self.type !='Player':
            print('Y:',self.polozenie_hex_y,'X:',self.polozenie_hex_x)
            group.screen.fill('#ffffff')
            group.draw()
            polygon = pygame.draw.polygon(self.owner, (0,255,0), self.verticles_texture)
            
            self.texture.blit(self.owner,(0,0))
            # self.owner.set_alpha(128)
            self.type = 'Player'
            group.s.blit(self.owner,self.owner_rect)
            group.screen.blit(group.s,(0,0))
        else:
            print('Posiadasz to pole')
            # print(group.num_hex_x)
