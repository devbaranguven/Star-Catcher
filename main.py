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

# Oyun objeleri için resimler yükleniyor ve ayarlanıyor
ufo_img = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "ufo.png")), (65, 65))
yildiz_img = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "yildiz.png")), (30, 40))
uzay_gemisi_img = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "uzay_gemisi.png")), (65, 65))
meteor_img = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "meteor.png")), (30, 30))
secret_img = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "kalp.png")), (200, 200))

# Arka plan müziği ayarlanıyor
pygame.mixer.music.load(os.path.join(sound_path, "music.mp3"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

#Çarpma sesi
explosion_sound = pygame.mixer.Sound(os.path.join(sound_path, "explosion.mp3"))
explosion_sound.set_volume(0.5)

#Yazı tipi
font = pygame.font.Font(None, 36)

# Sis animasyonu (meteor çarpınca çıkan efekt)
sis_images = []
for i in range(1, 25):
    img = pygame.image.load(f"sis/sis{i}.png")
    img = pygame.transform.scale(img, (80, 80))
    sis_images.append(img)

# Alev animasyonu (uzay gemisi altı)
    flame_images = []
for i in range(9):  # explosion00 - explosion08
    img = pygame.image.load(f"explosion/explosion0{i}.png")
    img = pygame.transform.scale(img, (30, 30))
    flame_images.append(img)

#Game Over ekranı
def game_over_screen(score):
    pygame.mixer.music.stop()
    screen.blit(bg_img, (0, 0))
    game_over_text = font.render("GAME OVER", True, RED)
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    restart_text = font.render("Restart", True, WHITE)

    restart_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 - 120, 120, 50)

    screen.blit(game_over_text, (screen_width // 2 - 80, screen_height // 2 - 60))
    screen.blit(final_score_text, (screen_width // 2 - 80, screen_height // 2 - 20))
    screen.blit(restart_text, (screen_width // 2 - 50, screen_height // 2 - 120))
    pygame.display.flip()

  # Butona tıklanmayı bekle
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return
    
#Ana oyun döngüsü
def run_game():
    pygame.mixer.music.play(-1)
    flame_frame = 0
    ufo_x = 400
    ufo_y = 100
    ufo_speed_x = 4
    ufo_speed_y = 2

    uzay_gemisi_x = 400
    uzay_gemisi_y = screen_height - 100
    uzay_gemisi_speed = 7

    yildizlar = []
    meteorlar = []
    animations = []

    score = 0
    missed_yildiz = 0
    health = 4
    yildiz_speed = 3
    yildiz_speed_increase_time = time.time()
    paused_at_143 = False

    running = True    
    while running:
        screen.blit(bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:
                uzay_gemisi_x = int(event.x * screen_width) - 32

        if missed_yildiz >= 3 or health <= 0:
            game_over_screen(score)
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and uzay_gemisi_x > 0:
            uzay_gemisi_x -= uzay_gemisi_speed
        if keys[pygame.K_RIGHT] and uzay_gemisi_x + 65 < screen_width:
            uzay_gemisi_x += uzay_gemisi_speed

        if time.time() - yildiz_speed_increase_time > 20:
            yildiz_speed += 1
            yildiz_speed_increase_time = time.time()      
        
        
        #Ufo hareketi
        ufo_x += ufo_speed_x
        ufo_y += ufo_speed_y
        if ufo_x + 65 >= screen_width or ufo_x <= 0:
            ufo_speed_x *= -1
        if ufo_y >= 150 or ufo_y <= 50:
            ufo_speed_y *= -1

        # Yıldız veya meteor düşür
        if random.randint(1, 100) > 98:
            drop_x = ufo_x + 32
            drop_y = ufo_y + 65
            if random.randint(1, 100) <= 75:
                yildizlar.append([drop_x, drop_y])
            else:
                meteorlar.append([drop_x, drop_y])

        
         # Yıldızları güncelle
        yeni_yildizlar = []
        for yildiz in yildizlar:
            yildiz[1] += yildiz_speed
            if uzay_gemisi_y < yildiz[1] + 40 < uzay_gemisi_y + 65 and uzay_gemisi_x < yildiz[0] + 15 < uzay_gemisi_x + 65:
                score += 1
                missed_yildiz = 0
            elif yildiz[1] >= screen_height:
                missed_yildiz += 1
            else:
                yeni_yildizlar.append(yildiz)
        yildizlar = yeni_yildizlar

        # Meteorları güncelle
        yeni_meteorlar = []
        for meteor in meteorlar:
            meteor[1] += yildiz_speed
            if uzay_gemisi_y < meteor[1] + 30 < uzay_gemisi_y + 65 and uzay_gemisi_x < meteor[0] + 15 < uzay_gemisi_x + 65:
                health -= 1
                explosion_sound.play()
                animations.append({"x": meteor[0], "y": meteor[1], "frame": 0})
            elif meteor[1] < screen_height:
                yeni_meteorlar.append(meteor)
        meteorlar = yeni_meteorlar

         # Obje çizimi
        screen.blit(ufo_img, (ufo_x, ufo_y))
        for yildiz in yildizlar:
            screen.blit(yildiz_img, (yildiz[0], yildiz[1]))
        for meteor in meteorlar:
            screen.blit(meteor_img, (meteor[0], meteor[1]))
        screen.blit(flame_images[flame_frame], (uzay_gemisi_x + 17, uzay_gemisi_y + 55))
        screen.blit(uzay_gemisi_img, (uzay_gemisi_x, uzay_gemisi_y))

        
        # Sis animasyonu (meteor çarpınca)
        yeni_animations = []
        for anim in animations:
            if anim["frame"] < len(sis_images):
                screen.blit(sis_images[anim["frame"]], (anim["x"], anim["y"]))
                anim["frame"] += 1
                yeni_animations.append(anim)
        animations = yeni_animations

        # Skorlar,kaçırılan ve sağlık bilgisi
        score_text = font.render(f"Score: {score}", True, BLUE)
        missed_text = font.render(f"Missed: {missed_yildiz}/3", True, RED)
        health_text = font.render(f"Health: {health}", True, GREEN)
        screen.blit(score_text, (20, 20))
        screen.blit(missed_text, (screen_width - 150, 20))
        screen.blit(health_text, (screen_width // 2 - 70, 20))

        # Gizli sürpriz
        if score == 143 and not paused_at_143:
            screen.blit(secret_img, (screen_width // 2 - 100, screen_height // 2 - 100))
            pygame.display.flip()
            paused = True
            while paused:
                for event in pygame.event.get():
                    if event.type in [pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN]:
                        paused = False
            paused_at_143 = True

        pygame.display.flip()
        flame_frame = (flame_frame + 1) % len(flame_images)
        pygame.time.delay(40)

while True:
    run_game()
