import sys
import pygame
import function

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)

	function.menu_start()
	pygame.display.update()
	zmienne.mainClock.tick(60)
