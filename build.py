import pygame
class BuildMenu(pygame.sprite.Group):
	"""docstring for BuildMenu"""
	
	def __init__(self,screen):
		super().__init__()
		self.on_off = False
		self.item_offset = pygame.Vector2(100,0)
		
		self.display_surface = screen
		self.display_size = pygame.Vector2(self.display_surface.get_size()[0],self.display_surface.get_size()[1])
		
		self.ui_size  = pygame.Vector2(300,0)
		
		self.internal_surf_size = (self.display_size.x-self.ui_size.x,self.display_size.y-30)
		self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
		self.internal_surf.set_alpha(255)
		self.offset = pygame.math.Vector2()		

	def open_menu(self):
		self.on_off = True
		self.display_surface.set_alpha(255)
	def close_menu(self):
		self.on_off = False
	def draw_menu(self):
		self.internal_surf.blit(self.display_surface,(0,30))
		s = pygame.Surface(self.internal_surf_size,pygame.SRCALPHA)
		s.fill((255,25,158))
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect_item.centery): #
			offset_pos = sprite.rect_item.topleft
			s.blit(sprite.item_surface,offset_pos)
		self.display_surface.blit(s,(0,30))        
		
	def item_offset_add(self):
		self.item_offset.y +=110
		# self.update()
		pass
	def item_offset_sub(self):
		self.item_offset.y -=110
class MenuItem(pygame.sprite.Sprite):
	"""docstring for MenuItem"""

	def __init__(self,group,description,image,cost,army_buff,money_buff):
		
		super().__init__(group)
		self.cost = cost
		self.have = False
		self.army_buff = army_buff
		self.money_buff = money_buff
		

		self.FONTSIZE = 25
		self.fontDesc = pygame.font.Font(None,self.FONTSIZE)
		self.description = self.description_wrap(description)
		self.description_text = self.fontDesc.render(description,True,'#000000')
		item_size = pygame.Vector2()
		item_size.x = group.internal_surf_size[0]
		item_size.y = 100
		self.des_size = (item_size.x*0.75,item_size.y)
		self.item_offset = pygame.Vector2()
		self.item_offset.x = group.internal_surf_size[0]-item_size.x
		self.item_offset.y += group.item_offset.y
		#surface 
		self.item_surface = pygame.Surface((group.internal_surf_size[0],100),pygame.SRCALPHA)
		self.description_surface = pygame.Surface(self.des_size, pygame.SRCALPHA)
		self.image = pygame.image.load('GUI/Building/'+image+'.png')
		self.image = pygame.transform.scale(self.image,(100,100))
		button_size = (group.internal_surf_size[0]-100-self.des_size[0],100)
		self.button = pygame.Surface(button_size, pygame.SRCALPHA)
		#rect
		self.rect_item = self.item_surface.get_rect(topleft = (0,self.item_offset.y))
		self.rect_image = self.image.get_rect(topleft = (0,self.item_offset.y))
		self.rect_button = self.button.get_rect(topleft = (100,self.item_offset.y))
		self.rect_description = self.description_surface.get_rect(topleft = (100+145,self.item_offset.y))

		group.item_offset_add()
		self.description_surface.fill('#ff0000')
		self.description_surface.blit(self.description_text,(10,5))
		self.item_surface.fill('#ff000025')
		self.button.fill('#0000ff')
		self.fontBuy = pygame.font.Font(None,45)
		button_text = self.fontBuy.render(str(cost)+' $',True,'#000000')
		self.button.blit(button_text,(10,5))


		self.item_surface.blit(self.description_surface,(100+145,0))
		self.item_surface.blit(self.image,(0,0))
		self.item_surface.blit(self.button,(100,0))
	def update(self):
		self.item_surface.fill('#00ff0025')
		self.description_surface.fill('#00ff00')
		self.button.fill('#0000ff')
		self.description_surface.blit(self.description_text,(10,5))
		button_text = self.fontBuy.render("Kupione",True,'#000000')
		self.button.blit(button_text,(10,5))


		self.item_surface.blit(self.description_surface,(100+145,0))
		self.item_surface.blit(self.image,(0,0))
		self.item_surface.blit(self.button,(100,0))
		
	def buy(self):
		# if zmienne.m_score >=self.cost and zmienne.a_score >-1:
		# 	zmienne.m_score-=self.cost
		# 	zmienne.m_buff += self.money_buff
		# 	zmienne.a_buff += self.army_buff
		self.have = True
		self.update()

		

		pass
	def description_wrap(self,description):
		line = description
		n = 92
		lines = [line[i:i+n] for i in range(0, len(line), n)]
		new_line=''
		for x in lines:
			new_line +=x 
			new_line +='\t'
			print (new_line)
		return new_line