import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Menu:
    def __init__(self, screen, clock, max_tps):
        self.screen = screen
        self.clock = clock
        self.max_tps = max_tps
        self.status = True
        self.resume = False
        self.font = pygame.font.Font(None, 48)
        self.new_game_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 120, 200, 100)
        self.quit_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 120, 200, 100)
        self.background_texture = pygame.image.load("texture/main_menu/background.png").convert()
        self.new_game_button_texture = pygame.image.load("texture/main_menu/graj_button.png").convert_alpha()
        self.resume_game_button_texture = pygame.image.load("texture/main_menu/wznow_button.png").convert_alpha()
        self.quit_button_texture = pygame.image.load("texture/main_menu/zamknij_button.png").convert_alpha()
        self.load_button_texture = pygame.image.load("texture/main_menu/wczytaj_button.png").convert_alpha()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.new_game_button.collidepoint(pos):
                    self.status = False
                    self.resume = True
                    return 'new_game'
                elif self.quit_button.collidepoint(pos):
                    self.status = False
                    return 'quit'

    def draw(self):
        self.screen.blit(self.background_texture, (0, 0))
        self.screen.blit(self.load_button_texture, (SCREEN_WIDTH / 2 - 150, 360))
        if self.resume:
            button_texture = self.resume_game_button_texture
        else:
            button_texture = self.new_game_button_texture
        self.screen.blit(button_texture, self.new_game_button)

        quit_texture = self.quit_button_texture
        self.screen.blit(quit_texture, self.quit_button)

        pygame.display.flip()

    def run(self):
        choice = self.handle_events()
        if choice:
            return choice
        self.draw()
        self.clock.tick(self.max_tps)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
max_tps = 60.0

menu1 = Menu(screen, clock, max_tps)
menu1.run()
