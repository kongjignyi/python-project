#假装这里有东西
import pygame
class Bg(pygame.sprite.Sprite):
    def __init__(self):
        super(Bg, self).__init__()
        bg_small = pygame.image.load('screanshot 2.png').convert_alpha()
        grass_land = bg_small.subsurface((0, 0, 1581, 840))
        self.surf = pygame.transform.scale(grass_land, (800, 600))
        self.rect = self.surf.get_rect(left=0, top=0)  # 左上角定位


class Pig(pygame.sprite.Sprite):
    def __init__(self):
        super(Pig, self).__init__()
        self.surf = pygame.image.load('dog_4_idle.png').convert_alpha()
        self.rect = self.surf.get_rect(center=(400, 300))  # 中心定位

    def update(self, keys):
        speed = 1  # 定义一个新的变量来控制速度
        if keys[pygame.K_LEFT]:
            self.rect.move_ip((-speed, 0))
        elif keys[pygame.K_RIGHT]:
            self.rect.move_ip((speed, 0))
        elif keys[pygame.K_UP]:
            self.rect.move_ip((0, -speed))
        elif keys[pygame.K_DOWN]:
            self.rect.move_ip((0, speed))

        # 防止小猪跑到屏幕外面
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600


class Goddess(pygame.sprite.Sprite):
    def __init__(self):
        super(Goddess, self).__init__()
        building = pygame.image.load('1.png').convert_alpha()
        self.surf = building.subsurface(((64*2 - 10, 0, 50, 100)))
        self.rect = self.surf.get_rect(center=(500, 430))  # 女神像的中心放到画布(500, 430)的位置


def main():
    pygame.init()
    pygame.display.set_caption('咕咕咕：顾子静做的游戏')  # 游戏标题
    win = pygame.display.set_mode((800, 600))  # 窗口尺寸

    bg = Bg()
    goddess = Goddess()
    pig = Pig()
    all_sprites = [bg, goddess, pig]  # 注意添加顺序，后添加的对象图层在先添加的对象的图层上面

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 点击左上角或者右上角的x关闭窗口时，停止程序
                running = False

        keys = pygame.key.get_pressed()
        pig.update(keys)
        for sprite in all_sprites:
            win.blit(sprite.surf, sprite.rect)
        pygame.display.flip()


if __name__ == '__main__':
    main()