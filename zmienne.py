# zmienne
import pygame



res = (1280, 720)
screen = pygame.display.set_mode(res)



tekstury_path = 'tekstury/'
click=False

wymiary = (100, 200)
szerokosc_hex = 0
wysokosc_hex = 0
przesuniecie_x = 0
przesuniecie_y = 0
obramowanie_wymiary_x = [58, 0, 0, 58, 119, 119]
obramowanie_wymiary_y = [0, 30, 97, 127, 97, 30]
wymiar_obramowania = []
m_score = 0
a_score = 0
p_score = 1
wyb = True
menu_p_bool = False
menu_s_bool = True
game_status = False



# interfejs
up_bar = pygame.Surface((1280, 30))
up_bar.fill("black")

# wczytanie tekstury
grass_surface = pygame.image.load(tekstury_path+"hex_trawa.png",)
village_surface = pygame.image.load(tekstury_path+"wioska.png")
forest_surface = pygame.image.load(tekstury_path+"las.png")
water_surface = pygame.image.load(tekstury_path+"woda.png")
castle_surface = pygame.image.load(tekstury_path+"castle.png")
imageDEC_surface = pygame.image.load(tekstury_path+"ekran.png")
button1_surface = pygame.image.load(tekstury_path+"button1.png")
button2_surface = pygame.image.load(tekstury_path+"button2.png")
button3_surface = pygame.image.load(tekstury_path+"button3.png")
# tło meny pauzy
menu_s_surface = pygame.image.load('GUI/carlos_menu.png')   # per-pixel alpha
menu_s_surface = pygame.transform.scale(menu_s_surface, (res[0], res[1]))
#przycisku menu

#b = pygame.Rect(left, top, width, height)
button_play = pygame.Rect(res[0]/2-200/2,200,200,97)
button_option = pygame.Rect(res[0]/2-200/2, 310, 200, 78)
button_exit = pygame.Rect(res[0]/2-200/2, 420, 200, 78)
#button_option = pygame.Rect(centerW-ButtonW/2, ButtonPosition*(2+1), ButtonW, 50)
button_exit = pygame.Rect(res[0]/2-200/2, 530, 200, 100)

button_play_surface = pygame.image.load('GUI/play_button.png')
button_option_surface = pygame.image.load('GUI/option_button.png')
button_exit_surface = pygame.image.load('GUI/exit_button.png')


player_hex = pygame.Surface((1000, 1000), pygame.SRCALPHA)

wymiar_p = []
camx = 0
camy = 0

hex_surf = {}
hex_x = {}
hex_y = {}
hex_typ = {}
hex_num_x = 20
hex_num_y = 20
hex_num = (hex_num_x * hex_num_y)
licz = 0
