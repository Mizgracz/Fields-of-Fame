import pygame, sys
import function
import zmienne


def gameloop():

    while zmienne.game_status:

        function.draw()
        function.playe_hex()
        zmienne.screen.blit(zmienne.up_bar, (0, 0))
        function.score()
        function.decision()
        function.keyboard()
        function.mouse()
        function.turn()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and zmienne.menu_p_bool == False:
                    zmienne.menu_p_bool = True
                    function.menu_pause()
        pygame.display.update()
        function.mainClock.tick(60)
