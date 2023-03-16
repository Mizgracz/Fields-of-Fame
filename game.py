import pygame, sys
import function
import zmienne
import build

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
				if event.key == pygame.K_ESCAPE and zmienne.pause_menu_status == False:
					zmienne.pause_menu_status = True
					function.menu_pause()
				if event.key == pygame.K_b and zmienne.build_menu_status==False:
					print('BEGIN')
					zmienne.build_menu_status=True
					build.menu_build()
					print('END')
		pygame.display.update()
		zmienne.mainClock.tick(60)
