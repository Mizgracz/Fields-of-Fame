import sys
import pygame
# import function
# import zmienne
import Hexagon
import random

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
pygame.event.set_grab(True)

camera = Hexagon.CameraGroup()

hexagonImage = {
	'castle':'tekstury/castle.png',
	'grass':'tekstury/grass.png',
	'forest':'tekstury/forest.png',
	'village':'tekstury/village.png',
	'water':'tekstury/water.png',
}
random.seed()
def map_gen(width,height):
	przesuniecie_x =0
	przesuniecie_y =0
	offset_x = 0
	offset_y = 0
	# for h in range(height):
	for h in range(height):
		if  h%2==0:
			offset_x=0
		else:
			offset_x=-64
			pass

		for w in range(width):
			rnd = random.randint(1,5)
			if rnd != 1:
				tmpI = 'grass'
			else:
				tmpI='water'
			Hexagon.hexagon((przesuniecie_x+offset_x,przesuniecie_y+offset_y),camera,hexagonImage[tmpI])
			# print(przesuniecie_x+offset_x,przesuniecie_y+offset_y)
			przesuniecie_x +=128
		przesuniecie_x = 0
		przesuniecie_y +=128
		offset_y -=128/8

map_gen(30,30)
while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
		if event.type == pygame.MOUSEWHEEL:
			camera.zoom_scale += event.y * 0.03

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

	screen.fill('#71ddee')
	camera.update()
	camera.custom_draw()


	# function.menu_start()
	pygame.display.update()
	clock.tick(60)
