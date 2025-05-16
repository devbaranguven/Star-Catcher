#oyun için gerekli kütüphaneler
import pygame
import random
import time
import os

pygame.init()

#Ekran boyutu,pencere ve başlık oluşturuluyor
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("UFO Star Catch")

# Renk tanımlamaları
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
#Resim ve ses dosyaları
image_path = os.path.join("oyun_resimleri")
sound_path = os.path.join("sesler")

#Arka plan
bg_img = pygame.image.load(os.path.join(image_path, "arka_plan.png"))
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))