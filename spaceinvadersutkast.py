import pygame
import random
import math

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initiera pygame
pygame.init()

# Skärmens storlek
screen = pygame.display.set_mode((700, 600))

# Titel och ikon
pygame.display.set_caption("Space Invaders")

# Färger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Spelarskepp
playerX = 370
playerY = 550
playerX_change = 0


# Fiende
enemyX = []
enemyY = []
enemyY_change = 0.02  # Fienderna rör sig nedåt i en konstant hastighet
num_of_enemies = 3
wave = 1


# Boss-relaterade variabler
boss_active = False
boss_health = 15  # Bossen kräver 10 skott
bossX = 0
bossY = 50
bossY_change = 0.015  # Hastighet för bossen, långsammare än vanliga

# Startmängd liv
player_lives = 30

# Livets teckensnitt
lives_font = pygame.font.Font('freesansbold.ttf', 32)

# Visa liv
def show_lives(x, y):
    lives = lives_font.render("Health: " + str(player_lives), True, WHITE)
    screen.blit(lives, (x, y))

# Vinststatus
game_won = False



for i in range(num_of_enemies):
    enemyX.append(random.randint(0, 660))  # Startposition för varje fiende
    enemyY.append(random.randint(50, 150))  # Startposition för varje fiende

def start_new_wave():
    global num_of_enemies, enemyY_change, wave, boss_active
    wave += 1
    enemyY_change += 0.02  # Öka hastigheten för vanliga fiender
    num_of_enemies += 1

    # Lägg till nya fiender
    enemyX.append(random.randint(0, 660))
    enemyY.append(random.randint(50, 150))

    # Spawna boss vid våg 5
    if wave == 5 and not boss_active:
        num_of_enemies = 2
        eneyY_change = 0.02
        spawn_boss()


# Skott
bulletX = 0
bulletY = 480
bulletY_change = 0.5
bullet_state = "ready"  # "ready" betyder att du kan skjuta, "fire" betyder att skottet är på väg

# Poäng
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Spelares funktion
def player(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, 40, 20))

# Fienders funktion
def enemy(x, y, i):
    pygame.draw.rect(screen, RED, (x, y, 40, 20))

def spawn_boss():
    global bossX, bossY, boss_active
    bossX = random.randint(0, 660)  # Startposition inom skärmens bredd
    bossY = 50  # Start nära toppen
    boss_active = True


def boss(x, y):
    pygame.draw.rect(screen, (255, 0, 255), (x, y, 80, 40))  # Bossens rektangel

def show_lose_screen():
    screen.fill(BLACK)
    font = pygame.font.Font('freesansbold.ttf', 64)
    win_text = font.render("You lose!", True, WHITE)
    screen.blit(win_text, (200, 200))

    # Rita knappen för att börja om
    button_font = pygame.font.Font('freesansbold.ttf', 32)
    button_text = button_font.render("Restart", True, BLACK)
    button_rect = pygame.Rect(275, 400, 150, 50)  # Knappens position och storlek
    pygame.draw.rect(screen, WHITE, button_rect)
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

    pygame.display.update()

    return button_rect  # Returnera knappens rektangel för kollisionskontroll


def show_win_screen():
    screen.fill(BLACK)
    font = pygame.font.Font('freesansbold.ttf', 64)
    win_text = font.render("You Win!", True, WHITE)
    screen.blit(win_text, (200, 200))

    # Rita knappen för att börja om
    button_font = pygame.font.Font('freesansbold.ttf', 32)
    button_text = button_font.render("Restart", True, BLACK)
    button_rect = pygame.Rect(275, 400, 150, 50)  # Knappens position och storlek
    pygame.draw.rect(screen, WHITE, button_rect)
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

    pygame.display.update()

    return button_rect  # Returnera knappens rektangel för kollisionskontroll

def reset_game():
    
    global score_value, wave, num_of_enemies, enemyX, enemyY, boss_active, boss_health, game_won

    score_value = 0
    wave = 1
    num_of_enemies = 3
    enemyX = [random.randint(0, 660) for _ in range(num_of_enemies)]
    enemyY = [random.randint(50, 150) for _ in range(num_of_enemies)]
    boss_active = False
    boss_health = 10
    game_won = False
    

def is_boss_collision(bossX, bossY, bulletX, bulletY):
    distance = math.sqrt((math.pow(bossX - bulletX, 2)) + (math.pow(bossY - bulletY, 2)))
    return distance < 40

# Skottfunktion
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    pygame.draw.circle(screen, BLUE, (x + 20, y), 10)

# Kollision
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

# Visa poäng
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, WHITE)
    screen.blit(score, (x, y))


 # Spel-loop
running = True
while running:
    screen.fill(BLACK)


    if game_won:
        button_rect = show_win_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    reset_game()
        continue

    if boss_active:
        boss(bossX, bossY)
        bossY += bossY_change
        if is_boss_collision(bossX, bossY, bulletX, bulletY):
            bulletY = 480
            bullet_state = "ready"
            boss_health -= 1
            if boss_health <= 0:
                boss_active = False
                game_won = True
        if bossY > 600:
            bossY = 50
            bossX = random.randint(0, 660)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 660:
        playerX = 660

    for i in range(num_of_enemies):
        enemyY[i] += enemyY_change
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 660)
            enemyY[i] = random.randint(50, 150)
        if enemyY[i] > 600:
            enemyY[i] = random.randint(50, 150)
            player_lives -= 1  # Minska liv när en fiende passerar
            if player_lives <= 0:
                running = False
 
        enemy(enemyX[i], enemyY[i], i)
        if score_value >= wave * 10:
            start_new_wave()

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_lives(530, 10)  # Visa antalet liv längst upp till höger

    pygame.display.update()

pygame.quit()
