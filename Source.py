import pygame
from pygame import *
from os import path
import winsound
import random


img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

lives_up = path.join(snd_dir, '1up1.wav')
key_up = path.join(snd_dir, 'Blip.wav')
coin_get = path.join(snd_dir, 'Coin.wav')
hit_enemy = path.join(snd_dir, 'Hit4.wav')
hit_player = path.join(snd_dir, 'Hit3.wav')
lost = path.join(snd_dir, 'Lose1.wav')
jump_snd = path.join(snd_dir, 'Jump4.wav')

green_lvl = True
ice_lvl = False

count_R = 0
count_L = 0

FPS = 60
k = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
infoScreen = pygame.display.Info()
WIDTH = infoScreen.current_w
HEIGHT = infoScreen.current_h
WIDTH = 1400
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 0)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Игра")
clock = pygame.time.Clock()

death_bg = pygame.image.load(path.join(img_dir, "red.jpg"))
death_bg = pygame.transform.scale(death_bg, (WIDTH, HEIGHT))
death_bg_rect = death_bg.get_rect()

victory_bg = pygame.image.load(path.join(img_dir, "win_img.jpg"))
victory_bg = pygame.transform.scale(victory_bg, (WIDTH, HEIGHT))
victory_bg_rect = victory_bg.get_rect()

player_img = pygame.image.load(path.join(img_dir, "p1_front.png"))

right_wall_img = pygame.image.load(path.join(img_dir, "houseDarkMidLeft.png"))
walls = [pygame.image.load(path.join(img_dir, "houseDarkAlt.png")),
         pygame.image.load(path.join(img_dir, "houseDarkAlt2.png"))]
clock_img = pygame.image.load(path.join(img_dir, "clock.png"))
sign_img = pygame.image.load(path.join(img_dir, "signHangingBed.png"))
rock_img = pygame.image.load(path.join(img_dir, "rockMoss.png"))
# rock_img = pygame.transform.scale(rock_img, (rock_img.get_rect().width * 2, rock_img.get_rect().height * 2))
roof_img = pygame.image.load(path.join(img_dir, "awningGreenRed.png"))

spikes_img = pygame.image.load(path.join(img_dir, "spikesssss.png"))
player_mini_img = pygame.image.load(path.join(img_dir, "hud_heartFull.png"))
player_mini_img2 = pygame.image.load(path.join(img_dir, "hud_heartEmpty.png"))

powerup_images = {'lives': pygame.image.load(path.join(img_dir, 'hud_heartFull.png')),
                  'coins': pygame.image.load(path.join(img_dir, 'hud_coins.png')),
                  'keys': pygame.image.load(path.join(img_dir, 'hud_keyYellow.png'))}

door_locked_down = pygame.image.load(path.join(img_dir, "doorLock.png"))
door_opened_down = pygame.image.load(path.join(img_dir, "doorOpen.png"))

door_locked_up = pygame.image.load(path.join(img_dir, "doorTop.png"))
door_opened_up = pygame.image.load(path.join(img_dir, "doorOpenTop.png"))

enemy_ghost_img = pygame.image.load(path.join(img_dir, "ghost.png"))
enemy_ghost_img_hit = pygame.image.load(path.join(img_dir, "ghost_hit.png"))
enemy_ghost_img_dead = pygame.image.load(path.join(img_dir, "ghost_dead.png"))

bridge_img = pygame.image.load(path.join(img_dir, "bridge.png"))
left_bank_img = pygame.image.load(path.join(img_dir, "grassCliffRightAlt.png"))
right_bank_img = pygame.image.load(path.join(img_dir, "grassCliffLeftAlt.png"))

fence_img1 = pygame.image.load(path.join(img_dir, "caneRed.png"))
wind_img_top = pygame.image.load(path.join(img_dir, "windowCheckered.png"))
wind_img_bot = pygame.image.load(path.join(img_dir, "windowHighCheckeredBottom.png"))
water_img = pygame.image.load(path.join(img_dir, "liquidWaterTop_mid.png"))

spin_img = pygame.image.load(path.join(img_dir, "spinner.png"))
spin_img2 = pygame.image.load(path.join(img_dir, "spinner_spin.png"))

fish_img_up = pygame.image.load(path.join(img_dir, "piranha.png"))
fish_img_down = pygame.image.load(path.join(img_dir, "piranha_down.png"))

all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
platforms = pygame.sprite.Group()
dangers_bl = pygame.sprite.Group()
dangers_en = pygame.sprite.Group()
powerups = pygame.sprite.Group()
powerups_lives = pygame.sprite.Group()
doors = pygame.sprite.Group()
dangers_ent_stopped = pygame.sprite.Group()
specTiles = pygame.sprite.Group()

pygame.mixer.music.load(path.join(snd_dir, '15 Clockwork Squares.wav'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)


class Pow(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
