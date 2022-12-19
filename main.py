import os
import sys
import pygame

pygame.init()
pygame.display.set_caption('Перемещение героя')
pygame.key.set_repeat(200, 70)
FPS = 50
WIDTH = 400
HEIGHT = 300
STEP = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА",
                  "",
                  "Правила игры",
                  "Если в правилах несколько строк",
                  "приходится выводить их построчно"]
    fon = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 60
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color("green"))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord  # координаты у
        intro_rect.x = 10
        screen.blit(string_rendered, intro_rect)
        text_coord += intro_rect.height + 10
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return [line.ljust(max_width, '.') for line in level_map]


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(pos_x * tile_width + 16, pos_y * tile_height + 5)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
    return new_player, x, y


player, level_x, level_y = generate_level(load_level("level1.txt"))
camera = Camera()


while True:
    WIDTH, HEIGHT = pygame.display.get_window_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.rect.x -= STEP
            if event.key == pygame.K_RIGHT:
                player.rect.x += STEP
            if event.key == pygame.K_UP:
                player.rect.y -= STEP
            if event.key == pygame.K_DOWN:
                player.rect.y += STEP
    screen.fill(pygame.Color(0, 0, 0))
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
