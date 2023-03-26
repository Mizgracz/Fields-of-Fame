import pygame
import zmienne
import timer

# set the size and color of the gray box

gray_mainbox_width = 256
gray_mainbox_height = 690
gray_mainbox_color = (161, 113, 33)  # this is a tuple representing RGB values

gray_upperbox_width = 236
gray_upperbox_height = 238
gray_upperbox_color = (196, 166, 116)

gray_middlebox_width = 236
gray_middlebox_height = 144
gray_middlebox_color = (33, 161, 113)

gray_bottombox_width = 236
gray_bottombox_height = 268
gray_bottombox_color = (196, 166, 116)

gray_box = pygame.Surface((gray_mainbox_width, gray_mainbox_height))
upper_box = pygame.Surface((gray_upperbox_width, gray_upperbox_height))
middle_box = pygame.Surface((gray_middlebox_width, gray_middlebox_height))
bottom_box = pygame.Surface((gray_bottombox_width, gray_bottombox_height))



# get the coordinates to position the gray box on the right side of the screen
gray_box_x = zmienne.res[0] - gray_mainbox_width
gray_box_y = 30

upper_box_x = zmienne.res[0] - gray_mainbox_width + 10
upper_box_y = + 40

middle_box_x = zmienne.res[0] - gray_mainbox_width + 10
middle_box_y = gray_upperbox_height + 50

bottom_box_x = zmienne.res[0] - gray_mainbox_width + 10
bottom_box_y = zmienne.res[1] - gray_bottombox_height - 10

middle_box_rect = middle_box.get_rect(topleft =(middle_box_x, middle_box_y) )

def praweUI():
    FONT_SIZE = 50
    FONT_NAME = 'timesnewroman'

   

    # create a Surface object for the gray box
    gray_box.fill(gray_mainbox_color)

    upper_box.fill(gray_upperbox_color)

    middle_box.fill(gray_middlebox_color)
    

    bottom_box.fill(gray_bottombox_color)

    # Tekst dla upper_box

    upper_box_font = pygame.font.SysFont(FONT_NAME, 20)
    upper_box_text = upper_box_font.render("Tutaj będą surowce", True, (255, 255, 255))
    upper_box_text_rect = upper_box_text.get_rect(center=(gray_upperbox_width // 2, gray_upperbox_height // 2))
    upper_box.blit(upper_box_text, upper_box_text_rect)

    # Tekst dla middle_box

    middle_box_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    middle_box_text = middle_box_font.render("BUDYNKI", True, (255, 255, 255))
    middle_box_text_rect = middle_box_text.get_rect(center=(gray_middlebox_width // 2, gray_middlebox_height // 2))

    middle_box.blit(middle_box_text, middle_box_text_rect)

    # Tekst dla bottom_box

    bottom_box_font = pygame.font.SysFont(FONT_NAME, 20)
    bottom_box_text = bottom_box_font.render("Tutaj będzie opis", True, (255, 255, 255))
    bottom_box_text_rect = bottom_box_text.get_rect(center=(gray_bottombox_width // 2, gray_bottombox_height // 2))
    bottom_box.blit(bottom_box_text, upper_box_text_rect)



    # draw the gray box onto the screen
    zmienne.screen.blit(gray_box, (gray_box_x, gray_box_y))

    zmienne.screen.blit(upper_box, (upper_box_x, upper_box_y))

    zmienne.screen.blit(middle_box, (middle_box_x, middle_box_y))

    zmienne.screen.blit(bottom_box, (bottom_box_x, bottom_box_y))
    
    
    timer.timer()

    pygame.display.update()
