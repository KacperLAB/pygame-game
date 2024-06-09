
import pygame,random,time

pygame.init()

TIME_LIMIT = 2
WIDTH = 800
HEIGHT = 400
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 100

WHITE = (255,255,255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Click, click!')
ICON = pygame.image.load("window_icon.png")
pygame.display.set_icon(ICON)

button_sound = pygame.mixer.Sound("sound.mp3")
button_sound.set_volume(0.2)

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

class Button:
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width= width
        self.height = height
        self.last_shown = time.time()

    def press_check(self, mouse_position):
        mouse_position_x, mouse_position_y = mouse_position
        return self.x <= mouse_position_x <= self.x + self.width and self.y <= mouse_position_y <= self.y + self.height

    def draw_button(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def change_position(self):
        self.x = random.randrange(WIDTH-BUTTON_WIDTH)
        self.y = random.randrange(HEIGHT-BUTTON_HEIGHT)
    
    def change_color(self):
        self.color = (random.randrange(255),random.randrange(255),random.randrange(255))

    def change_size(self):
        self.width = self.width - 10
        self.height = self.height - 10

def check_clicks(buttons, mouse_position):
    clicked_buttons = []  # List to store clicked buttons
    for button in buttons:
        if button.press_check(mouse_position):
            clicked_buttons.append(button)  # Add clicked button to list
    return clicked_buttons  # Return list of clicked buttons

def paused():
    paused_text = font.render("PAUSED",True,BLACK)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
        screen.blit(paused_text,(600,0))
        pygame.display.update()

#button1 = Button(BLACK,350,150,BUTTON_WIDTH,BUTTON_HEIGHT)
font = pygame.font.SysFont('Arial',60)

buttons = [Button(BLACK,350,150,BUTTON_WIDTH,BUTTON_HEIGHT)]

score = 0
combo = 0
hits = 0
misses = 0
highest_score = 0



while True:
    if(misses == 0):
        acc = 100
    else:
        acc = (hits/(hits+misses))*100
        acc = format(acc,'.2f')
    
    score_text = font.render("score: " + str(score),True,BLACK)
    combo_text = font.render("x"+str(combo),True,BLACK)
    hits_text = font.render("hits: "+ str(hits),True,BLACK)
    misses_text = font.render("misses: "+ str(misses),True,BLACK)
    acc_text = font.render("acc: "+ str(acc) +"%",True,BLACK)
    if(score >= highest_score):
        highest_score = score
    highest_score_text = font.render("highest score: " + str(highest_score),True,BLACK)

    current_time = time.time()
    for button in buttons:
        if current_time - button.last_shown > TIME_LIMIT:
        # Button timed out, change position
            score -= 1
            misses += 1
            button.change_position()
            button.change_color()
            button.last_shown = current_time  # Update last shown time


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused()

        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_w):
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = event.pos
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                mouse_position = pygame.mouse.get_pos()
    
            clicked_buttons = check_clicks(buttons, mouse_position)
            for button in clicked_buttons:
                pygame.mixer.Sound.play(button_sound)
                button.change_color()
                button.change_position()
                score += 1*combo
                combo += 1
                hits += 1
                button.last_shown = current_time
                if score % 10 == 0:
                    button.change_size()
                    buttons.append(Button(BLACK, 350, 150, button.width, button.height))
            if not clicked_buttons:
                score -= 1
                combo = 0
                misses += 1

    screen.fill(WHITE)
    
    for button in buttons:
        button.draw_button(screen)
    
    screen.blit(score_text,(0,0))
    screen.blit(combo_text,(0,60))
    screen.blit(hits_text,(0,120))
    screen.blit(misses_text,(0,180))
    screen.blit(acc_text,(0,240))
    screen.blit(highest_score_text,(0,300))

    pygame.display.update()