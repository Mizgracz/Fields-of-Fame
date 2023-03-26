import pygame
import time
import zmienne
# Set up the window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
# Set up the font

# Set up the timer
start_time = time.time()
seconds = 0
elapsed_time = 0
def timer():
    FONT_SIZE = 36
    FONT_NAME = 'timesnewroman'
    font_2 = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    # Update the timer
    current_time = time.time()
    elapsed_time = current_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)

    # Draw the timer box
    timer_box = pygame.Rect(zmienne.res[0]-200, zmienne.res[1]-80, 180, 60)
    pygame.draw.rect(zmienne.screen, (255, 255, 255), timer_box)
    pygame.draw.rect(zmienne.screen, (0, 0, 0), timer_box, 2)

    # Draw the timer text
    timer_text = font_2.render('{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds), True, (0, 0, 0))
    text_rect = timer_text.get_rect(center=timer_box.center)
    zmienne.screen.blit(timer_text, text_rect)

    # Update the display
    pygame.display.update()
    zmienne.mainClock.tick(60)

