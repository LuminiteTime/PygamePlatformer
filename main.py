from levels import *
from Source import *
from Spec_tiles import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.playerx = WIDTH // 2
        self.playery = HEIGHT - 135
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
        if (keystate[pygame.K_LEFT] or keystate[pygame.K_a]) and not self.hidden:
            player.speedx = -15
            self.LEFT = True
            self.RIGHT = False
            self.MOVING = True
        if (keystate[pygame.K_RIGHT] or keystate[pygame.K_d]) and not self.hidden:
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

        if self.rect.right > WIDTH + 300:
            self.rect.right = WIDTH + 300
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0

    def hide(self):
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


class Spinner(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.begin = self.rect.centery
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30
        self.frame = 0
        self.R = True
        self.L = False

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.R:
                self.R = False
                self.L = True
                self.image = spin_img2
            elif self.L:
                self.R = True
                self.L = False
                self.image = spin_img


class Fish(pygame.sprite.Sprite):
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

    def update(self):
        if self.move:
            self.speedy += -6
        if not self.move:
            self.speedy += 6
        if self.rect.bottom <= self.begin:
            self.move = False
            self.speedy = 0
            self.speedy += 6
            self.image = fish_img_down
        elif self.rect.top >= self.begin + 70:
            self.speedy = 0
            self.speedy += -6
            self.move = True
            self.image = fish_img_up
        self.rect.bottom += self.speedy
        self.speedy = 0


class Fake_Ghost(pygame.sprite.Sprite):
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
        self.last = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.frame = 0

    def update(self):
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
        self.blockx = x
        self.blocky = y
        self.rect.center = (self.blockx, self.blocky)


class Danger_spikes(pygame.sprite.Sprite):
    def __init__(self, left, right, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.right = right
        self.rect.bottom = y


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


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIDTH / 2, -t + HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


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


def draw_text(surf, text, size, x, y, is_lvl):
    font = pygame.font.Font(font_name, size)
    color = WHITE
    if is_lvl:
        if levels_themes[level_num] == 'ice':
            color = BLACK
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_item(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.centerx = x + 25
    img_rect.centery = y + 5
    surf.blit(img, img_rect)


def death():
    winsound.PlaySound(hit_player, winsound.SND_ASYNC | winsound.SND_ALIAS)
    player.rect.center = player.begin
    player.lives -= 1
    player.hide()


def show_go_screen():
    screen.blit(pygame.transform.scale(pygame.image.load(path.join(img_dir, "start_bg.png")),
                                       (WIDTH, HEIGHT)),
                pygame.transform.scale(pygame.image.load(path.join(img_dir, "start_bg.png")),
                                       (WIDTH, HEIGHT)).get_rect())
    # draw_text(screen, "Платформер", 64, WIDTH // 2, HEIGHT // 4, False)
    draw_text(screen, "Перемещение - стрелки или 'A' и 'D'. 'esc' - выход из игры", 22, WIDTH // 2, HEIGHT // 2, False)
    draw_text(screen, "Прыжок - 'Пробел'", 22, WIDTH // 2, HEIGHT // 2 + 40, False)
    draw_text(screen, "Нажмите любую кнопку, чтобы начать", 18, WIDTH // 2, HEIGHT * 3 // 4, False)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.quit()
            if event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_ESCAPE:
                    pygame.quit()
                else:
                    waiting = False


def show_win_screen():
    screen.blit(victory_bg, victory_bg_rect)
    draw_text(screen, f"Уровень {level_num} пройден! Ваш счет: {score}", 64, WIDTH // 2, HEIGHT // 4, False)
    draw_text(screen, "Перемещение - стрелки или 'A' и 'D'", 22, WIDTH // 2, HEIGHT // 2, False)
    draw_text(screen, "Прыжок - 'Пробел'", 22, WIDTH // 2, HEIGHT // 2 + 40, False)
    draw_text(screen, "Нажмите любую кнопку, чтобы начать следующий уровень!", 18, WIDTH // 2, HEIGHT * 3 // 4, False)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.quit()
            if event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_ESCAPE:
                    pygame.quit()
                else:
                    waiting = False


def show_end_screen():
    winsound.PlaySound(lost, winsound.SND_ASYNC | winsound.SND_ALIAS)
    screen.blit(death_bg, death_bg_rect)
    draw_text(screen, f"Вы старались! Ваш счет: {score}", 64, WIDTH // 2, HEIGHT // 4, False)
    draw_text(screen, "Конец игры", 22, WIDTH // 2, HEIGHT // 2, False)
    draw_text(screen, "Нажмите любую кнопку, чтобы начать заново", 18, WIDTH // 2, HEIGHT * 3 // 4, False)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.quit()
            if event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_ESCAPE:
                    pygame.quit()
                else:
                    waiting = False
                    player.lives = 3


def show_final_screen():
    screen.blit(victory_bg, victory_bg_rect)
    draw_text(screen, f"Вы прошли игру! Ваш общий счет: {res}", 64, WIDTH // 2, HEIGHT // 4, False)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.quit()


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

message = False


def create_lvl(level, theme):
    x = y = 0
    clo = False
    roo = False
    for row in level:
        for col in row:
            if col == "-":
                pf = Block(x, y, pygame.image.load(path.join(img_dir, theme + "Half.png")))
                platforms.add(pf)
                all_sprites.add(pf)
            if col == "_":
                global block
                block = Block(x, y + 5, pygame.image.load(path.join(img_dir, theme + "Mid.png")))
                all_sprites.add(block)
                platforms.add(block)
            if col == "r":
                pf = Block(x, y, right_wall_img)
                all_sprites.add(pf)
            if clo:
                cl = Block(x1, y1 - 40, clock_img)
                all_sprites.add(cl)
                clo = False
            if roo:
                ro = Block(x2, y2 - 40, roof_img)
                all_sprites.add(ro)
                roo = False
            if col == "w" or col == "C" or col == "R":
                pf = Block(x, y, random.choice(walls))
                all_sprites.add(pf)
                if col == "C":
                    clo = True
                    x1 = x
                    y1 = y
                if col == "R":
                    roo = True
                    x2 = x
                    y2 = y
            if col == "s":
                global spikes
                spikes = Danger_spikes(x - 30, x + 170, y + 14, spikes_img)
                all_sprites.add(spikes)
                dangers_bl.add(spikes)
            if col == "g":
                global enemy_ghost
                enemy_ghost = Enemy(x, y, enemy_ghost_img)
                all_sprites.add(enemy_ghost)
                dangers_en.add(enemy_ghost)
            if col == "f":
                fg = Fake_Ghost(x, y, enemy_ghost_img)
                all_sprites.add(fg)
            if col == "h":
                global pow_live
                pow_live = Pow(x, y, 'lives')
                all_sprites.add(pow_live)
                powerups_lives.add(pow_live)
            if col == "k":
                global pow_key
                pow_key = Pow(x, y, 'keys')
                all_sprites.add(pow_key)
                powerups.add(pow_key)
            if col == "c":
                global pow_coin
                pow_coin = Pow(x, y, 'coins')
                all_sprites.add(pow_coin)
                powerups.add(pow_coin)
            if col == "t":
                st = Block(x, y + 15, rock_img)
                all_sprites.add(st)
            if col == "S":
                si = Block(x, y, sign_img)
                all_sprites.add(si)
            if col == "b":
                ba = Block(x, y + 5, left_bank_img)
                platforms.add(ba)
                all_sprites.add(ba)
            if col == "d":
                ba = Block(x, y + 5, right_bank_img)
                platforms.add(ba)
                all_sprites.add(ba)
            if col == "m":
                br = Block(x, y - 20, bridge_img)
                platforms.add(br)
                all_sprites.add(br)
            if col == "x":
                global message
                message = True
                global x_mes
                x_mes = x
                global y_mes
                y_mes = y
            if col == "=":
                di = Block(x, y + 30, pygame.image.load(path.join(img_dir, theme + "Center.png")))
                all_sprites.add(di)
            if col == "y":
                fe = Block(x, y, fence_img1)
                all_sprites.add(fe)
            if col == "i":
                pf = Block(x, y, random.choice(walls))
                all_sprites.add(pf)
                fe = Block(x, y - 40, wind_img_top)
                all_sprites.add(fe)
            if col == "I":
                pf = Block(x, y, random.choice(walls))
                all_sprites.add(pf)
                fe = Block(x, y - 40, wind_img_bot)
                all_sprites.add(fe)
            if col == "W":
                pf = Block(x, y + 5, water_img)
                all_sprites.add(pf)
            if col == "P":
                spinner = Spinner(x, y, spin_img)
                all_sprites.add(spinner)
                dangers_ent_stopped.add(spinner)
            if col == "F":
                fish = Fish(x, y, fish_img_up)
                all_sprites.add(fish)
                dangers_ent_stopped.add(fish)
            if col == "М":
                pow_coin = Pow(x, y + 20, 'coins')
                all_sprites.add(pow_coin)
                powerups.add(pow_coin)

                coinBlock = CoinBlock(x, y, pygame.image.load(path.join(img_dir, "boxCoin.png")))
                all_sprites.add(coinBlock)
                platforms.add(coinBlock)
                specTiles.add(coinBlock)

            x += 69
        y += 40
        x = 0

    global door_down
    door_down = Door(WIDTH - 50, block.rect.top, door_locked_down, door_opened_down)
    all_sprites.add(door_down)
    doors.add(door_down)
    global door_up
    door_up = Door(WIDTH - 50, door_down.rect.top, door_locked_up, door_opened_up)
    all_sprites.add(door_up)
    doors.add(door_up)
    global player
    player = Player()
    all_sprites.add(player)


running = True
up = False
down = False
score = 0
is_key = False
on_block = True
game_over = True

level_num = 1
again = False
res = 0

total_level_width = len(levels[level_num][0]) * 69  # Высчитываем фактическую ширину уровня
total_level_height = len(levels[level_num]) * 40  # высоту

camera = Camera(camera_configure, total_level_width, total_level_height)

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
        dangers_ent_stopped = pygame.sprite.Group()
        specTiles = pygame.sprite.Group()

        create_lvl(levels[level_num], levels_themes[level_num])

        up = False
        down = False
        is_key = False
        on_block = True
        score = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_w) and not player.isJumping:
                player.isJumping = True
                winsound.PlaySound(jump_snd, winsound.SND_ASYNC | winsound.SND_ALIAS)
                player.velocity = 100
                on_block = False
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

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
                if isinstance(i, CoinBlock):
                    i.activate()
                    i.lifes -= 1
                    if i.lifes <= 0:
                        i.kill()

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
                winsound.PlaySound(coin_get, winsound.SND_ASYNC | winsound.SND_ALIAS)
                score += 100
            if i.type == 'keys':
                winsound.PlaySound(key_up, winsound.SND_ASYNC | winsound.SND_ALIAS)
                is_key = True
    else:
        powerups_touches = pygame.sprite.spritecollide(player, powerups, True)
        powerups_touches_lives = pygame.sprite.spritecollide(player, powerups_lives, True)
        for i in powerups_touches_lives:
            if i.type == 'lives':
                winsound.PlaySound(lives_up, winsound.SND_ASYNC | winsound.SND_ALIAS)
                player.lives += 1
                if player.lives >= 3:
                    player.lives = 3
        for i in powerups_touches:
            if i.type == 'coins':
                winsound.PlaySound(coin_get, winsound.SND_ASYNC | winsound.SND_ALIAS)
                score += 100
            if i.type == 'keys':
                winsound.PlaySound(key_up, winsound.SND_ASYNC | winsound.SND_ALIAS)
                is_key = True

    touches = pygame.sprite.spritecollide(player, dangers_ent_stopped, False)
    for i in touches:
        death()

    doors_hits = pygame.sprite.spritecollide(player, doors, False)
    for hit in doors_hits:
        if is_key:
            res += score
            show_win_screen()
            level_num += 1
            message = False
            for i in all_sprites:
                i.kill()
            try:
                create_lvl(levels[level_num], levels_themes[level_num])
            except Exception as e:
                show_final_screen()
            score = 0
            is_key = False

    enemy_hits = pygame.sprite.spritecollide(player, dangers_en, False)
    for hit in enemy_hits:
        if down:
            winsound.PlaySound(hit_enemy, winsound.SND_ASYNC | winsound.SND_ALIAS)
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
        show_end_screen()
        for i in all_sprites:
            i.kill()
        create_lvl(levels[level_num], levels_themes[level_num])
        again = True

        score = 0
        is_key = False

    all_sprites.update()
    screen.blit(pygame.transform.scale(pygame.image.load(path.join(img_dir, levels_themes[level_num] + "_bg.png")),
                                       (WIDTH, HEIGHT)),
                pygame.transform.scale(pygame.image.load(path.join(img_dir, levels_themes[level_num] + "_bg.png")),
                                       (WIDTH, HEIGHT)).get_rect())
    camera.update(player)
    for e in all_sprites:
        screen.blit(e.image, camera.apply(e))
    if is_key:
        draw_item(screen, 0, 70, powerup_images['keys'])
    draw_lives(screen, 0, 5, player.lives, player_mini_img)
    if message:
        draw_text(screen, "Привидения могут быть дружелюбными", 30, x_mes, y_mes, True)
    draw_text(screen, f"Уровень {level_num}", 30, WIDTH // 2, 10, True)
    draw_text(screen, str(score), 50, 700, 30, True)
    pygame.display.flip()

pygame.quit()
