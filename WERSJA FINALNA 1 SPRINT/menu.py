import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Menu:
    def __init__(self, screen, clock, max_tps):
        self.screen = screen
        self.clock = clock
        self.max_tps = max_tps
        self.font = pygame.font.Font(None, 48)
        self.new_game_button = pygame.Rect(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2-50, 200, 100)
        self.quit_button = pygame.Rect(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2+100, 200, 100)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.new_game_button.collidepoint(pos):
                    return 'new_game'
                elif self.quit_button.collidepoint(pos):
                    return 'quit'

    def draw(self):
        self.screen.fill((0, 0, 0)) # kolor tła menu - w tym przypadku czarne
        new_game_text = self.font.render('New Game', True, (255, 255, 255)) # kolor tekstu przycisku
        pygame.draw.rect(self.screen, (0, 0, 255), self.new_game_button) # kolor tła przycisku - w tym przypadku niebieski
        self.screen.blit(new_game_text, (self.new_game_button.centerx - new_game_text.get_width()/2, self.new_game_button.centery - new_game_text.get_height()/2))
        quit_text = self.font.render('Quit', True, (255, 255, 255)) # kolor tekstu przycisku
        pygame.draw.rect(self.screen, (0, 0, 255), self.quit_button) # kolor tła przycisku - w tym przypadku niebieski
        self.screen.blit(quit_text, (self.quit_button.centerx - quit_text.get_width()/2, self.quit_button.centery - quit_text.get_height()/2))
        pygame.display.flip()

    def run(self):
        while True:
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
