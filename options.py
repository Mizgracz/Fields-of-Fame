import pygame
import sys
import function
import zmienne

def setting_menu():
	print('F_BEGIN')
	zmiennatmp=True

	tmp_screen_center=zmienne.screen_center.copy()
	tmp_screen_center[0]-=zmienne.setting_surface.get_size()[0]/2
	tmp_screen_center[1]-=zmienne.setting_surface.get_size()[1]/2
	zmienne.CheckBox_True_surface =pygame.transform.scale(zmienne.CheckBox_True_surface, (20, 20))
	zmienne.CheckBox_False_surface =pygame.transform.scale(zmienne.CheckBox_False_surface, (20, 20))
	
	box = pygame.Rect((tmp_screen_center[0]+10)+100,tmp_screen_center[1]+10*5, 20, 20)
	exit = pygame.Rect(tmp_screen_center[0]+zmienne.button_exit_surface.get_size()[0]/2,tmp_screen_center[1]+zmienne.setting_surface.get_size()[1]-zmienne.button_exit_surface.get_size()[1], zmienne.button_exit_surface.get_size()[0], zmienne.button_exit_surface.get_size()[1])
	
	while zmiennatmp:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					zmienne.click = True

		zmienne.screen.blit(zmienne.setting_surface, tmp_screen_center)
		function.draw_text("OPCJE",function.font,(0,0,255),zmienne.screen,tmp_screen_center[0]+10,tmp_screen_center[1]+10)
		
		function.draw_text("Muzyka",function.font,(0,0,255),zmienne.screen,tmp_screen_center[0]+10,tmp_screen_center[1]+10*5)
		
		if zmienne.music_status:
			zmienne.screen.blit(zmienne.CheckBox_True_surface, (tmp_screen_center[0]+10+100,tmp_screen_center[1]+10*5))
		else:
			zmienne.screen.blit(zmienne.CheckBox_False_surface, (tmp_screen_center[0]+10+100,tmp_screen_center[1]+10*5))

		zmienne.screen.blit(zmienne.button_exit_surface, (tmp_screen_center[0]+zmienne.button_exit_surface.get_size()[0]/2,tmp_screen_center[1]+zmienne.setting_surface.get_size()[1]-zmienne.button_exit_surface.get_size()[1]))
		
		mx, my = pygame.mouse.get_pos()


		if box.collidepoint((mx, my)):
			if zmienne.click:
				if  zmienne.music_status:
					zmienne.click=False
					zmienne.music_status=False
				else:
					zmienne.music_status=True
		if exit.collidepoint((mx, my)):
			if zmienne.click:
				zmienne.click=False
				zmiennatmp=False

		function.draw_text("OPCJE2",function.font,(0,0,255),zmienne.screen,tmp_screen_center[0]+10,tmp_screen_center[1]+10*7)
		pygame.display.update()
		zmienne.mainClock.tick(60)
		zmienne.click = False
	print(f'F_END {0}')
	pass