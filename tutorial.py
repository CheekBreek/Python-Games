import pygame, sys, random

def ball_animation():

    global ball_speed_x, ball_speed_y, player_score, opponent_score
    
    #Game Logic
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    #Ball Collision (Top of Bottom)
    if ball.top <= 0 or ball.bottom >= screen_height:
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
    player.y += player_speed

    if player.top <= 0:
        player.top = 0 #puts player at the top of screen
    if player.bottom >= screen_height:
        player.bottom = screen_height #puts player at bottom

def opponent_animation():
    opponent.y += opponent_speed

    if opponent.top <= 0:
        opponent.top = 0 #puts player at the top of screen
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height #puts player at bottom

def opponent_ai():
    if opponent.top < ball.y: #opponent above ball
        opponent.y += opponent_speed
    if opponent.bottom > ball.y: #opponent below ball
        opponent.y -= opponent_speed
    
    if opponent.top <= 0: #oppoent at top of screen
        opponent.top = 0
    if opponent.bottom >= screen_height: #opponent at bottom
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y

    #move ball to center
    ball.center = (screen_width/2, screen_height/2)

    #start the ball in a random direction
    ball_speed_y *= random.choice((1,-1)) #restarts ball in random direction
    ball_speed_x *= random.choice((1,-1)) #restarts ball in random direction

# Generates Texts
def text_generator(text, x, y, fontSize):
    font = pygame.font.Font("freesansbold.ttf", fontSize)
    text1 = font.render(text, False, white, t_color)

    # Centering/Aligning the Text
    text1_width = text1.get_width()
    text1_height = text1.get_height()
    textRect = text1.get_rect()
    textRect.center = (x + text1_width / 2, y - text1_height / 2)

    screen.blit(text1, textRect)

# Generates Images
def image_generator(filename, x, y):
    image = pygame.image.load(f'./media/{filename}')
    screen.blit(image, (x,y))

# Pong Game
def game():  
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
        if multiplayer == False:
            opponent_ai()
        else:
            opponent_animation()

        #once we're done with ball animation, let's put it in it's own function
        #remember: need to declare global variables for ball speeds

        # Visuals
        screen.fill(bg_color)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

        # Creating the surface for text
        player_text = basic_font.render(f'{player_score}', False, light_grey)
        screen.blit(player_text,(660,470)) #blit puts one surface on another

        opponent_text = basic_font.render(f'{opponent_score}', False, light_grey)
        screen.blit(opponent_text,(600,470)) #blit puts one surface on another


        #Loop Timer
        pygame.display.flip()
        clock.tick(60)   

# Tutorial Page
def tutorial():
    global mouse

    while True:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN: # click "Start Game" button
                if screen_width-200 <= mouse[0] <= screen_width - 67 and screen_height -50 <= mouse [1] <= screen_height +15:
                    game() # Game is started
                
        
        screen.fill(bg_color)
        
        # Controls
        text_generator("Controls", 50, 50, 32)

        # Player 1
        text_generator("Player 1", 100, 90, 24)
        image_generator("icons8-w-key-96.png", 150, 100)
        image_generator("icons8-s-key-96.png", 150, 200)
        image_generator("icons8-space-key-96.png", 150, 300)
        text_generator("Up", 300, 170, 20)
        text_generator("Down", 300, 270, 20)
        text_generator("Power Up", 300, 370, 20)

        # Player 2
        text_generator("Player 2", screen_width / 2 + 10, 90, 24)
        image_generator("icons8-page-up-button-96.png", screen_width / 2 + 60, 100)
        image_generator("icons8-page-down-button-96.png", screen_width / 2 + 60, 200)
        image_generator("icons8-0-key-96.png", screen_width / 2 + 60, 300)
        text_generator("Up", screen_width / 2 + 210, 170, 20)
        text_generator("Down", screen_width / 2 + 210, 270, 20)
        text_generator("Power Up (Keypad 0)", screen_width / 2 + 210, 370, 20)
        
        # PowerUps
        text_generator("Power Ups", 50, 450, 32)
        text_generator("Power UP - Paddle gets larger", 300, 550, 16)

        # Mouse
        mouse = pygame.mouse.get_pos()
        if screen_width -200 <= mouse[0] <= screen_width - 67 and screen_height -50 <= mouse[1] <= screen_height +15: 
            pygame.draw.rect(screen,(t_color),[screen_width-200,screen_height-50,153,35])   # hovering around button
        else: 
            pygame.draw.rect(screen,(white),[screen_width-200,screen_height-50,153,35])  # not hovering around button
        
        # Board Hazards
        text_generator("Board Hazards", 50, 700, 32)
        text_generator("Blackhole - Ball is sucked in, and ejected at a random speed and direction", 300, 800, 16)
        text_generator("Start Game", screen_width - 190, screen_height - 20, 24)
        
        pygame.display.update()


# General setup
pygame.init()
clock = pygame.time.Clock()

# Screen
screen_height = 960
screen_width = 1280
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

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
                tutorial()

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