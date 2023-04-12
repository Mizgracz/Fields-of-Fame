import pygame,os,sys


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720





class LoadMenu(object):
    """docstring for LoadMenu"""
    scroll = 0
    def __init__(self, screen,GAME):
        super(LoadMenu, self).__init__()
        self.game = GAME

        self.MOUSE_Y = 0
        self.allItem = []
        self.screen = screen
        self.status = False
        self.WINDOW_SIZE = self.screen.get_size()
        self.background_texture = pygame.Surface(self.WINDOW_SIZE)
        

        self.SCROLL_SURFACE = pygame.Surface((30,self.screen.get_size()[1]*0.25))
        self.SCROLL_SURFACE.fill((0,0,0))
        self.SCROLL_RECT = pygame.Rect(0,0,0,0)
        self.SCROLL_RECT.topleft = (self.screen.get_size()[0]-30,0)



        
        self.SCROLL_RECT.size = (30,self.screen.get_size()[1]*0.25)




        self.RECT = pygame.Rect(self.WINDOW_SIZE[0]-30,0,30,self.screen.get_size()[1]*0.25)
        self.RECT.centery = self.screen.get_size()[1]*0.25/2

        self.background_texture.fill('#ff00ff')
        ###CZYTAJ ILOŚĆ PLIKÓW PLIKI / 3
        self.folder_path = 'save/'
        self.ILOSC_PLIKOW = len([f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))])
        x = self.ILOSC_PLIKOW/4.5
        if x<1:
            x=1
            pass
        #### ZAOKRĄGLIĆ W GURE
        self.window = pygame.Surface((self.WINDOW_SIZE[0],self.WINDOW_SIZE[1]*x),pygame.SRCALPHA)

        self.on_bar = False
        self.mouse_diff = 0
        self.y_axis = 0
        self.change_y = 0

        bar_height = int((self.WINDOW_SIZE[1] - 40) / (self.window.get_size()[1] / (self.WINDOW_SIZE[1] * 1.0)))
        self.bar_rect = pygame.Rect(self.WINDOW_SIZE[0] - 40,20,40,bar_height)
        self.bar_up = pygame.Rect(self.WINDOW_SIZE[0] - 20,0,20,20)
        self.bar_down = pygame.Rect(self.WINDOW_SIZE[0] - 20,self.WINDOW_SIZE[1] - 20,20,20)

        self.scroll_length = self.WINDOW_SIZE[1] - self.bar_rect.height - 40


        self.update()
    def update(self):
        self.allItem = []
        self.ILOSC_PLIKOW = len([f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))])
        x = self.ILOSC_PLIKOW/4.75
        if x<1:
            x=1
            pass
        #### ZAOKRĄGLIĆ W GURE
        self.window = pygame.Surface((self.WINDOW_SIZE[0],self.WINDOW_SIZE[1]*x),pygame.SRCALPHA)
        from os import listdir
        from os.path import isfile, join
        mypath = 'save/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for i in range(self.ILOSC_PLIKOW):
            self.allItem += [LoadItem(f'{onlyfiles[i]}',self.window,i)]
        pass
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            elif self.bar_up.collidepoint(pos):
                self.change_y = 10
            elif self.bar_down.collidepoint(pos):
                self.change_y = -10
        else :
            self.change_y = 0
            self.on_bar = False
            
                
    
        PRESS = pygame.mouse.get_pressed()[0]
        POS = pygame.mouse.get_pos()
        self.MOUSE_Y = pygame.mouse.get_pos()[1]
        for item in self.allItem:
            if item.rect_item.collidepoint(POS) and PRESS:
                self.load_game(item.tmpID)
                self.status = False
                pygame.time.Clock().tick(3)
        # if self.RECT.collidepoint(pygame.mouse.get_pos()) :



        
    def load_game(self,index):
        import gameplay
        print('LoadGame')
        import csv,zipfile

        with zipfile.ZipFile(f"save/{self.allItem[index].name}", "r") as zip:
            zip.extractall()
        with open(f'save/map.csv','r') as savefile:
            csvfile = csv.reader(savefile,delimiter=';')
            i = -1
            for row in csvfile:
                if i !=-1:
                    self.game.map.allhex["hex", i].polozenie_hex_x = int(row[0])
                    self.game.map.allhex["hex", i].polozenie_hex_y = int(row[1])
                    self.game.map.allhex["hex", i].number = int(row[2])
                    self.game.map.allhex["hex", i].texture_index = int(row[3])
                    self.game.map.allhex["hex", i].verticles = (row[4]) 
                    self.game.map.allhex['hex',i].update_texture()
                i+=1
            
            pass
        with open(f'save/stats.txt','r') as savefile:
            # csvfile = csv.reader(savefile,delimiter=':')
            stats,col2 = [],[]
            for line in savefile:
                stats += [line.strip().split(":")]
                
            gameplay.build_stauts = bool(stats[0][1])
            gameplay.build =bool(stats[1][1])
            gameplay.gold_count = int(stats[2][1])
            gameplay.army_count = int(stats[3][1])
            gameplay.terrain_count = int(stats[4][1])
            gameplay.wyb = bool(stats[5][1])
            gameplay.player_hex_status = bool(stats[6][1])
            gameplay.army_count_bonus = int(stats[7][1])
            gameplay.gold_count_bonus = int(stats[8][1])
            gameplay.turn_count = int(stats[9][1])

        pygame.time.Clock().tick(1)
        os.remove(f"save/stats.txt")
        os.remove(f"save/map.csv")
        self.update()
        pass
    def draw(self):
        
        self.handle_events()
        self.screen.blit(self.background_texture, (0, 0))

        self.y_axis += self.change_y
        
        if self.y_axis > 0:
            self.y_axis = 0
        elif (self.y_axis + self.window.get_size()[1]) < self.WINDOW_SIZE[1]:
            self.y_axis = self.WINDOW_SIZE[1] - self.window.get_size()[1]

        height_diff = self.window.get_size()[1] - self.WINDOW_SIZE[1]
        if height_diff == 0 :
            height_diff = 1
        bar_half_lenght = self.bar_rect.height / 2 + 20
        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < 20:
                self.bar_rect.top = 20
            elif self.bar_rect.bottom > (self.WINDOW_SIZE[1] - 20):
                self.bar_rect.bottom = self.WINDOW_SIZE[1] - 20
            
            self.y_axis = int(height_diff / (self.scroll_length * 1.0) * (self.bar_rect.centery - bar_half_lenght) * -1)
            self.scroll = self.y_axis
        else:
            self.bar_rect.centery =  self.scroll_length / (height_diff * 1.0) * (self.y_axis * -1) + bar_half_lenght
        for i in self.allItem:
            i.update()
            i.drawItem()



        # pygame.draw.rect(self.screen,('#000000'),self.SCROLL_RECT)
        pygame.draw.rect(self.screen,(255,255,0),self.bar_rect)
        
        # self.screen.blit(self.bar_up_image,(self.WINDOW_SIZE[0] - 20,0))
        # self.screen.blit(self.bar_down_image,(self.WINDOW_SIZE[0] - 20,self.WINDOW_SIZE[1] - 20))        
        self.screen.blit(self.window,(0,self.scroll))
        # self.screen.blit(self.SCROLL_SURFACE,(self.screen.get_size()[0]-30,self.MOUSE_Y))
        pygame.display.flip()
class LoadItem(object):
    _ID_ = 0
    """docstring for Item"""
    def __init__(self, name,screen,tmpID):
        FONT_SIZE = 20
        FONT_NAME = 'timesnewroman'
        font_text = pygame.font.SysFont(FONT_NAME,FONT_SIZE)
        super(LoadItem, self).__init__()
        self.screen = screen
        self.name = name
        self.tmpID = tmpID
        self.WIDTH = self.screen.get_size()[0]//2
        self.HEIGHT = 100
        self.item_surface = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.item_surface.fill('#00ff00')
        self.del_surface = pygame.Surface((100,100))
        self.del_surface.fill('#ff0000')
        self.rect_item = pygame.Rect(self.WIDTH/2,150*self.tmpID+50+LoadMenu.scroll,self.WIDTH,100)
        self.rect_del = pygame.Rect(self.WIDTH/2,150*self.tmpID+50+LoadMenu.scroll,100,100)
        self.rect_del.right = self.rect_item.right
        self.rect_item = pygame.Rect(self.WIDTH/2,150*self.tmpID+50+LoadMenu.scroll,self.WIDTH-100,100)
        
        self.font_opis = font_text.render((f'{self.tmpID+1}. {self.name}'), True,(255, 255, 255))
        
    def drawItem(self):
        self.screen.blit(self.item_surface,self.rect_item)
        self.screen.blit(self.del_surface,self.rect_del)
        self.item_surface.blit(self.font_opis,(10,5))
        # pygame.draw.rect(self.screen,(255,255,255),self.rect_item)
        # pygame.draw.rect(self.screen,(25,0,255),self.rect_del)
    def update(self):
        self.rect_item.top = 150*self.tmpID+50+LoadMenu.scroll
        self.rect_del.top = 150*self.tmpID+50+LoadMenu.scroll
#######################

class SaveMenu(object):
    """docstring for LoadMenu"""
    scroll = 0
    def __init__(self, screen,GAME):
        super(LoadMenu, self).__init__()
        self.game = GAME

        self.MOUSE_Y = 0
        self.allItem = []
        self.screen = screen
        self.status = False
        self.WINDOW_SIZE = self.screen.get_size()
        self.background_texture = pygame.Surface(self.WINDOW_SIZE)
        

        self.SCROLL_SURFACE = pygame.Surface((30,self.screen.get_size()[1]*0.25))
        self.SCROLL_SURFACE.fill((0,0,0))
        self.SCROLL_RECT = pygame.Rect(0,0,0,0)
        self.SCROLL_RECT.topleft = (self.screen.get_size()[0]-30,0)



        
        self.SCROLL_RECT.size = (30,self.screen.get_size()[1]*0.25)




        self.RECT = pygame.Rect(self.WINDOW_SIZE[0]-30,0,30,self.screen.get_size()[1]*0.25)
        self.RECT.centery = self.screen.get_size()[1]*0.25/2

        self.background_texture.fill('#ff00ff')
        ###CZYTAJ ILOŚĆ PLIKÓW 
        self.folder_path = 'save/'
        self.ILOSC_PLIKOW = len([f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))])
        x = self.ILOSC_PLIKOW/4.5
        if x<1:
            x=1
            pass
        #### ZAOKRĄGLIĆ W GURE
        self.window = pygame.Surface((self.WINDOW_SIZE[0],self.WINDOW_SIZE[1]*x),pygame.SRCALPHA)

        self.on_bar = False
        self.mouse_diff = 0
        self.y_axis = 0
        self.change_y = 0

        bar_height = int((self.WINDOW_SIZE[1] - 40) / (self.window.get_size()[1] / (self.WINDOW_SIZE[1] * 1.0)))
        self.bar_rect = pygame.Rect(self.WINDOW_SIZE[0] - 40,20,40,bar_height)
        self.bar_up = pygame.Rect(self.WINDOW_SIZE[0] - 20,0,20,20)
        self.bar_down = pygame.Rect(self.WINDOW_SIZE[0] - 20,self.WINDOW_SIZE[1] - 20,20,20)

        self.scroll_length = self.WINDOW_SIZE[1] - self.bar_rect.height - 40


        self.update()
    def update(self):
        self.allItem = []
        self.ILOSC_PLIKOW = len([f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))])
        x = self.ILOSC_PLIKOW/4.75
        if x<1:
            x=1
            pass
        #### ZAOKRĄGLIĆ W GURE
        self.window = pygame.Surface((self.WINDOW_SIZE[0],self.WINDOW_SIZE[1]*x),pygame.SRCALPHA)
        from os import listdir
        from os.path import isfile, join
        mypath = 'save/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for i in range(self.ILOSC_PLIKOW):
            self.allItem += [LoadItem(f'{onlyfiles[i]}',self.window,i)]
        pass
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            elif self.bar_up.collidepoint(pos):
                self.change_y = 10
            elif self.bar_down.collidepoint(pos):
                self.change_y = -10
        else :
            self.change_y = 0
            self.on_bar = False
        
        PRESS = pygame.mouse.get_pressed()[0]
        POS = pygame.mouse.get_pos()
        self.MOUSE_Y = pygame.mouse.get_pos()[1]
        for item in self.allItem:
            if item.rect_item.collidepoint(POS) and PRESS:
                self.load_game(item.tmpID)
                self.status = False
                pygame.time.Clock().tick(3)        
        
    def load_game(self,index):
        import gameplay
        print('LoadGame')
        import csv,zipfile

        with zipfile.ZipFile(f"save/{self.allItem[index].name}", "r") as zip:
            zip.extractall()
        with open(f'save/map.csv','r') as savefile:
            csvfile = csv.reader(savefile,delimiter=';')
            i = -1
            for row in csvfile:
                if i !=-1:
                    self.game.map.allhex["hex", i].polozenie_hex_x = int(row[0])
                    self.game.map.allhex["hex", i].polozenie_hex_y = int(row[1])
                    self.game.map.allhex["hex", i].number = int(row[2])
                    self.game.map.allhex["hex", i].texture_index = int(row[3])
                    self.game.map.allhex["hex", i].verticles = (row[4]) 
                    self.game.map.allhex['hex',i].update_texture()
                i+=1
            
            pass
        with open(f'save/stats.txt','r') as savefile:
            # csvfile = csv.reader(savefile,delimiter=':')
            stats,col2 = [],[]
            for line in savefile:
                stats += [line.strip().split(":")]
                
            gameplay.build_stauts = bool(stats[0][1])
            gameplay.build =bool(stats[1][1])
            gameplay.gold_count = int(stats[2][1])
            gameplay.army_count = int(stats[3][1])
            gameplay.terrain_count = int(stats[4][1])
            gameplay.wyb = bool(stats[5][1])
            gameplay.player_hex_status = bool(stats[6][1])
            gameplay.army_count_bonus = int(stats[7][1])
            gameplay.gold_count_bonus = int(stats[8][1])
            gameplay.turn_count = int(stats[9][1])

        pygame.time.Clock().tick(1)
        os.remove(f"save/stats.txt")
        os.remove(f"save/map.csv")
        self.update()
        pass
    def draw(self):
        
        self.screen.blit(self.background_texture, (0, 0))
        # self.screen.blit(self.load_button_texture, (SCREEN_WIDTH / 2 - 150, 360))
        # if self.resume:
        #     button_texture = self.resume_game_button_texture
        # else:
        #     button_texture = self.new_game_button_texture
        # self.screen.blit(button_texture, self.new_game_button)

        # quit_texture = self.quit_button_texture
        # self.screen.blit(quit_texture, self.quit_button)
        self.handle_events()

        self.y_axis += self.change_y
        
        if self.y_axis > 0:
            self.y_axis = 0
        elif (self.y_axis + self.window.get_size()[1]) < self.WINDOW_SIZE[1]:
            self.y_axis = self.WINDOW_SIZE[1] - self.window.get_size()[1]

        height_diff = self.window.get_size()[1] - self.WINDOW_SIZE[1]
        if height_diff == 0 :
            height_diff = 1
        bar_half_lenght = self.bar_rect.height / 2 + 20
        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < 20:
                self.bar_rect.top = 20
            elif self.bar_rect.bottom > (self.WINDOW_SIZE[1] - 20):
                self.bar_rect.bottom = self.WINDOW_SIZE[1] - 20
            
            self.y_axis = int(height_diff / (self.scroll_length * 1.0) * (self.bar_rect.centery - bar_half_lenght) * -1)
            self.scroll = self.y_axis
        else:
            self.bar_rect.centery =  self.scroll_length / (height_diff * 1.0) * (self.y_axis * -1) + bar_half_lenght
        for i in self.allItem:
            i.update()
            i.drawItem()



        # pygame.draw.rect(self.screen,('#000000'),self.SCROLL_RECT)
        pygame.draw.rect(self.screen,(255,255,0),self.bar_rect)
        
        # self.screen.blit(self.bar_up_image,(self.WINDOW_SIZE[0] - 20,0))
        # self.screen.blit(self.bar_down_image,(self.WINDOW_SIZE[0] - 20,self.WINDOW_SIZE[1] - 20))        
        self.screen.blit(self.window,(0,self.scroll))
        # self.screen.blit(self.SCROLL_SURFACE,(self.screen.get_size()[0]-30,self.MOUSE_Y))
        pygame.display.flip()
class SaveItem(object):
    _ID_ = 0
    """docstring for Item"""
    def __init__(self, name,screen,tmpID):
        FONT_SIZE = 20
        FONT_NAME = 'timesnewroman'
        font_text = pygame.font.SysFont(FONT_NAME,FONT_SIZE)
        super(LoadItem, self).__init__()
        self.screen = screen
        self.name = name
        self.tmpID = tmpID
        self.WIDTH = self.screen.get_size()[0]//2
        self.HEIGHT = 100
        self.item_surface = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.item_surface.fill('#00ff00')
        self.del_surface = pygame.Surface((100,100))
        self.del_surface.fill('#ff0000')
        self.rect_item = pygame.Rect(self.WIDTH/2,150*self.tmpID+50+LoadMenu.scroll,self.WIDTH,100)
        self.rect_del = pygame.Rect(self.WIDTH/2,150*self.tmpID+50+LoadMenu.scroll,100,100)
        self.rect_del.right = self.rect_item.right
        self.rect_item = pygame.Rect(self.WIDTH/2,150*self.tmpID+50+LoadMenu.scroll,self.WIDTH-100,100)
        
        self.font_opis = font_text.render((f'{self.tmpID+1}. {self.name}'), True,(255, 255, 255))
        
    def drawItem(self):
        self.screen.blit(self.item_surface,self.rect_item)
        self.screen.blit(self.del_surface,self.rect_del)
        self.item_surface.blit(self.font_opis,(10,5))
        # pygame.draw.rect(self.screen,(255,255,255),self.rect_item)
        # pygame.draw.rect(self.screen,(25,0,255),self.rect_del)
    def update(self):
        self.rect_item.top = 150*self.tmpID+50+LoadMenu.scroll
        self.rect_del.top = 150*self.tmpID+50+LoadMenu.scroll

###################

class Menu:
    resume = False
    def __init__(self, screen, clock, max_tps):
        self.screen = screen
        self.clock = clock
        self.max_tps = max_tps
        self.status = True
        
        

        self.font = pygame.font.Font(None, 48)
        self.new_game_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 120, 200, 100)
        self.load_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 0, 200, 100)
        self.save_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 120, 200, 100)
        self.quit_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 240, 200, 100)
        self.background_texture = pygame.image.load("texture/main_menu/background.png").convert()
        self.new_game_button_texture = pygame.image.load("texture/main_menu/graj_button.png").convert_alpha()
        self.resume_game_button_texture = pygame.image.load("texture/main_menu/wznow_button.png").convert_alpha()
        self.quit_button_texture = pygame.image.load("texture/main_menu/zamknij_button.png").convert_alpha()
        self.load_button_texture = pygame.image.load("texture/main_menu/wczytaj_button.png").convert_alpha()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.new_game_button.collidepoint(pos):
                    self.status = False
                    self.resume = True
                    return 'new_game'
                elif self.quit_button.collidepoint(pos):
                    self.status = False
                    return 'quit'
                elif self.load_button.collidepoint(pos):
                    self.status = False
                    self.resume = True
                    return 'load_game'
                elif self.save_button.collidepoint(pos):
                    self.status = False
                    self.resume = True
                    return 'save_game'

    def draw(self):
        self.screen.blit(self.background_texture, (0, 0))
        self.screen.blit(self.load_button_texture, (SCREEN_WIDTH / 2 - 150, 360))
        if self.resume:
            button_texture = self.resume_game_button_texture
            self.screen.blit(self.load_button_texture,self.save_button)
        else:
            button_texture = self.new_game_button_texture
        self.screen.blit(button_texture, self.new_game_button)

        quit_texture = self.quit_button_texture
        self.screen.blit(quit_texture, self.quit_button)

        pygame.display.flip()

    def run(self):
        choice = self.handle_events()
        if choice:
            return choice
        self.draw()
        self.clock.tick(self.max_tps)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
max_tps = 60.0

menu1 = Menu(screen, clock, max_tps)
menu1.run()
