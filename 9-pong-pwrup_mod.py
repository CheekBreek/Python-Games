import pygame
import sys
import random

# Pygame Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Game Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colors
light_grey = (200, 200, 200)
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height /
                     2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Game Variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# Sound Effects
pong_sound = pygame.mixer.Sound("./media/pong.ogg")
score_sound = pygame.mixer.Sound("./media/score.ogg")

# Power Up variables
pwrupImg = pygame.image.load("./media/pwrup.png")
p1_pwrupReady = True
p2_pwrupReady = True
p1_used_pwrup = 0
p2_used_pwrup = 0


def pwrup_ready():
    if p1_pwrupReady:
        screen.blit(pwrupImg, (screen_width-60, 10))

    if p2_pwrupReady:
        screen.blit(pwrupImg, (10, 10))


def pwrup_check():
    curr_time = pygame.time.get_ticks()
    if curr_time - p1_used_pwrup >= 4000:
        player.height = 140
    if curr_time - p2_used_pwrup >= 4000:
        opponent.height = 140

    global p1_pwrupReady, p2_pwrupReady
    if curr_time - p1_used_pwrup >= 8000:
        p1_pwrupReady = True
    if curr_time - p2_used_pwrup >= 8000:
        p2_pwrupReady = True


def p1_pwrup():
    if p1_pwrupReady:
        player.height += 160


def p2_pwrup():
    if p2_pwrupReady:
        opponent.height += 160


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball Collision (Top or Bottom)
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    # Player Scores
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        ball_restart()

    # Opponent Scores
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        ball_restart()

    # Ball Collision (Player or Opponent)
    if ball.colliderect(player) or ball.colliderect(opponent):
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_x *= -1


def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_ai():
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y

    # move ball to the center
    ball.center = (screen_width/2, screen_height/2)

    # start the ball in a random direction
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


if __name__ == "__main__":

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_speed -= 6
                if event.key == pygame.K_DOWN:
                    player_speed += 6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_speed += 6
                if event.key == pygame.K_DOWN:
                    player_speed -= 6
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP0:
                    p1_pwrup()
                    p1_pwrupReady = False
                    p1_used_pwrup = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    p2_pwrup()
                    p2_pwrupReady = False
                    p2_used_pwrup = pygame.time.get_ticks()

        ball_animation()
        player_animation()
        opponent_ai()
        pwrup_check()

        # Visuals
        screen.fill(bg_color)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2,
                                                0), (screen_width / 2, screen_height))
        pwrup_ready()
        # Creating the surface for text
        player_text = basic_font.render(f'{player_score}', False, light_grey)
        screen.blit(player_text, (660, 470))
        opponent_text = basic_font.render(
            f'{opponent_score}', False, light_grey)
        screen.blit(opponent_text, (600, 470))

        # Loop Timer
        pygame.display.flip()
        clock.tick(60)
