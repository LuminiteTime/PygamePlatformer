import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

count_R = 0
count_L = 0

WIDTH = 1400
HEIGHT = 500
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (126, 46, 31)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 0)
pygame.display.set_caption("Игра")
clock = pygame.time.Clock()

background = pygame.image.load(path.join(img_dir, "bg_shroom.png"))
background = pygame.transform.scale(background, (1400, 500))
# background.set_alpha(100)
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "p1_front.png"))
block_img = pygame.image.load(path.join(img_dir, "grassMid.png"))

platform_mid_img = pygame.image.load(path.join(img_dir, "grassHalfMid.png"))
platform_r_img = pygame.image.load(path.join(img_dir, "grassHalfRight.png"))
platform_l_img = pygame.image.load(path.join(img_dir, "grassHalfLeft.png"))
plat_img = pygame.image.load(path.join(img_dir, "grassHalf.png"))

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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        # self.radius = 20
        self.playerx = WIDTH // 2
        self.playery = HEIGHT - 116
        self.speedx = 0
        self.isJumping = False
        self.gravity = 1.1
        self.velocity = 0
        self.rect.center = (self.playerx, self.playery)
        self.RIGHT = False
        self.LEFT = False
        self.MOVING = False
        self.lives = 3
        self.hide_timer = pygame.time.get_ticks()
        self.hidden = False
        self.begin = self.rect.center

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            player.speedx = -15
            self.LEFT = True
            self.RIGHT = False
            self.MOVING = True
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            player.speedx = 15
            self.RIGHT = True
            self.LEFT = False
            self.MOVING = True
        if not (keystate[pygame.K_RIGHT] or keystate[pygame.K_d]) and not (keystate[pygame.K_LEFT] or
                                                                           keystate[pygame.K_a]):
            self.MOVING = False

        self.rect.x += self.speedx

        touches = pygame.sprite.spritecollide(player, platforms, False)
        for i in touches:
            if player.rect.right >= i.rect.left and player.RIGHT:
                player.rect.right = i.rect.left
            elif player.rect.left <= i.rect.right and player.LEFT:
                player.rect.left = i.rect.right

        self.speedx = 0

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.image = player_img
            self.LEFT = False
            self.RIGHT = False
            self.rect.center = self.begin

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH // 2, HEIGHT + 1000)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.begin = self.rect.centery
        self.speedx = 0
        self.speedy = 0
        self.move = True
        self.lives = 3
        self.last = pygame.time.get_ticks()
        self.cooldown = 300
        self.isdead = False
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.frame = 0

    def update(self):
        if self.isdead:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == 3:
                    self.kill()
                else:
                    self.image = enemy_ghost_img_dead
        else:
            if self.move:
                self.speedy += -4
            if not self.move:
                self.speedy += 4
            if self.rect.bottom <= self.begin:
                self.move = False
                self.speedy = 0
                self.speedy += 4
            elif self.rect.top >= self.begin:
                self.speedy = 0
                self.speedy += -4
                self.move = True
            self.rect.bottom += self.speedy
            self.speedy = 0


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Danger_spikes(pygame.sprite.Sprite):
    def __init__(self, left, right, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        # self.radius = 20
        self.rect.left = left
        self.rect.right = right
        self.rect.top = y


class Pow(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, img_locked, img_opened):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_locked
        self.opened = img_opened
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        if is_key:
            self.image = self.opened


def draw_lives(surf, x, y, lives, img):
    if lives == 3:
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 55 * i
            img_rect.y = y
            surf.blit(img, img_rect)
    elif lives == 2:
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 55 * i
            img_rect.y = y
            surf.blit(img, img_rect)

        img_rect = img.get_rect()
        img_rect.x = x + 55 * 2
        img_rect.y = y
        surf.blit(player_mini_img2, img_rect)
    elif lives == 1:
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 55 * i
            img_rect.y = y
            surf.blit(img, img_rect)

        img_rect = img.get_rect()
        img_rect.x = x + 55
        img_rect.y = y
        surf.blit(player_mini_img2, img_rect)

        img_rect = img.get_rect()
        img_rect.x = x + 55 * 2
        img_rect.y = y
        surf.blit(player_mini_img2, img_rect)
    else:
        for i in range(3):
            img_rect = img.get_rect()
            img_rect.x = x + 55 * i
            img_rect.y = y
            surf.blit(player_mini_img2, img_rect)


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_item(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.centerx = x + 25
    img_rect.centery = y + 5
    surf.blit(img, img_rect)


def death():
    player.rect.center = player.begin
    player.lives -= 1
    player.hide()


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Простенький платформер", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Перемещение - стрелки или 'A' и 'D'", 22, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Прыжок - 'Пробел'", 22, WIDTH // 2, HEIGHT // 2 + 40)
    draw_text(screen, "Нажмите любую кнопку, чтобы начать", 18, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.quit()
            if event1.type == pygame.KEYUP:
                waiting = False


walking_anim = {'right': [], 'left': []}
for i in range(1, 12):
    filename = 'p1_walk0{}L.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename))
    img.set_colorkey(BLACK)
    walking_anim['left'].append(img)

    filename = 'p1_walk0{}R.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename))
    img.set_colorkey(BLACK)
    walking_anim['right'].append(img)

all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
platforms = pygame.sprite.Group()
dangers_bl = pygame.sprite.Group()
dangers_en = pygame.sprite.Group()
powerups = pygame.sprite.Group()
powerups_lives = pygame.sprite.Group()
doors = pygame.sprite.Group()

platform2 = Block(250, HEIGHT - 200, plat_img)
all_sprites.add(platform2)
platforms.add(platform2)

platform4 = Block(WIDTH // 2 + 50, HEIGHT - 250, plat_img)
all_sprites.add(platform4)
platforms.add(platform4)

im = 0
pl_0 = 0

for i in range(3):
    if i == 0:
        im = platform_l_img
        # im1 = platform_l_img
    if i == 1:
        im = platform_mid_img
        # im1 = platform_r_img
    if i == 2:
        im = platform_r_img
    platform1 = Block(WIDTH // 2 - 300 + 69 * i, HEIGHT - 300, im)
    all_sprites.add(platform1)
    platforms.add(platform1)
    # if i == 0 or i == 1:
    #     platform3 = Block(WIDTH // 2 + 90 + 69 * i, HEIGHT - 250, im1)
    #     all_sprites.add(platform3)
    #     platforms.add(platform3)
    if i == 0:
        pl_l = platform1
        # pl_l1 = platform3
    if i == 1:
        pl_0 = platform1
        # pl_01 = platform3
    if i == 2:
        pl_r = platform1
        # pl_r1 = platform3

spikes = Danger_spikes(pl_l.rect.left - 2, pl_r.rect.right - 2, pl_l.rect.bottom, spikes_img)
all_sprites.add(spikes)
dangers_bl.add(spikes)

for i in range(21):
    block = Block(70 * i, HEIGHT - 35, block_img)
    all_sprites.add(block)
    blocks.add(block)

door_down = Door(WIDTH - 50, block.rect.top, door_locked_down, door_opened_down)
all_sprites.add(door_down)
doors.add(door_down)
door_up = Door(WIDTH - 50, door_down.rect.top, door_locked_up, door_opened_up)
all_sprites.add(door_up)
doors.add(door_up)

enemy_ghost = Enemy(platform4.rect.centerx + 50, block.rect.top - 30, enemy_ghost_img)
all_sprites.add(enemy_ghost)
dangers_en.add(enemy_ghost)

pow_live = Pow(pl_0.rect.centerx, pl_0.rect.top - 25, 'lives')
all_sprites.add(pow_live)
powerups_lives.add(pow_live)

pow_key = Pow(platform2.rect.centerx, platform2.rect.top - 25, 'keys')
all_sprites.add(pow_key)
powerups.add(pow_key)

for i in range(3):
    pow_coin = Pow(pl_l.rect.centerx + 90 * i, block.rect.top - 25, 'coins')
    all_sprites.add(pow_coin)
    powerups.add(pow_coin)

player = Player()
all_sprites.add(player)

# Цикл игры
running = True
up = False
down = False
score = 0
is_key = False
lava = False
on_block = True
game_over = True

while running:
    if game_over:
        show_go_screen()
        game_over = False

        all_sprites = pygame.sprite.Group()
        blocks = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        dangers_bl = pygame.sprite.Group()
        dangers_en = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        powerups_lives = pygame.sprite.Group()
        doors = pygame.sprite.Group()

        platform2 = Block(250, HEIGHT - 200, plat_img)
        all_sprites.add(platform2)
        platforms.add(platform2)

        platform4 = Block(WIDTH // 2 + 50, HEIGHT - 250, plat_img)
        all_sprites.add(platform4)
        platforms.add(platform4)

        im = 0
        pl_0 = 0

        for i in range(3):
            if i == 0:
                im = platform_l_img
                # im1 = platform_l_img
            if i == 1:
                im = platform_mid_img
                # im1 = platform_r_img
            if i == 2:
                im = platform_r_img
            platform1 = Block(WIDTH // 2 - 300 + 69 * i, HEIGHT - 300, im)
            all_sprites.add(platform1)
            platforms.add(platform1)
            # if i == 0 or i == 1:
            #     platform3 = Block(WIDTH // 2 + 90 + 69 * i, HEIGHT - 250, im1)
            #     all_sprites.add(platform3)
            #     platforms.add(platform3)
            if i == 0:
                pl_l = platform1
                # pl_l1 = platform3
            if i == 1:
                pl_0 = platform1
                # pl_01 = platform3
            if i == 2:
                pl_r = platform1
                # pl_r1 = platform3

        spikes = Danger_spikes(pl_l.rect.left - 2, pl_r.rect.right - 2, pl_l.rect.bottom, spikes_img)
        all_sprites.add(spikes)
        dangers_bl.add(spikes)

        for i in range(21):
            block = Block(70 * i, HEIGHT - 35, block_img)
            all_sprites.add(block)
            blocks.add(block)

        door_down = Door(WIDTH - 50, block.rect.top, door_locked_down, door_opened_down)
        all_sprites.add(door_down)
        doors.add(door_down)
        door_up = Door(WIDTH - 50, door_down.rect.top, door_locked_up, door_opened_up)
        all_sprites.add(door_up)
        doors.add(door_up)

        enemy_ghost = Enemy(platform4.rect.centerx + 50, block.rect.top - 30, enemy_ghost_img)
        all_sprites.add(enemy_ghost)
        dangers_en.add(enemy_ghost)

        pow_live = Pow(pl_0.rect.centerx, pl_0.rect.top - 25, 'lives')
        all_sprites.add(pow_live)
        powerups_lives.add(pow_live)

        pow_key = Pow(platform2.rect.centerx, platform2.rect.top - 25, 'keys')
        all_sprites.add(pow_key)
        powerups.add(pow_key)

        for i in range(3):
            pow_coin = Pow(pl_l.rect.centerx + 90 * i, block.rect.top - 25, 'coins')
            all_sprites.add(pow_coin)
            powerups.add(pow_coin)

        player = Player()
        all_sprites.add(player)

        up = False
        down = False
        is_key = False
        lava = False
        on_block = True
        score = 0

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_w) and not player.isJumping:
                player.isJumping = True
                player.velocity = 100
                on_block = False

    # Обновление
    if player.isJumping:
        player.velocity -= int(player.gravity * 20)
        if player.velocity > 0:
            up = True
            down = False
        if player.velocity < 0:
            up = False
            down = True
    player.rect.bottom -= player.velocity

    if player.rect.bottom >= block.rect.top and not player.hidden:
        player.rect.bottom = block.rect.top
        player.isJumping = False
        player.velocity = 0
        up = False
        down = False

    if player.RIGHT:
        if player.isJumping:
            player.image = pygame.image.load(path.join(img_dir, "p1_jumpR.png"))
            player.image.set_colorkey(BLACK)
        elif player.MOVING:
            player.image = walking_anim['right'][count_R]
            count_R += 1
            if count_R >= 11:
                count_R = 0
        elif not player.MOVING and not player.MOVING:
            player.image = pygame.image.load(path.join(img_dir, "p1_standR.png"))
            player.image.set_colorkey(BLACK)

    if player.LEFT:
        if player.isJumping:
            player.image = pygame.image.load(path.join(img_dir, "p1_jumpL.png"))
            player.image.set_colorkey(BLACK)
        elif player.MOVING:
            player.image = walking_anim['left'][count_L]
            count_L += 1
            if count_L >= 11:
                count_L = 0
        elif not player.MOVING and not player.MOVING:
            player.image = pygame.image.load(path.join(img_dir, "p1_standL.png"))
            player.image.set_colorkey(BLACK)

    if up:
        touches = pygame.sprite.spritecollide(player, dangers_bl, False)
        for i in touches:
            death()

        touches = pygame.sprite.spritecollide(player, platforms, False)
        for i in touches:
            if player.rect.top <= i.rect.bottom:
                player.rect.top = i.rect.bottom
                player.velocity = -player.velocity

    if down:
        touches = pygame.sprite.spritecollide(player, platforms, False)
        for i in touches:
            if player.rect.bottom >= i.rect.top:
                player.rect.bottom = i.rect.top
                player.isJumping = False

    if player.lives == 3:
        powerups_touches_lives = pygame.sprite.spritecollide(player, powerups_lives, False)
        for i in powerups_touches_lives:
            pass

        powerups_touches = pygame.sprite.spritecollide(player, powerups, True)
        for i in powerups_touches:
            if i.type == 'coins':
                score += 100
            if i.type == 'keys':
                is_key = True
    else:
        powerups_touches = pygame.sprite.spritecollide(player, powerups, True)
        powerups_touches_lives = pygame.sprite.spritecollide(player, powerups_lives, True)
        for i in powerups_touches_lives:
            if i.type == 'lives':
                player.lives += 1
                if player.lives >= 3:
                    player.lives = 3
        for i in powerups_touches:
            if i.type == 'coins':
                score += 100
            if i.type == 'keys':
                is_key = True

    doors_hits = pygame.sprite.spritecollide(player, doors, False)
    for hit in doors_hits:
        if is_key:
            running = False

    enemy_hits = pygame.sprite.spritecollide(player, dangers_en, False)
    for hit in enemy_hits:
        if down:
            hit.image = enemy_ghost_img_hit
            hit.lives -= 1
            if hit.lives <= 0:
                hit.isdead = True
                score += 500
            player.isJumping = True
            player.velocity = 100
            on_block = False
        else:
            death()

    now = pygame.time.get_ticks()
    if now - enemy_ghost.last >= enemy_ghost.cooldown:
        enemy_ghost.last = now
        enemy_ghost.image = enemy_ghost_img

    if player.lives <= 0:
        running = False

    all_sprites.update()
    # Рендеринг
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    if is_key:
        draw_item(screen, 0, 70, powerup_images['keys'])
    draw_lives(screen, 0, 5, player.lives, player_mini_img)
    draw_text(screen, str(score), 50, WIDTH // 2, 10)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
