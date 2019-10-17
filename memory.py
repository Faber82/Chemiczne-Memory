import os.path
import pygame
import threading
import random
import math
import sys
#__file__ to nazwa ścieżki pliku z którego moduł został zaczytany jeżeli był zaczytany z pliku
#os.path.split(ścieżka) to funkcja która rozdziela ścieżkę na część przednią: ścieżkę i część tylną: nazwę pliku
#os.path.abspath() zwraca pełną ścieżkę nawet jeżeli podaliśmy np. .tekst.txt, lub katalog\..\drugi_katalog to pokaże całą ścieżkę

#poniższa linijka zwraca pełną ścieżkę pliku memory.py rozdzieloną na część przednią i tylną
os.path.split(os.path.abspath(__file__))

#pygame.image.get_extended() - sprawdza czy są dostępne rozszeżone formaty plików. Zwraca wartość True albo False. Jeżeli dobrze zrozumiałem
# bez tego można zaczytać tylko format PNG.

#poniższa pętla sprawdza dostępność plików 
if not pygame.image.get_extended():
#if not pygame.image.get_extended(): <-wersja z przodka
	raise SystemExit("Sorry, you require extended image module")
#Rect() - obiekt pygame do przechowywania koordynatów obiektów prostokątnych dwie pierwsze wartości to współrzędne na osi x,y;
#dwie następne to wymiary szerokość wysokość -> Rect(top,left,width,hight)

#parametry ekranu:
screen = pygame.Rect (0,0,1024,768)
#card_edges to odległość pola z kartami od brzegu obrazu, card_fill to odległość kart od siebie
card_edges=50
card_fill=4

#wymiary ekranu, oraz ustawienie wartści aktualnej karty na "Rzadna"	
width = 1024
height = 768
actual_card = None
#funkcja łądowania kart. argument funkcji poprzedzony gwiazdką oznacza, że można przyjąć elementy nie zdefiniowane jako lista
#dla każdej card z cards_base, dodajemy do pustej listy images element wygenerowany przez funkcję card_loading z atrybutem card 
#Funkcja zwraca listę kart.

def cards_loading(*cards_base):
	images=[]
	for position in cards_base:
		images.append(card_loading(position))
	return images

#funkcja card_loading kożysta z instrukcji try -> except. próbuje wczytać obraz z namebase i podstawić go za wartość img
#z wyjątkiem zgłoszenia błędu pygame.error co zpowoduje zamknięcie aplikacji
def card_loading(namebase, transparent=False):
	try:
		img=pygame.image.load(namebase)
	except pygame.error:
		raise SystemExit
	img=img.convert()
	#var.convert() tworzy nową kopię powierzchni ze zmienionym formatem pixeli. Przy braku podanego argumentu
	#Jeżeli żadne argumenty nie zostaną podane to format pixeli będzie taki sam jak powierzchnia wyświetlona.
	#przekonwertowanie powierzchni poleceniem convert() spowoduje że pixele utracą parametr alfa(czyli przeźroczystość)
	if transparent:
		#img.get_at((0,0)) kopjuje wartość koloru dla podanego pixela (w naszym przypadku pixela na pozycji 0,0) jeżeli transparent (chyba jeżeli transparent=True ale napewno niewiem)
		color=img.get_at((0,0))
		#po nadaniu zmiennej color wartości z pixela na pozycji 0,0 nadajemy ten kolor całemu img. Funkcja zwraca zmodyfikowany
		#w ten sposób img.
	#NIE WIEM TYLKO PO CO TO WSZYSTKO
		img.set_colorkey(color,RLEACCEL)
	return img

def pair_checking(card):
	#zmienna poza funkcją jest domyślnie globalna. Zmienna wewnątrz funkcji jest domyślnie lokalna. zmienna globalna
	#z poza funkcji może być zaczytana ale nie może być zmieniona wewnątrz funkcji. Żeby można było modyfikować globalną
	#funkcję wewnątrz funkcji należy dopisać wewnątrz funkcji "global" przed funkcją
	global actual_card
	#jeżeli nie ma aktualnej karty, karta (card) zostanie obrócona (funkcja rotate dalej w kodzie). aktualna karta (actual_card) będzie równać się karcie (card)
	if actual_card == None:
		card.rotate()
		actual_card=card
	#w przeciwnym razie karta (card) zostanie obrócona (funkcja rotate dalej w kodzie). Jeżeli id aktualnej_karty będzie takie samo jak id karty to znajdziemy parę
	#wyświetli się komunikat "Para!". Obie: aktualna karta i karta wyblakną do wartości alfa=80. wartość aktualnej karty zmieni się na "Żadna"
	else:
		card.rotate()
		if actual_card.id == card.id:
			print ("Para!")
			actual_card.image.set_alpha(80)
			card.image.set_alpha(80)
			actual_card = None
			#W przeciwnym razie pojawi się komuniat "To nie jest para". 
		else:
			print("To nie jest para")
			#jeżeli warunek z if nie zostanie spełniony to funkcja func zmieni stan carty i aktualnej karty na niewciśniętą
			#i obróci obie koszulkami do góry.
			def func():
				global actual_card
				card.pressed=False
				card.rotate()
				actual_card.rotate()
				actual_card.pressed=False
				actual_card=None
			#poniższa funkcja set_timeout CHYBA OKREŚLA OPÓŹNIENIE DLA WYKONANIA FUNKCJI func o 0,1s
 			 # to jest 0,1s czyli 100ms				
			set_timeout(func,0.5)


#poniższa funkcja to Timer. w def set_timeout wartość odliczana wynosi na początku Nic, chodzi tylko o utworzenie zmiennej
#żeby potem nie kszyczał że zmienna jest niezdefiniowana
def set_timeout(func,sec):
	t=None
	#wewnątrz Set_timeout utworzona jest funkcja func_wrapper (dekorator). działa to tak, że wzywamy funkcję 
	#set_timeout. Ta ma argumenty func i sec. Wewnątrz func_wrapper znajduje się timer. wywołana zostaje funkcja func
	def func_wrapper():
		func()
		#t.cancel() to syntax dla zatrzymania timera. wychodzi więc że po wykonaniu poleceń z func() zatrzymany zostaje timer
		t.cancel()
		#threading.Timer to wątek wykonujący funkcję po upływie określonego czasu. Argumenty to, czas i funkcja dekorator
	t=threading.Timer(sec,func_wrapper)
	#na koniec zostaje uruchomiony timer
	t.start()
	#podsumowując po wywołaniu set_timeout z argumentami func i sec nastąpi określenie t na podstawie podanej sec
	#(1.0 czyli 0,1s.) i odwołnia do funkcji dekoratora. Dekorator najpierw za pomocą funkcji func przywróci karty do pozycji 
	#wyjściowej a potem zakończy timer (TEGO AKURAT NIE ROZUMIEM). Na koniec posiadając już określony timer t funkcja set_timeout 
	#uruchoim timer przez t.start()

#klasa Card której argumentem jest Sprite z modułu pygame.sprite.
#Klasa opisuje obiekty tej gry czyli karty. Obiekt opisany jest w ten sposób, że __init__ opisuje właściwości karty, a pozostałe funkcje
#opisują co można z tymi kartami zrobić.
class Card(pygame.sprite.Sprite):
	#pygame.sprite.Sprite -> podstawowa klasa do obsługi widocznych obiektów graficznych
	global card_fill
	#klasa Sprite wymaga metody __init__(conajmniej self, + ewentualnie inne argumenty)
	def __init__(self,data):
		#wywołuję konstruktora klasy nadrzędnej (Sprite)
		pygame.sprite.Sprite.__init__(self)
		#teraz tworzę obrazy kart
		#lista obrazów (pusta)
		self.images=[]
		#self.images.append(card_loading("karta.jpg")) dodaje do listy obraz koszulki karty. 

		#Funkcja card_loading jako namebase przyjmuje wartość "karta.jpg". Następnie 
		#funkcja "próbuje" wczytać obraz (img=pygame.image.load(namebase)), jeżeli nie odnajdzie pliku zwróci error. 
		#następnie konwertuje obraz bez arguentów co spowoduje usunięcie wartości alfa dla piskeli. Potem wczyta kolor 
		#z piksela z pozycji 0,0 (color=img.get_at((0,0)). Na koniec obrazkowi zostaje nadany kolor (img.set_colorkey(color,RLEACCEL))
		#Po przeróbkach obraz zostaje zwrócony przez funkcję
		self.images.append(card_loading("karta.jpg"))
		#Funkcja card_loading jako namebase przyjmuje wartość data[0]. JAK ROZUMIEM PRZYJMUJE WARTOSC PIERWSZEJ (ZEROWEJ)
		#POZYCJI Z LISTY DATA (TYLKO ŻE NIGDZIE TAKIEJ NIE WIDZIAŁĘM JAK DOTĄD). Reszta operacji card_loading zostaje
		#przeprowadzona jak poprzednio.
		self.images.append(card_loading(data[0]))
		#rect służy do określenia pozycji i wymiarów. JEŻELI DOBRZE ROZUMIEM RECT ODBIERZE WYMIARY OD IMAGES[0] (BO IMAGES[0].GET_RECT())
		self.rect=self.images[0].get_rect()
		#przesuwa prostokąt (czyli naszą kartę) na osi x o wymiar card_fill czyli o 4 (CZEGO? NIE WIEM)
		self.rect.centerx=card_fill
		#przesuwa prostokąt (czyli naszą kartę) na osi Y o 100 (PIXELI? TEŻ NIE WIEM)
		self.rect.centery=100
		#image=element z pierwszej pozycji (dokładnie to zerowej) na liście images
		self.image=self.images[0]
		#obrócenie=fałsz czyli domyślnie nie obrócona
		self.rotation=False
		#id=pozycja dróga z listy data(czyli pierwsza). WSZYSTKO WSKAZUJE NA TO ŻE IMAGES I DATA TO TUPLE Z LISTY KARDS. 
		#KAŻDA POZYCJA LISTY KARDS SKŁADA SIĘ Z DWÓCH TUPLI KARTY.JPG I ID W POSTACI NAZWY. PIERWSZE TUPLE TWORZĄ LISTĘ CARDS
		#DRUGIE TUPLE TO LISTA DATA
		self.id=data[1]
		#pressed ustalone na fałsz więc karta domyślnie niewciśnięta
		self.pressed=False
		#funkcja obracania karty. Jeżeli obrazek nie obrócony to image zamienia się na images (CZYLI CHYBA Z KOSZULKI NA SPÓD)
		#a parametr rotate zmienia się na prawda
	def rotate(self):
		if not self.rotation:
			self.image=self.images[1]
			self.rotation=True
		#w przeciwnym razie image = images[0] czyli koszulka a parametr roate zmienia się na Fałsz.
		else:
			self.image=self.images[0]
			self.rotation=False
	#fnkcja do klikania myszką
	def mouseEvent(self,type):
		#jeśli typ=klik i pressed=fałsz
		if type=="click":
			if not self.pressed:
				#wykonuje się funkjca pair_chacking (czyli porównywanie id karty i aktalnej karty) a następnie status karty 
				#pressed zmienia się na prawda
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
		#wywaliłem z przodka obwódkę
	def draw(self,ekran,pic):
		but_draw=pygame.transform.scale(pic,(self.width,self.height))
		ekran.blit(but_draw,(self.x,self.y))
		#pygame.draw.rect(ekran, self.pic, (self.x, self.y,self.width,self.height),0)
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
	#pygame.display.set_mode sprawi że faktycznie wyświetli się okno gry. Argumenty to szerokość i wysokość okna. Warość jest 
	#umieszczona w zmiennej screen
	screen = pygame.display.set_mode ((width, height))
	ekran=screen
	#ta funkcja nadaje nazwę oknu (będzie się wyświetlać na górnej listwie i po zminimalizowaniu)
	pygame.display.set_caption("Chemiczne Memory")
	#card_loading to dokłądniej funkcja do załadowania jpgów. w poniższym przypadku załadowane zostanie tło 
	background=card_loading('tło.jpg')
	#ta funkcja dopasuje wymiary tła do zadanych wymiarów. W moim przypadku do width i height podanych wcześniej. Wypełni więc
	#całe okno
	background=pygame.transform.scale (background, (width, height))
	displaylist=[]
	global card_fill
	global card_edges
	#poniżej znajduje się lista tupli. każdy element składa się z dwóch tupli czyli nazwy pliku i id. Kart są sparowane
	#przez id (dwie kraty mają samo id)
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
	#lista cards jest mieszana w losowej kolejności. Układ kart za każdym razem będzie inny
	random.shuffle(cards)
	#dla każdej karty w cards zmienna card (pochodzi z cards_loading (for cards in cards_base)) przyjmuje właściwości 
	#klassy Card dla argumentu cards[inde x c]
	for c in range(0,len(cards)):
		card=Card(cards[c])
		#pozycja kart na osi x to obwiednia karty +szerokość karty i wypełnienia karty * modulo z wartoci c 
		#(od 0 do ostatniej karty). Dzięki temu ustali się miejsce dla 10 kart w rzędzie
		card.rect.centerx=card_edges + ((c%10)*(card.rect.width+card_fill))
		#pozycja na osi y to brzeg kraty + wysokość karty i wypełnienie karty * floor z wartości c/10. floor z wartości to 
		#floor zwraca największą liczbę całkowitą nie większą niż zadana liczba. Rezultat działania jest taki że dla każdego C
		#zostanie zwrócone 10 pól (np floor dla 0/10 da 10 zer) (NIE BARDZO OBEJMUJE GLOWĄ JAK TO MA SIĘ WYŚWIETLAĆ)
		card.rect.centery=card_edges + (math.floor(c/10)*(card.rect.height+card_fill))
		#karty dodawane są na koniec listy displaylist ustalonej wcześnie jako pusta
		displaylist.append(card)
	exit=False
	quit_button=Button((0,255,0),850,700,150,50,'Koniec')
	while not exit:
		
		#CHYBA uruchamia kolejno akcje i usuwa je z listy rzeczy do wykonania
		
		for action in pygame.event.get():
			quit_button.draw(ekran,pygame.image.load("przycisk.jpg"))
			pos=pygame.mouse.get_pos()
			#jeśli typ akcji QUIT gra się zamknie.
			if action.type==pygame.QUIT:
				sys.exit(0)
			#jeśli zostanie wciśnięty przycisk myszy nr 1 (CZYLI CHYBA LEWY)
			if action.type==pygame.MOUSEBUTTONUP:
				if (action.button==1): #po co nawias?
					#CHYBA OZNACZA ŻE NA DANEJ WSPÓŁRZĘDNEJ GDZIE NASTĄPIŁO WCIŚNIĘCIE PRZYCISKU MYSZY ZOSTANIE WYKONANA AKCJA
					x,y=action.pos
					# dla elementu i z zakresu od 0 do tylu ile jest elementów w liście displaylist
					for i in range (0,len(displaylist)):
						#gamer = element i z listy displaylist 
						gamer=displaylist[i]
						#jeśli gamer o w spółrzędnych x,y jest w obszarze rect
						if gamer.rect.collidepoint(x,y):
							#CHYBA NASTĘPUJE EFEKT WCIŚNIĘCIACZYLI OBRÓT KARTY
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
			
		#funkcja blit kopjuje pixele z jednego obrazu na drugi. Jeżeli robię blit obrazu na inny obraz to nie tyle ukłądam jeden 
		#obraz na drugim co zmieniam kolory pixeli na tym spodnim (u mnie background) na kolory tego nakładanego.
		#W efekcie tworzę nowy background z namalowanym obrazem (KARTY CHYBA)
		
		screen.blit(background,(0,0))
		for i in range (0,len(displaylist)):
			#dla każdego elementu (i) w zakresie od 0 do tylu ile jest elementów w liście displaylist, blituję obrazki.
			#rezultat - maluję karty na tle
			screen.blit(displaylist[i].image, displaylist[i].rect)
		#kompletny obraz z kartami zostaje zaktualizowany
			pygame.display.update(displaylist[i].rect)
		#NIE WIEM O CO CHODZI ZE ZWRÓCENIEM 0
	return 0
	#Jeżeli uruchamiam swój plik (memory.py) jako główny program interpreter nada wartość __main__ do __name__. Gdyby 
	#inny plik był main wtedy name otrzymałoby nazwę mojego pliku. W moim przypadku warunek powinien być spełniony
	#NIE WIEM PO CO TO 


if __name__=='__main__':
	#jeżeli warunek jest spełniony zostaje uruchomina gra
	pygame.init()
	main()
