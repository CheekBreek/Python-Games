import pygame

# Play Background Music 
def play_music(track): # Track corresponds to which wav file to choose according to current level 
    pygame.mixer.music.load(f"./media/background{track}.wav")  
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1) 

# Stop the Background Music
def stop_music():
    pygame.mixer.music.stop()

# Bullet Firing Sounds
def bullet_sounds(track): # Track corresponds to which wav file to choose according to current level 
    return pygame.mixer.Sound(f"./media/laser{track}.ogg")
