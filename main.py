import pygame
import random
import math
from pygame import mixer

# Initialise the pygame methods
pygame.init()

# Create the window
window = pygame.display.set_mode((800, 600))

# Background sound
mixer.music.load('background-music.wav')
mixer.music.play(-1)

# Title and logo
pygame.display.set_caption('Stressed Unicorns')
icon = pygame.image.load('suave-unicorn.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('suave-unicorn.png')
playerX = 370
playerY = 480
playerX_Change = 0

# Stressed Unicorns
stressedUnicornsImg = []
stressedUnicornX = []
stressedUnicornY = []
stressedUnicornX_change = []
stressedUnicornY_change = []
num_of_stressed_unicorns = 6

for i in range(num_of_stressed_unicorns):
    stressedUnicornsImg.append(pygame.image.load('stressed-unicorn.png'))
    stressedUnicornX.append(random.randint(0, 735))
    stressedUnicornY.append(random.randint(50, 150))
    stressedUnicornX_change.append(4)
    stressedUnicornY_change.append(40)

# Wine

# Ready - you can't see the wine glass on the screen
# Throw - the wine glass is currently moving
wineGlassImg = pygame.image.load('wine.png')
wineGlassX = 0
wineGlassY = 480
wineGlassX_change = 4
wineGlassY_change = 10
wineGlass_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('sweet_creamy.ttf', 32)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('sweet_creamy.ttf', 64)


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    window.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    window.blit(over_text, (200, 250))


def player(x, y):
    window.blit(playerImg, (x, y))


def enemy(x, y, index):
    window.blit(stressedUnicornsImg[index], (x, y))


def fire_bullet(x, y):
    global wineGlass_state
    wineGlass_state = 'fire'
    window.blit(wineGlassImg, (x + 16, y + 10))


def is_collision(unicorn_x, unicorn_y, wine_x, wine_y):
    distance = math.sqrt((math.pow(unicorn_x - wine_x, 2)) + (math.pow(unicorn_y - wine_y, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # Background
    window.fill((254, 184, 198))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -8
            if event.key == pygame.K_RIGHT:
                playerX_Change = 8
            if event.key == pygame.K_SPACE:
                if wineGlass_state == 'ready':
                    bullet_sound = mixer.Sound('throw.wav')
                    bullet_sound.play()
                    wineGlassX = playerX
                    fire_bullet(playerX, wineGlassY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    # Make sure sprites don't go out of bounds
    playerX += playerX_Change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_stressed_unicorns):

        # Game Over
        if stressedUnicornY[i] > 440:
            for j in range(num_of_stressed_unicorns):
                stressedUnicornY[j] = 2000
            game_over_text()
            break

        stressedUnicornX[i] += stressedUnicornX_change[i]

        if stressedUnicornX[i] <= 0:
            stressedUnicornX_change[i] = 4
            stressedUnicornY[i] += stressedUnicornY_change[i]
        elif stressedUnicornX[i] >= 736:
            stressedUnicornX_change[i] = -4
            stressedUnicornY[i] += stressedUnicornY_change[i]

        # Collision
        collision = is_collision(stressedUnicornX[i], stressedUnicornY[i], wineGlassX, wineGlassY)
        if collision:
            explosion_sound = mixer.Sound('swallow.wav')
            explosion_sound.play()
            wineGlassY = 480
            wineGlass_state = 'ready'
            score_value += 1
            stressedUnicornX[i] = random.randint(0, 735)
            stressedUnicornY[i] = random.randint(50, 150)

        enemy(stressedUnicornX[i], stressedUnicornY[i], i)

    # Bullet movement
    if wineGlassY <= 0:
        wineGlassY = 480
        wineGlass_state = 'ready'

    if wineGlass_state == 'fire':
        fire_bullet(wineGlassX, wineGlassY)
        wineGlassY -= wineGlassY_change

    player(playerX, playerY)
    show_score(textX, textY)

    # Update the window
    pygame.display.update()
