# zmienne
import pygame



res = (1280, 720)
screen_center = [res[0]/2,res[1]/2]
screen = pygame.display.set_mode(res)
mainClock = pygame.time.Clock()

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

a_buff = 0
m_buff = 0

click=False
wyb = True
pause_menu_status = False
start_menu_status = True
build_menu_status = False
game_status = False

music_status = True

# interfejs
up_bar = pygame.Surface((1280, 30))
up_bar.fill("black")

# wczytanie tekstury hex
grass_surface = pygame.image.load("tekstury/hex_trawa.png",)
village_surface = pygame.image.load("tekstury/wioska.png")
forest_surface = pygame.image.load("tekstury/las.png")
water_surface = pygame.image.load("tekstury/woda.png")
castle_surface = pygame.image.load("tekstury/castle.png")
# tekstury GUI tury
imageDEC_surface = pygame.image.load("tekstury/ekran.png")
gold_surface = pygame.image.load("GUI/gold_button.png")
army_surface = pygame.image.load("GUI/army_button.png")
turn_surface = pygame.image.load("GUI/turn_button.png")
# tło meny pauzy
#przycisku menu

#b = pygame.Rect(left, top, width, height)
button_play = pygame.Rect(res[0]/2-200/2,200,200,97)
button_option = pygame.Rect(res[0]/2-200/2, 310, 200, 78)
button_exit = pygame.Rect(res[0]/2-200/2, 530, 200, 100)
# GUI menu
menu_s_surface = pygame.image.load('GUI/carlos_menu.png')
menu_s_surface = pygame.transform.scale(menu_s_surface, (res[0], res[1]))

button_play_surface = pygame.image.load('GUI/play_button.png')
button_option_surface = pygame.image.load('GUI/option_button.png')
button_exit_surface = pygame.image.load('GUI/exit_button.png')

#budynki tekstura tmp
build1 = pygame.image.load('GUI/Building/tmp.png')
build2 = pygame.image.load('GUI/Building/tmp2.png')
build3 = pygame.image.load('GUI/Building/tmp3.png')



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


# opcje
setting_surface = pygame.image.load('GUI/Setting/setting_screen.png')
setting_surface = pygame.transform.scale(setting_surface, (setting_surface.get_size()[0],res[1]-100))
CheckBox_True_surface=pygame.image.load('GUI/Setting/CheckBoxTrue.png')
CheckBox_False_surface=pygame.image.load('GUI/Setting/CheckBoxFalse.png')