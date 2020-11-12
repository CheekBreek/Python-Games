import pygame
import math
import random
import sys

pygame.init()

# Game Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Title Variable
title = True
exitgame = False

# Colours
white = (255, 255, 255)
light_grey = (200, 200, 200)
light_blue = (68, 85, 90)
gold = (255, 215, 0)
bg_color = pygame.Color('grey12')
t_color = pygame.Color('grey12')

# Background
background = pygame.image.load("./media/stars.png")
titlescreen = pygame.image.load("./media/spacetitle.jpg")
victoryscreen = pygame.image.load("./media/spacewin.jpg")
# Sound
pygame.mixer.music.load("./media/background.wav")
pygame.mixer.music.play(-1)

# Player
playerImg = pygame.image.load("./media/spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Cursor
cursorImg = pygame.image.load("./media/spaceship.png")
cursorX = 142
cursorY = 500


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load("./media/ufo.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("./media/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Fonts
score_value = 0
font = pygame.font.Font("./fonts/Square.ttf", 24)
font_large = pygame.font.Font("./fonts/Square.ttf", 40)
textX = 10
textY = 10
victory_font = pygame.font.Font("./fonts/Square.ttf", 90)
game_over_font = pygame.font.Font("./fonts/Square.ttf", 128)


def show_score(x, y):
    score = font.render("Score: "+str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def cursor(x, y):
    screen.blit(cursorImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state

    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):

    distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))

    if distance < 27:
        return True
    else:
        return False


def game_over():  # display the game over text
    over_font = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_font, (100, 250))


def victory():  # display the victory screen
    pygame.mixer.music.load("./media/FFWIN.mp3")
    pygame.mixer.music.play(-1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        screen.blit(victoryscreen, (0, 0))

        titleFont = victory_font.render("VICTORY", False, white)
        screen.blit(titleFont, (240, 200))  # blit puts one surface on another

        saved = font.render(
            "Earth has been saved! You have defeated the alien threat!", False, white)
        screen.blit(saved, (50, 450))  # blit puts one surface on another

        pygame.display.update()


# Game Loop
running = True
while running:

    while True and title == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                exitgame = True
                cursorX = 561

            if event.key == pygame.K_LEFT:
                exitgame = False
                cursorX = 142

            if event.key == pygame.K_RETURN:
                if exitgame == True:
                    pygame.quit()
                    sys.exit()

                title = False

        screen.fill((0, 0, 0))
        screen.blit(titlescreen, (0, 0))

        titleFont = font_large.render("Space Invaders", False, white)
        screen.blit(titleFont, (250, 200))  # blit puts one surface on another

        play = font.render("Play", False, white)
        screen.blit(play, (150, 450))  # blit puts one surface on another

        exit = font.render("Exit", False, white)
        screen.blit(exit, (570, 450))  # blit puts one surface on another

    # pygame.display.flip()
    # clock.tick(60)
        cursor(cursorX, cursorY)
        pygame.display.update()

    # Game Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3

            if event.key == pygame.K_RIGHT:
                playerX_change = 3

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = pygame.mixer.Sound("./media/laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Screen Attributes
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_enemies):

        # Game Over
        if enemyY[i] > 440:  # trigger the end of the game
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over()

            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = pygame.mixer.Sound("./media/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Animation
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
