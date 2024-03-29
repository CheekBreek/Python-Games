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
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
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

# Ball
ballImg = pygame.image.load("./media/ball.png")
ballX = screen_width / 2 - 15
ballY = screen_height / 2 - 15

# Right Paddle
lPaddleImg = pygame.image.load("./media/lPaddle.png")
lPaddleX = 10
lPaddleY = screen_height / 2 - 70

# Right Paddle
rPaddleImg = pygame.image.load("./media/rPaddle.png")
rPaddleX = screen_width - 20
rPaddleY = screen_height / 2 - 70

def lPaddle(x, y):
  screen.blit(lPaddleImg, (x, y)) #draw the left player on the screen

def rPaddle(x, y):
  screen.blit(rPaddleImg, (x, y)) #draw the right player on the screen

def dBall(x, y):
  screen.blit(ballImg, (x, y)) #draw the ball on the screen

def ball_animation():
  global ball_speed_x, ball_speed_y, player_score, opponent_score, ballX, ballY

  ball.x += ball_speed_x
  ball.y += ball_speed_y
  ballX += ball_speed_x
  ballY += ball_speed_y

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
  global rPaddleY

  player.y += player_speed
  rPaddleY += player_speed

  if player.top <= 0:
    player.top = 0
    rPaddleY = 0
  if player.bottom >= screen_height:
    player.bottom = screen_height
    rPaddleY = screen_height - 140
  
def opponent_ai():
  global lPaddleY

  if opponent.top < ball.y:
    opponent.y += opponent_speed
    lPaddleY += opponent_speed

  if opponent.bottom > ball.y:
    opponent.y -= opponent_speed
    lPaddleY -= opponent_speed

  if opponent.top <= 0:
    opponent.top = 0
    lPaddleY = 0

  if opponent.bottom >= screen_height:
    opponent.bottom = screen_height
    lPaddleY = screen_height - 140
    
def ball_restart():
  global ball_speed_x, ball_speed_y, ballX, ballY

  # move ball to the center
  ball.center = (screen_width/2, screen_height/2)
  ballX = screen_width/2 - 15
  ballY = screen_height/2 - 15

  # start the ball in a random direction
  ball_speed_y *= random.choice((1,-1)) 
  ball_speed_x *= random.choice((1,-1))  

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

    ball_animation()
    player_animation()
    opponent_ai()

    # Visuals 
    screen.fill(bg_color)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))

    rPaddle(rPaddleX, rPaddleY)
    lPaddle(lPaddleX, lPaddleY)
    dBall(ballX, ballY)

    # Creating the surface for text
    player_text = basic_font.render(f'{player_score}',False,light_grey)
    screen.blit(player_text,(660,470)) 

    opponent_text = basic_font.render(f'{opponent_score}',False,light_grey)
    screen.blit(opponent_text,(600,470)) 

    # Loop Timer
    pygame.display.flip()
    clock.tick(60)
