import sys
import pygame
import os # 导入 os 模块来处理文件路径

# --- 常量定义 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SPEED = 3

# 图片和字体路径（假设图片在 'assets' 文件夹中）
ASSETS_DIR = 'assets'
BG_IMAGE_PATH = os.path.join(ASSETS_DIR, 'screanshot 2.png')

# 动画帧的目录和前缀（现在是 8 帧）
ANIMATION_DIR = 'out' # 假设分割后的帧保存在 'out' 文件夹
ANIMATION_PREFIX = 'dog_4_walk_sheet_' # <--- 已更新为正确的动画文件名前缀

# 字体路径现在指向 assets 文件夹
CUSTOM_FONT_PATH = os.path.join(ASSETS_DIR, '默陌专辑手写体.ttf')


# --- 游戏精灵 ---
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        try:
            bg_small = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
            grass_land = bg_small.subsurface((0, 0, 1581, 840))
            self.image = pygame.transform.scale(grass_land, (SCREEN_WIDTH, SCREEN_HEIGHT)) # <--- 这里使用 self.image
        except pygame.error as e:
            print(f"错误：加载背景图片失败 ({BG_IMAGE_PATH})：{e}。将使用纯色背景替代。")
            self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) # <--- 这里使用 self.image
        self.rect = self.image.get_rect(left=0, top=0) # <--- 这里使用 self.image


class Dog(pygame.sprite.Sprite):
    def __init__(self):
        super(Dog, self).__init__()
        self.frames = [] # 用于存储所有动画帧
        self.current_frame = 0 # 当前显示的帧的索引
        self.animation_speed = 0.1 # 动画播放速度，值越小，切换越快 (每帧0.1秒，即10帧/秒)
        self.last_update = pygame.time.get_ticks() # 上次更新帧的时间

        # 加载所有 8 帧动画
        for i in range(1, 9): # 循环范围是 1 到 8 (共 8 帧)
            frame_path = os.path.join(ANIMATION_DIR, f"{ANIMATION_PREFIX}{i}.png")
            try:
                frame_image = pygame.image.load(frame_path).convert_alpha()
                # 原始帧是 384x47，如果 Dog 精灵太小，可能需要缩放。
                # 假设每帧就是 48x47 （384 / 8）像素，
                # 如果小狗看起来太小，可以在这里缩放：
                # frame_image = pygame.transform.scale(frame_image, (desired_width, desired_height))
                self.frames.append(frame_image)
            except pygame.error as e:
                print(f"错误：加载动画帧失败 ({frame_path})：{e}。动画将使用红色方块。")
                self.frames = [pygame.Surface((48, 47))] # 备用：只有一帧红色方块，大小与单帧一致
                self.frames[0].fill((255, 0, 0))
                break # 加载失败则停止加载，使用备用帧

        self.image = self.frames[self.current_frame] # 初始化当前显示的图片
        # 确保 rect 的大小和当前帧匹配，初始位置在屏幕中心
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))


    def update(self, keys):
        # 移动小狗
        if keys[pygame.K_LEFT]:
            self.rect.move_ip((-PLAYER_SPEED, 0))
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip((PLAYER_SPEED, 0))
        if keys[pygame.K_UP]:
            self.rect.move_ip((0, -PLAYER_SPEED))
        if keys[pygame.K_DOWN]:
            self.rect.move_ip((0, PLAYER_SPEED))

        # 防止小狗跑到屏幕外面
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # 动画播放逻辑
        now = pygame.time.get_ticks() # 获取当前时间
        if now - self.last_update > self.animation_speed * 1000: # 1000 毫秒 = 1 秒
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames) # 切换到下一帧，循环播放
            self.image = self.frames[self.current_frame] # 更新小狗的图片为当前帧


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False

    def draw(self, surface, font):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=10)

        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            self.is_hovered = True
        else:
            self.current_color = self.color
            self.is_hovered = False

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False


def show_start_screen(screen):
    bg_image = None

    title_font = None
    button_font = None
    try:
        title_font = pygame.font.Font(CUSTOM_FONT_PATH, 72)
        button_font = pygame.font.Font(CUSTOM_FONT_PATH, 36)
    except FileNotFoundError:
        print(f"警告：自定义字体未找到 ({CUSTOM_FONT_PATH})。将使用默认字体。")
        title_font = pygame.font.Font(None, 72)
        button_font = pygame.font.Font(None, 36)
    except Exception as e:
        print(f"警告：加载自定义字体时发生意外错误：{e}。将使用默认字体。")
        title_font = pygame.font.Font(None, 72)
        button_font = pygame.font.Font(None, 36)

    start_button = Button(300, 300, 200, 60, "开始游戏", (107, 195, 255), (150, 210, 255))
    quit_button = Button(300, 400, 200, 60, "退出游戏", (255, 107, 107), (255, 150, 150))

    title_text = title_font.render("咕咕咕：顾子静的游戏", True, (50, 50, 50))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))

    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.is_clicked(event):
                return True

            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        start_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)

        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            for y in range(SCREEN_HEIGHT):
                color_val = int(180 + (y / SCREEN_HEIGHT) * 75)
                pygame.draw.line(screen, (color_val, color_val, 255), (0, y), (SCREEN_WIDTH, y))

        screen.blit(title_text, title_rect)
        start_button.draw(screen, button_font)
        quit_button.draw(screen, button_font)

        version_text = pygame.font.Font(None, 20).render("版本 v1.0", True, (100, 100, 100))
        screen.blit(version_text, (10, SCREEN_HEIGHT - 20))

        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    pygame.display.set_caption('咕咕咕：顾子静做的游戏')
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    if not show_start_screen(win):
        pygame.quit()
        return

    game_font = None
    try:
        game_font = pygame.font.Font(CUSTOM_FONT_PATH, 50)
    except FileNotFoundError:
        print(f"警告：自定义字体未找到 ({CUSTOM_FONT_PATH})。将使用默认字体。")
        game_font = pygame.font.Font(None, 50)
    except Exception as e:
        print(f"警告：加载自定义字体时发生意外错误：{e}。将使用默认字体。")
        game_font = pygame.font.Font(None, 50)

    text = game_font.render("就这样吧，还能咋地", True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, 200)

    bg = Background()
    dog = Dog()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(bg)
    all_sprites.add(dog)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if show_start_screen(win):
                        continue
                    else:
                        running = False

        keys = pygame.key.get_pressed()
        dog.update(keys)

        all_sprites.draw(win)

        win.blit(text, textRect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()