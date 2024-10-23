import pygame
import random
import math

# Initiera pygame
pygame.init()

# Skärmens storlek
screen = pygame.display.set_mode((800, 600))

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
playerY = 480
playerX_change = 0

# Fiende
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Skott
bulletX = 0
bulletY = 480
bulletY_change = 10
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

# Skottfunktion
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    pygame.draw.circle(screen, BLUE, (x + 20, y), 5)

# Kollision
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Visa poäng
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, WHITE)
    screen.blit(score, (x, y))

# Spel-loop
running = True
while running:
    # Fyll bakgrunden svart
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Om en knapp trycks ned, kontrollera om det är vänster eller höger
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # Om en knapp släpps
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Spelarrörelse
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 760:
        playerX = 760

    # Fienderörelse
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 760:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # Kollision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Skottrörelse
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()

pygame.quit()
