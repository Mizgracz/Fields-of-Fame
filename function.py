import random
import pygame,sys
import game
import zmienne
import build
import options

pygame.init()

zmienne.screen.fill((255, 255, 255))
clock = pygame.time.Clock()

# ticking


for j in range(0, zmienne.hex_num_y):

	zmienne.wysokosc_hex = 128 * j
	zmienne.szerokosc_hex = 0

	for i in range(zmienne.hex_num_x):
		zmienne.hex_x["hex", zmienne.licz] = zmienne.szerokosc_hex + zmienne.przesuniecie_x
		zmienne.hex_y["hex", zmienne.licz] = zmienne.wysokosc_hex + zmienne.przesuniecie_y
		if zmienne.szerokosc_hex == 595 and zmienne.wysokosc_hex == 384:
			zmienne.hex_surf["hex", zmienne.licz] = 101
		else:
			zmienne.hex_surf["hex", zmienne.licz] = random.randint(0, 100)
		zmienne.szerokosc_hex += 119
		zmienne.licz += 1

	if j % 2 != 0:
		zmienne.przesuniecie_x = 0
	else:
		zmienne.przesuniecie_x += -60

	zmienne.przesuniecie_y += -30


def draw():
	zmienne.screen.fill((255, 255, 255))
	for d in range(0, zmienne.hex_num):

		if zmienne.hex_surf["hex", d] == 101:
			zmienne.screen.blit(zmienne.castle_surface, (zmienne.hex_x["hex", d], zmienne.hex_y["hex", d]))

		elif zmienne.hex_surf["hex", d] < 20:
			zmienne.screen.blit(zmienne.water_surface, (zmienne.hex_x["hex", d], zmienne.hex_y["hex", d]))

		elif 19 < zmienne.hex_surf["hex", d] < 50:
			zmienne.screen.blit(zmienne.forest_surface, (zmienne.hex_x["hex", d], zmienne.hex_y["hex", d]))

		elif 101 > zmienne.hex_surf["hex", d] > 95:
			zmienne.screen.blit(zmienne.village_surface, (zmienne.hex_x["hex", d], zmienne.hex_y["hex", d]))

		else:
			zmienne.screen.blit(zmienne.grass_surface, (zmienne.hex_x["hex", d], zmienne.hex_y["hex", d]))


def mouse():
	mouse_x, mouse_y = pygame.mouse.get_pos()
	if mouse_y > 50:
		zmienne.camy -= 5
		for MY1 in range(0, zmienne.hex_num):
			zmienne.hex_y["hex", MY1] -= 5

	if mouse_y < 720 - 50:
		zmienne.camy += 5
		for MY2 in range(0, zmienne.hex_num):
			zmienne.hex_y["hex", MY2] += 5
	if mouse_x < 1280 - 50:
		zmienne.camx += 5
		for MX1 in range(0, zmienne.hex_num):
			zmienne.hex_x["hex", MX1] += 5
	if mouse_x > 50:
		zmienne.camx -= 5
		for MX2 in range(0, zmienne.hex_num):
			zmienne.hex_x["hex", MX2] -= 5


def keyboard():
	press = pygame.key.get_pressed()
	global camy
	global camx
	if press[pygame.K_RIGHT]:
		camx -= 5
		for KR in range(0, zmienne.hex_num):
			zmienne.hex_x["hex", KR] -= 5
	if press[pygame.K_LEFT]:
		camx += 5
		for KL in range(0, zmienne.hex_num):
			zmienne.hex_x["hex", KL] += 5
	if press[pygame.K_DOWN]:
		camy -= 5
		for KD in range(0, zmienne.hex_num):
			zmienne.hex_y["hex", KD] -= 5

	if press[pygame.K_UP]:

		camy += 5
		for KU in range(0, zmienne.hex_num):
			zmienne.hex_y["hex", KU] += 5


def score():

	zmienne.up_bar.fill((0, 0, 0))
	# money
	money = pygame.font.Font(None, 25)

	money_score = money.render("Ilość Złota: " + str(zmienne.m_score), False, "white")
	money_score.blit(zmienne.screen, (1, 30))
	zmienne.up_bar.blit(money_score, (0, 6))
	# wojsko
	army = pygame.font.Font(None, 25)

	army_score = army.render("Ilość Wojska: " + str(zmienne.a_score), False, "white")
	army_score.blit(zmienne.screen, (100, 300))
	zmienne.up_bar.blit(army_score, (150, 6))

	# pola

	tiles_score = army.render("Ilość Posiadanych Pól: " + str(zmienne.p_score), False, "white")
	tiles_score.blit(zmienne.screen, (100, 300))
	zmienne.up_bar.blit(tiles_score, (330, 6))


def playe_hex():
	obw = 0

	zmienne.player_hex.fill((0, 0, 0, 0))

	for o in range(0, 6):
		zmienne.wymiar_p.append((zmienne.obramowanie_wymiary_x[o] + 535 + zmienne.camx + obw, zmienne.obramowanie_wymiary_y[o] + 294 + zmienne.camy))

	pygame.draw.polygon(zmienne.player_hex, (30, 224, 33, 110), zmienne.wymiar_p)
	pygame.draw.polygon(zmienne.player_hex, (255, 255, 255, 50), zmienne.wymiar_p, 4)

	for o in range(0, 6):
		zmienne.wymiar_p.pop()

	zmienne.screen.blit(zmienne.player_hex, (0, 0))


def decision():
	if zmienne.wyb:

		dec_rect = zmienne.imageDEC_surface.get_rect(center=(640, 360))
		gold_button_rect = zmienne.gold_surface.get_rect(midleft=(670, 360))
		army_button_rect = zmienne.army_surface.get_rect(midright=(610, 360))
		zmienne.screen.blit(zmienne.imageDEC_surface, dec_rect)
		zmienne.screen.blit(zmienne.gold_surface, gold_button_rect)
		zmienne.screen.blit(zmienne.army_surface, army_button_rect)
		colision = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()
		if gold_button_rect.collidepoint(colision) and mouse_pressed[0]:

			zmienne.m_score += 10
			zmienne.wyb = False
		if army_button_rect.collidepoint(colision) and mouse_pressed[0]:

			zmienne.a_score += 10
			zmienne.wyb = False


def turn():
	turn_rect = zmienne.turn_surface.get_rect(center=(100, 600))
	zmienne.screen.blit(zmienne.turn_surface, turn_rect)
	colision = pygame.mouse.get_pos()
	mouse_pressed = pygame.mouse.get_pressed()
	if turn_rect.collidepoint(colision) and mouse_pressed[0]:
		zmienne.wyb = True

font = pygame.font.SysFont(None, 30)
def draw_text(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)
def menu_pause():


	while zmienne.pause_menu_status:
		zmienne.screen.blit(zmienne.menu_s_surface, (100, 0))

		zmienne.screen.blit(zmienne.button_play_surface, zmienne.button_play)
		zmienne.screen.blit(zmienne.button_option_surface, zmienne.button_option)
		zmienne.screen.blit(zmienne.button_exit_surface, zmienne.button_exit)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					zmienne.click = True
		mx, my = pygame.mouse.get_pos()
		if zmienne.button_play.collidepoint((mx, my)):
			if zmienne.click:
				zmienne.click=False
				zmienne.pause_menu_status=False
				print('Play2')
				# game()
				game.gameloop()


		if zmienne.button_option.collidepoint((mx, my)):
			if zmienne.click:
				zmienne.click=False
				print('Options2')
				options.setting_menu()
				#options()
		if zmienne.button_exit.collidepoint((mx, my)):
			if zmienne.click:
				zmienne.click=False
				zmienne.pause_menu_status =False
				zmienne.game_status =False
				zmienne.start_menu_status = True
				print('Exit to start')



		pygame.display.update()
		zmienne.mainClock.tick(60)
		zmienne.click = False

def menu_start():
	while zmienne.start_menu_status:
		zmienne.screen.blit(zmienne.menu_s_surface, (0, 0))
		zmienne.screen.blit(zmienne.button_play_surface, zmienne.button_play)
		zmienne.screen.blit(zmienne.button_option_surface, zmienne.button_option)
		zmienne.screen.blit(zmienne.button_exit_surface, zmienne.button_exit)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					zmienne.click = True

		mx, my = pygame.mouse.get_pos()
		if zmienne.button_play.collidepoint((mx, my)):
			if zmienne.click:
				zmienne.click=False
				zmienne.start_menu_status=False
				zmienne.game_status =True
				print('Play')
				# game()
				game.gameloop()

		if zmienne.button_option.collidepoint((mx, my)):
			if zmienne.click:
				zmienne.click=False
				options.setting_menu()
				#options()
		if zmienne.button_exit.collidepoint((mx, my)):
			if zmienne.click:
				pygame.quit()
				sys.exit()

		pygame.display.update()
		zmienne.mainClock.tick(60)
		zmienne.click = False

