import pygame
import random
import sys
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

# Inicjalizacja PyGame
pygame.init()

# Ustawienia ekranu
szerokosc = 800
wysokosc = 400
ekran = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption('Click, click!')
icon = pygame.image.load("window_icon.png")
pygame.display.set_icon(icon)

slider = Slider(ekran, 100,200,400,20,min=0,max=1,step=0.1)
output = TextBox(ekran, 250, 250, 70, 50, fontSize=30)

button_sound = pygame.mixer.Sound("sound.mp3")
button_sound.set_volume(0.2)

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Szerokość i wysokość przycisku
szerokosc_przycisku = 50
wysokosc_przycisku = 50
margines = 0

# Czcionka
czcionka = pygame.font.SysFont("Arial", 30)

kolory = {"bialy": (255,255,255), "czarny":(0,0,0)}

# Kolory
bialy = (255, 255, 255)
czarny = (0, 0, 0)
ilosc_przyciskow = 10

def losuj_kolor():
    return (random.randrange(255),random.randrange(255),random.randrange(255))

def play_sound():
    pygame.mixer.Sound.play(button_sound)


class Przycisk:
    def __init__(self, kolor, x, y, szerokosc, wysokosc):
        self.kolor = kolor
        self.x = x
        self.y = y
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc

    def sprawdz_klikniecie(self, pozycja_myszy):
        x_myszy, y_myszy = pozycja_myszy
        return self.x <= x_myszy <= self.x + self.szerokosc and \
               self.y <= y_myszy <= self.y + self.wysokosc

    def rysuj(self, ekran):
        pygame.draw.rect(ekran, self.kolor, (self.x, self.y, self.szerokosc, self.wysokosc))

# Rozmieszczenie przycisków
ilosc_kolumn = max(1, int((szerokosc - 2 * margines) / (szerokosc_przycisku + margines)))
margines = 0

# Rozmieszczenie przycisków za pomocą funkcji pygame.draw.grid
przyciski = []
for i in range(ilosc_przyciskow):
    pozycja_x = i % ilosc_kolumn * (szerokosc_przycisku + margines)
    pozycja_y = i // ilosc_kolumn * (wysokosc_przycisku + margines)
    przyciski.append(Przycisk(losuj_kolor(), pozycja_x, pozycja_y, szerokosc_przycisku, wysokosc_przycisku))

# Główna pętla gry
while True:
    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Obsługa kliknięć na przyciskach
        if event.type == pygame.MOUSEBUTTONDOWN:
            pozycja_myszy = event.pos
            for i, przycisk in enumerate(przyciski):
                if przycisk.sprawdz_klikniecie(pozycja_myszy):
                    przycisk.kolor = losuj_kolor()
                    play_sound()
                    pygame.time.wait(1)
 
    # Rysowanie
    ekran.fill(bialy)

    

    # Rysowanie przycisków
    for przycisk in przyciski:
        przycisk.rysuj(ekran)

    output.setText(f"{int(slider.getValue()*100)}%")
    button_sound.set_volume(slider.getValue())
    # Aktualizacja ekranu
    pygame_widgets.update(event)
    pygame.display.update()
