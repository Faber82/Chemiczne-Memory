import os.path
import pygame
import threading
import random
import math
import sys

os.path.split(os.path.abspath(__file__))
if not pygame.image.get_extended():
	raise SystemExit("Sorry, you require extended image module")
screen = pygame.Rect (0,0,1024,768)
card_edges=50
card_fill=4
width = 1024
height = 768
actual_card = None

def cards_loading(*cards_base):
	images=[]
	for position in cards_base:
		images.append(card_loading(position))
	return images

def card_loading(namebase, transparent=False):
	try:
		img=pygame.image.load(namebase)
	except pygame.error:
		raise SystemExit
	img=img.convert()
	if transparent:
		color=img.get_at((0,0))
		img.set_colorkey(color,RLEACCEL)
	return img

def pair_checking(card):
	global actual_card	
	if actual_card == None:
		card.rotate()
		actual_card=card
	else:
		card.rotate()
		if actual_card.id == card.id:
			print ("Para!")
			actual_card.image.set_alpha(80)
			card.image.set_alpha(80)
			actual_card = None
		else:
			print("To nie jest para")
			def func():
				global actual_card
				card.pressed=False
				card.rotate()
				actual_card.rotate()
				actual_card.pressed=False
				actual_card=None			
			set_timeout(func,0.5)

def set_timeout(func,sec):
	t=None
	def func_wrapper():
		func()
		t.cancel()
	t=threading.Timer(sec,func_wrapper)
	t.start()

class Card(pygame.sprite.Sprite):
	global card_fill
	def __init__(self,data):
		pygame.sprite.Sprite.__init__(self)
		self.images=[]
		self.images.append(card_loading("karta.jpg"))
		self.images.append(card_loading(data[0]))
		self.rect=self.images[0].get_rect()
		self.rect.centerx=card_fill
		self.rect.centery=100
		self.image=self.images[0]
		self.rotation=False
		self.id=data[1]
		self.pressed=False
		
	def rotate(self):
		if not self.rotation:
			self.image=self.images[1]
			self.rotation=True
		else:
			self.image=self.images[0]
			self.rotation=False
	def mouseEvent(self,type):
		if type=="click":
			if not self.pressed:
				pair_checking(self)
				self.pressed=True

class Button():
	def __init__(self, pic, x, y, width, height, text=''):
		self.pic=pic
		self.x=x
		self.y=y
		self.width=width
		self.height=height
		self.text=text
	def draw(self,ekran,pic):
		but_draw=pygame.transform.scale(pic,(self.width,self.height))
		ekran.blit(but_draw,(self.x,self.y))
		if self.text!='':
			font=pygame.font.SysFont('comicsans',40)
			text=font.render(self.text,1,(0,0,0))
			ekran.blit(text, (self.x+(self.width/2 - text.get_width()/2), self.y+(self.height/2 - text.get_height()/2)))
	def isOver(self,pos):
		if pos[0]>self.x and pos[0]<self.x+self.width:
			if pos[1]>self.y and pos[1]<self.y+self.height:
				return True
		return False	

def main():
	screen = pygame.display.set_mode ((width, height))
	ekran=screen
	pygame.display.set_caption("Chemiczne Memory")
	background=card_loading('tło.jpg')
	background=pygame.transform.scale (background, (width, height))
	displaylist=[]
	global card_fill
	global card_edges
	cards =[
	("karta1.jpg","H"  ),("karta2.jpg","H"  ),
	("karta3.jpg","Be" ),("karta4.jpg","Be" ),
	("karta5.jpg","Cu" ),("karta6.jpg","Cu" ),
	("karta7.jpg","Zn" ),("karta8.jpg","Zn" ),
	("karta9.jpg","Al" ),("karta10.jpg","Al"),
	("karta11.jpg","N" ),("karta12.jpg","N" ),
	("karta13.jpg","O" ),("karta14.jpg","O" ),
	("karta15.jpg","Li"),("karta16.jpg","Li"),
	("karta17.jpg","Mg"),("karta18.jpg","Mg"),
	("karta19.jpg","Ag"),("karta20.jpg","Ag"),
	("karta21.jpg","Hg"),("karta22.jpg","Hg"),
	("karta23.jpg","C" ),("karta24.jpg","C" ),
	("karta25.jpg","P" ),("karta26.jpg","P" ),
	("karta27.jpg","S" ),("karta28.jpg","S" ),
	("karta29.jpg","Na"),("karta30.jpg","Na"),
	("karta31.jpg","Ca"),("karta32.jpg","Ca"),
	("karta33.jpg","Au"),("karta34.jpg","Au"),
	("karta35.jpg","B" ),("karta36.jpg","B" ),  
	("karta37.jpg","Si"),("karta38.jpg","Si"), 
	("karta39.jpg","F" ),("karta40.jpg","F" ),
	("karta41.jpg","Cl"),("karta42.jpg","Cl"),
	("karta43.jpg","Fe"),("karta44.jpg","Fe"),
	("karta45.jpg","Br"),("karta46.jpg","Br"),
	("karta47.jpg","J" ),("karta48.jpg","J" ),
	("karta49.jpg","He"),("karta50.jpg","He"),
	("karta51.jpg","Ne"),("karta52.jpg","Ne"),
	("karta53.jpg","Ar"),("karta54.jpg","Ar"),
	("karta55.jpg","Kr"),("karta56.jpg","Kr"),
	("karta57.jpg","Xe"),("karta58.jpg","Xe"),
	("karta59.jpg","Rn"),("karta60.jpg","Rn"),
	]
	random.shuffle(cards)
	for c in range(0,len(cards)):
		card=Card(cards[c])
		card.rect.centerx=card_edges + ((c%10)*(card.rect.width+card_fill))
		card.rect.centery=card_edges + (math.floor(c/10)*(card.rect.height+card_fill))
		displaylist.append(card)
	exit=False
	quit_button=Button((0,255,0),850,700,150,50,'Koniec')
	while not exit:
		for action in pygame.event.get():
			quit_button.draw(ekran,pygame.image.load("przycisk.jpg"))
			pos=pygame.mouse.get_pos()
			if action.type==pygame.QUIT:
				sys.exit(0)
			if action.type==pygame.MOUSEBUTTONUP:
				if (action.button==1): #po co nawias?
					x,y=action.pos
					for i in range (0,len(displaylist)):
						gamer=displaylist[i]
						if gamer.rect.collidepoint(x,y):
							gamer.mouseEvent("click")
				
			if action.type==pygame.MOUSEMOTION:
				if quit_button.isOver(pos):
					quit_button.draw(ekran,pygame.image.load("przycisk3.jpg"))			
			if action.type==pygame.MOUSEBUTTONDOWN:
				if quit_button.isOver(pos):
					quit_button.draw(ekran,pygame.image.load("przycisk2.jpg"))
			if action.type==pygame.MOUSEBUTTONUP:
				if quit_button.isOver(pos):
					exit=True
					break
					quit_button.draw(ekran,pygame.image.load("przycisk3.jpg"))
				else:
					quit_button.draw(ekran,pygame.image.load("przycisk.jpg"))
			pygame.display.flip()
		screen.blit(background,(0,0))
		for i in range (0,len(displaylist)):
			screen.blit(displaylist[i].image, displaylist[i].rect)
			pygame.display.update(displaylist[i].rect)
	return 0
if __name__=='__main__':
	pygame.init()
	main()
