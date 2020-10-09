import pygame, sys, random

def ball_animation():

    global ball_speed_x, ball_speed_y, player_score, opponent_score, ballX, ballY
    
    #Game Logic
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    #Visual Mod Logic
    ballX += ball_speed_x
    ballY += ball_speed_y

    #Ball Collision (Top of Bottom)
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1 #reverse direction
   
    # Player Scores
    if ball.left <= 0: 
        pygame.mixer.Sound.play(score_sound) #play the score sound
        player_score += 1 #increment player score var
        ball_restart() #start ball in the middle
    
    # Opponent Scores
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound) #play the score sound
        opponent_score += 1 #increment opponent score
        ball_restart()  #start ball in the middle
         
    #Ball Collision (Player)    
    if ball.colliderect(player) or ball.colliderect(opponent):
        pygame.mixer.Sound.play(pong_sound) #play the pong sound
        ball_speed_x *= -1 #reverse direction

def player_animation():
    global rPaddleY

    player.y += player_speed
    rPaddleY += player_speed

    if player.top <= 0:
        player.top = 0 #puts player at the top of screen
        rPaddleY = 0 # Visual mod
    if player.bottom >= screen_height:
        player.bottom = screen_height #puts player at bottom
        rPaddleY = player.top #Visual mod

def opponent_animation():
    global lPaddleY

    opponent.y += opponent_speed
    lPaddleY += opponent_speed

    if opponent.top <= 0:
        opponent.top = 0 #puts player at the top of screen
        lPaddleY = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height #puts player at bottom
        lPaddleY = opponent.top

def opponent_ai():
    global lPaddleY, p2_pwrupReady, p2_used_pwrup

    if opponent.top < ball.y:
        opponent.y += opponent_ai_speed
        lPaddleY += opponent_ai_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_ai_speed
        lPaddleY -= opponent_ai_speed
    
    if opponent.top <= 0:
        opponent.top = 0
        lPaddleY = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height
        lPaddleY = opponent.top

    if p2_pwrupReady:
        p2_pwrup()
        p2_pwrupReady = False
        p2_used_pwrup = pygame.time.get_ticks()

def ball_restart():
    global ball_speed_x, ball_speed_y, ballX, ballY

    #move ball to center
    ball.center = (screen_width/2, screen_height/2)
    ballX = screen_width/2 - 15
    ballY = screen_height/2 - 15

    #start the ball in a random direction
    ball_speed_y *= random.choice((1,-1)) #restarts ball in random direction
    ball_speed_x *= random.choice((1,-1)) #restarts ball in random direction

def lPaddle(x, y):
  screen.blit(lPaddleImg, (x, y)) #draw the left player on the screen (VISUAL MOD)

def rPaddle(x, y):
  screen.blit(rPaddleImg, (x, y)) #draw the right player on the screen (VISUAL MOD)

def dBall(x, y):
  screen.blit(ballImg, (x, y)) #draw the ball on the screen (VISUAL MOD)

def pwrup_ready():
    if p1_pwrupReady:
        screen.blit(pwrupImg, (screen_width-60, 10))

    if p2_pwrupReady:
        screen.blit(pwrupImg, (10, 10))

def pwrup_check():
    global rPaddleImg, lPaddleImg
    curr_time = pygame.time.get_ticks()
    if curr_time - p1_used_pwrup >= 4000:
        player.height = 140
        rPaddleImg = pygame.transform.scale(rPaddleImg, (10, 140))
    if curr_time - p2_used_pwrup >= 4000:
        opponent.height = 140
        lPaddleImg = pygame.transform.scale(lPaddleImg, (10, 140))

    global p1_pwrupReady, p2_pwrupReady
    if curr_time - p1_used_pwrup >= 8000:
        p1_pwrupReady = True
    if curr_time - p2_used_pwrup >= 8000:
        p2_pwrupReady = True

def p1_pwrup():
    global rPaddleImg
    if p1_pwrupReady:
        player.height += 160
        rPaddleImg = pygame.transform.scale(rPaddleImg, (10, 300))

def p2_pwrup():
    global lPaddleImg
    if p2_pwrupReady:
        opponent.height += 160
        lPaddleImg = pygame.transform.scale(lPaddleImg, (10, 300))

# General setup
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2- 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

#Colours
white = (255,255,255)
light_grey = (200,200,200)
light_blue = (68,85,90)
bg_color = pygame.Color('grey12')
t_color = pygame.Color('grey12')


# Game Variables
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0 #if not pressing a key, player stands still
opponent_speed = 0
opponent_ai_speed = 7

# Ball (VISUAL)
ballImg = pygame.image.load("./media/ball.png")
ballX = screen_width / 2 - 15
ballY = screen_height / 2 - 15

# Right Paddle (VISUAL)
lPaddleImg = pygame.image.load("./media/lPaddle.png")
lPaddleX = 10
lPaddleY = screen_height / 2 - 70

# Right Paddle (VISUAL)
rPaddleImg = pygame.image.load("./media/rPaddle.png")
rPaddleX = screen_width - 20
rPaddleY = screen_height / 2 - 70

# Power Up variables
pwrupImg = pygame.image.load("./media/pwrup.png")
p1_pwrupReady = True
p2_pwrupReady = True
p1_used_pwrup = 0
p2_used_pwrup = 0
p2_pwrup_delay = 0

# Title Variables
multiplayer = False
title = True

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# Sound
pong_sound = pygame.mixer.Sound("./media/pong.ogg") #in the media folder
score_sound = pygame.mixer.Sound("./media/score.ogg") #in the media folder


while True and title == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                multiplayer = True
                opponent_speed = 0

            if event.key == pygame.K_LEFT:
                multiplayer = False
                opponent_speed = 7

            if event.key == pygame.K_RETURN:
                title = False

    screen.fill(t_color)

    titleFont = basic_font.render("PONG", False, white)
    screen.blit(titleFont,(600,200)) #blit puts one surface on another

    oneplayer = basic_font.render("One Player", False, white)
    screen.blit(oneplayer,(300,600)) #blit puts one surface on another

    twoplayer = basic_font.render("Two Players", False, white)
    screen.blit(twoplayer,(900,600)) #blit puts one surface on another

    if multiplayer == True:
        pygame.draw.line(screen, light_blue, (880,640), (1108, 640), 5)
    
    else:
        pygame.draw.line(screen, light_blue, (280,640), (490, 640), 5)

    pygame.display.flip()
    clock.tick(60)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: #key pressed
            if event.key ==pygame.K_UP: #up key
                player_speed -= 6

            if event.key == pygame.K_w and multiplayer == True: #w key
                    opponent_speed -= 6
            
            if event.key == pygame.K_DOWN: #down key
                player_speed += 6
                
            if event.key == pygame.K_s and multiplayer == True: #s key
                    opponent_speed += 6

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
       
        if event.type == pygame.KEYUP: #key unpressed
            if event.key == pygame.K_UP: #up key
                player_speed += 6
            if event.key == pygame.K_DOWN: #down key
                player_speed -= 6

            if event.key == pygame.K_w and multiplayer == True: #w key
                opponent_speed += 6
            if event.key == pygame.K_s and multiplayer == True: #s key
                opponent_speed -= 6
    
    


    ball_animation()
    player_animation()
    pwrup_check()
    if multiplayer == False:
        opponent_ai()
    else:
        opponent_animation()

    #once we're done with ball animation, let's put it in it's own function
    #remember: need to declare global variables for ball speeds

    # Visuals
    screen.fill(bg_color)
    #pygame.draw.rect(screen, light_grey, player)
    #pygame.draw.rect(screen, light_grey, opponent)
    #pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))
    pwrup_ready()

    rPaddle(rPaddleX, rPaddleY)
    lPaddle(lPaddleX, lPaddleY)
    dBall(ballX, ballY)

    # Creating the surface for text
    player_text = basic_font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text,(660,470)) #blit puts one surface on another

    opponent_text = basic_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text,(600,470)) #blit puts one surface on another


    #Loop Timer
    pygame.display.flip()
    clock.tick(60)
