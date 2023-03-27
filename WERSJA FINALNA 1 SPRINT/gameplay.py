import pygame

gold_count = 0
army_count = 0
terrain_count = 1
wyb = True

class Camera:

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.camera_x = 0
        self.camera_y = 0

        self.mouse_x = 0
        self.mouse_y = 0

    def mouse(self):

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        predkosc = 2
        press = pygame.key.get_pressed()
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
                self.camera_y += predkosc +10
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

    def __init__(self,screen):

        self.up_bar_surface = pygame.Surface((1280, 30))
        self.up_bar_surface.fill("black")
        self.screen = screen

    def score(self):

        self.up_bar_surface.fill((0, 0, 0))
        # money
        money = pygame.font.Font(None, 25)
        money_score = money.render("Ilość Złota: " + str(gold_count), False, "white")
        self.up_bar_surface.blit(money_score, (10, 6))
        # wojsko
        army = pygame.font.Font(None, 25)
        army_score = army.render("Ilość Wojska: " + str(army_count), False, "white")
        self.up_bar_surface.blit(army_score, (160, 6))
        # pola
        tiles = pygame.font.Font(None, 25)
        tiles_score = tiles.render("Ilość Posiadanych Pól: " + str(terrain_count), False, "white")
        self.up_bar_surface.blit(tiles_score, (310, 6))

        # Wyświetlenie powierzchni górnej belki na ekranie
        self.screen.blit(self.up_bar_surface, (0, 0))


class Hourglass:

    def __init__(self, screen):

        self.hourglass_surface = pygame.transform.scale((pygame.image.load("klepsydra_button-removebg-preview.jpg")), (173, 184))
        self.hourglass_rect = self.hourglass_surface.get_rect(center=(100, 600))
        self.screen = screen


    def draw(self):
        self.screen.blit(self.hourglass_surface, self.hourglass_rect)

    def turn(self):
        global wyb
        colision = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.hourglass_rect.collidepoint(colision) and mouse_pressed[0]:
            wyb = True


class Decision:
    def __init__(self, screen):
        self.army_button = pygame.image.load("wojsko_button.png").convert_alpha()
        self.gold_button = pygame.image.load("zloto_button.png").convert_alpha()

        self.gold_rect = self.gold_button.get_rect(midright = (630,360))
        self.army_rect = self.army_button.get_rect(midleft = (700,360))
        self.screen = screen

    def draw(self):
        if wyb:
            self.screen.blit(self.gold_button, self.gold_rect)
            self.screen.blit(self.army_button, self.army_rect)

    def click(self):
        global gold_count
        global wyb
        global army_count

        colision = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.gold_rect.collidepoint(colision) and mouse_pressed[0] and wyb:
            wyb = False

            gold_count += 10

        if self.army_rect.collidepoint(colision) and mouse_pressed[0] and wyb:
            wyb = False

            army_count += 10
