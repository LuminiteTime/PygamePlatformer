from Source import *


class CoinBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.blockx = x
        self.blocky = y
        self.rect.center = (self.blockx, self.blocky)
        self.lifes = 1

    def activate(self):
        winsound.PlaySound(hit_enemy, winsound.SND_ASYNC | winsound.SND_ALIAS)
        global pow_
        pow_ = Pow(self.rect.centerx, self.rect.centery, 'lives')
        all_sprites.add(pow_)
        powerups.add(pow_)
