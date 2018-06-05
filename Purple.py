import pygame
import time
import os

print(pygame.version.ver)
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
#screen = pygame.display.set_mode((350,10)) #create a screen
pygame.mixer.music.load("C:\\Users\pgrimsrud\\NES\\bot\img\Purple.mp3")
#pygame.mixer.music.load("C:\Users\pgrimsrud\NES\\bot\img\Purple.mp3")
#time.sleep(1)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pass