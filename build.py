import zmienne
import pygame
import function
import sys



def menu_build():
	print('F_BEGIN')
	menu_b_surface = pygame.image.load('tekstury/ekran.png')
	menu_b_surface = pygame.transform.scale(menu_b_surface, (zmienne.res[0]/2, zmienne.res[1]/2))
	


	while zmienne.build_menu_status:
		zmienne.screen.blit(menu_b_surface, (0+zmienne.res[0]/4, 0+zmienne.res[1]/4))
		function.draw_text("MENU BUDOWANIA",function.font,(0,0,255),zmienne.screen,zmienne.res[0]/4,zmienne.res[1]/4)
		zmienne.screen.blit(zmienne.build1, (zmienne.res[0]/4+10,zmienne.res[1]/4+50))
		zmienne.screen.blit(zmienne.build2, (zmienne.res[0]/4+10+150,zmienne.res[1]/4+50))
		zmienne.screen.blit(zmienne.build3, (zmienne.res[0]/4+10+150*2,zmienne.res[1]/4+50))
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					zmienne.build_menu_status=False
		pygame.display.update()
		zmienne.mainClock.tick(60)
	print('F_END')
	pass