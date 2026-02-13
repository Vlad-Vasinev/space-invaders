import pygame.display
import pygame.event
import pygame.image
import pygame 
import time
from typing import List
import random

pygame.init()

screen_width: int = 950
screen_height: int = 550

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Space invaders v.1 by Vlad")

background_raw = pygame.image.load('data/bg.png').convert_alpha()
background_raw_2 = pygame.image.load('data/bg-2.png').convert_alpha()
background_raw_3 = pygame.image.load('data/bg-3.png').convert_alpha()

background = pygame.transform.scale(background_raw, (screen_width, screen_height))
background_2 = pygame.transform.scale(background_raw_2, (screen_width, screen_height))
background_3 = pygame.transform.scale(background_raw_3, (screen_width, screen_height))

backgrounds = [
  background, background_2, background_3
]

score_value = 0
score_x: int = 10
score_y: int = 10
font = pygame.font.Font('freesansbold.ttf', 22)

gameover_font = pygame.font.Font('freesansbold.ttf', 30)
  
player_image_raw = pygame.image.load('data/ship.png').convert_alpha()
player_image = pygame.transform.scale(player_image_raw, (50, 50))
player_x: int = 350
player_y: int = 490
player_x_change: int = 0
player_y_change: int = 0

invader_image: List = []
invader_x: List = []
invader_y: List = []
invader_xChange: List = []
invader_yChange: List = []
number_of_invaders: int = 10

explosion_raw = pygame.image.load('data/explosion.png').convert_alpha()
explosion_pic = pygame.transform.scale(explosion_raw, (70, 70))
explosion_rect = explosion_pic.get_rect()

invader_raw = pygame.image.load('data/invader.png').convert_alpha()
invader_pic = pygame.transform.scale(invader_raw, (50,50))

for i in range(number_of_invaders):
  invader_image.append(invader_pic)
  invader_x.append(random.randint(50, 600))
  invader_y.append(random.randint(50, 100))
  invader_xChange.append(random.uniform(0.5, 1.5))
  invader_yChange.append(random.randint(20, 35))
  
bullet_image_raw = pygame.image.load('data/bullet.png').convert_alpha()
bullet_image = pygame.transform.scale(bullet_image_raw, (20, 20))
bullet_x: int = 0
bullet_y: int = 0
bullet_x_change: int = 0
bullet_y_change: int = 2
bullet_state: str = "off"

def score_show(x, y):
  score = font.render("Score:" + str(score_value), True, (255, 255, 255))
  screen.blit(score, (x, y))
  
def game_over():
  game_over_text = gameover_font.render("GAME OVER", True, (255, 255, 255))
  text_rect = game_over_text.get_rect()
  text_rect.center = (screen_width // 2, screen_height // 2)
  screen.blit(game_over_text, text_rect)
  pygame.display.update()
  pygame.time.wait(7000)
  
def player(x, y): 
  screen.blit(player_image, (x- 16, y + 20))
  
def invader(x, y, i):
  screen.blit(invader_image[i], (x, y))
  
def bullet(x, y):
  global bullet_state
  screen.blit(bullet_image, (x, y))
  bullet_state = "fire"

#game Loop

bullet_cooldown: int = 0
cooldown_frames: int = 30

running: bool = True 

current_index: int = 0
current_counter: int = 0
current_interval: int = 60 * 12

clock = pygame.time.Clock()

hit_timer: List = [0] * number_of_invaders

while running: 
  
  current_counter += 1
  
  if(current_counter >= current_interval):
    current_index = (current_index + 1) % len(backgrounds)
    current_counter = 0
  
  screen.blit(backgrounds[current_index], (0, 0))
  
  for event in pygame.event.get(): 
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN: 
      if event.key == pygame.K_ESCAPE:
        running = False
      
      if event.key == pygame.K_LEFT:
        player_x_change = -1.2
      if event.key == pygame.K_RIGHT:
        player_x_change = +1.2
      if event.key == pygame.K_SPACE:
        if bullet_state == "off" and bullet_cooldown == 0:
          bullet_x = player_x
          bullet_y = player_y 
          bullet_state = "fire"
          bullet_cooldown = cooldown_frames
      if event.key == pygame.K_DOWN:
        player_x_change = 0
        player_y_change = +1
      if event.key == pygame.K_UP:
        player_x_change = 0
        player_y_change = -1
      if event.key == pygame.K_b:
        player_x_change = 0
        player_y_change = 0
        
  player_x += player_x_change
  player_y += player_y_change
  
  if bullet_y <= 0: 
    bullet_state = "off"
  if bullet_cooldown > 0:
    bullet_cooldown -= 1
  
  if player_x >= 900:
    player_x = 900
  if player_x <= 50:
    player_x = 50
  if player_y >= 500:
    player_y = 500
  if player_y <= 50:
    player_y = 50
  
  for i in range (number_of_invaders):
    
    player_rect = pygame.Rect(player_x, player_y, 50, 50)
    invader_rect = pygame.Rect(invader_x[i], invader_y[i], 50, 50)
    bullet_rect = pygame.Rect(bullet_x, bullet_y, 20, 20)
    
    if player_rect.colliderect(invader_rect):
      for j in range (number_of_invaders):
        invader_y[j] = 1000
      screen.blit(explosion_pic, (player_x, player_y))
      game_over()
      break
    if bullet_state == "fire" and bullet_rect.colliderect(invader_rect):
      
      if hit_timer[i] == 0:
        hit_timer[i] = 25
      
      if hit_timer[i] > 0:
        hit_timer[i] -= 1
        explosion_x = (invader_x[i] + 25 - explosion_pic.get_width() // 2)
        explosion_y = (invader_y[i] + 25 - explosion_pic.get_height() // 2)
        screen.blit(explosion_pic, (explosion_x, explosion_y))
        if hit_timer[i] == 0:
          score_value += 1 
          invader_x[i] = -1000
          invader_y[i] = -1000
          bullet_state = "off"
    
    if invader_x[i] >= 900 or invader_x[i] <= 0: 
      invader_xChange[i] *= -1
      invader_y[i] += invader_yChange[i]
      
    invader(invader_x[i], invader_y[i], i)
    
  if bullet_state == "fire":
    bullet(bullet_x, bullet_y)
    bullet_y -= bullet_y_change
  
  for i in range(number_of_invaders):
    invader_x[i] += invader_xChange[i]
    
  score_show(10,10)
  player(player_x, player_y)
  pygame.display.update()
  clock.tick(144)
    
        