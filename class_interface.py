'''
Модуль, что отвечает за отрисовку пользовательского интерфейса.
В моделе MVC является объектом типа View.
'''

import pygame
import json
from class_game import Game

FPS = 20

#SVGA разрешение. Сделать круче не позволяют устройство и религия.
WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 600
CELL_SIZE = 20

def cls(screen):
    '''
    Очищает screen : pygame.surface.
    '''
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WINDOW_SIZE_X, WINDOW_SIZE_Y))

def get_img_by_name(name):
    '''
    Возвращает пригодную для pygame картинку с названием name : str.
    Картинка должна быть расположена в директории ./img и должна иметь
    расширение .png.
    '''
    return pygame.image.load('./img/' + name + '.png').convert_alpha()

DATA = dict()

def load_images(name):
    '''
    Создаёт словарь DATA и заполняет его массивом картинок .png из папки ./img/, сохраняя
    названия ('./img/image.png' будет доступно по ключу 'image').
    Все необходимые ключи надо указать в файле ./<name>.txt
    '''
    data = dict()
    fin = open('./' + name + '.json', 'r' )
    images = json.load(fin)
    for image in images:
        data[image] = get_img_by_name(image) 
    fin.close()
    return data

def draw_column(screen, start_cell, end_cell, shift, block_type):
    '''
    Отрисовывает столбик из блоков block_type : str так:
    ^
    |
    |
    |                            C <--------- end_cell : int
    |                            C
    |    shift : int        C
    |<------------------> C <--------- start_cell : int
    |_______________________>
    screen : pygame.surface.
    Всё расстояние измеряется в блоках. 
    '''
    max_y = WINDOW_SIZE_Y // CELL_SIZE
    start_cell = max_y - start_cell
    end_cell = max_y - end_cell
    end_cell, start_cell = start_cell, end_cell
    i = start_cell
    while i <= end_cell:
        screen.blit(DATA[block_type], (shift * CELL_SIZE, i * CELL_SIZE))
        i += 1

def draw_terrain(screen, line):
    '''
    Отрисовывает почву при условии, что line[x : int]: 
    (
        int -- y для текущего x;
        str -- название типа блока;
    ).
    '''
    x = 0
    for high, block in line:
        draw_column(screen, 0, high, x, block)
        x += 1

def draw_covering(screen, line, covering):
    x = 0
    for covering_level, block in covering:
        draw_column(screen, line[x][0], line[x][0] + covering_level - 1, x, block)
        x += 1

def draw_game(screen, game):
    '''
    Отрисовывает на экран состояние игры game : Game.
    '''
    cls(screen)
    highs = game.landscapes()
    covering = game.covering()
    draw_terrain(screen, highs)
    draw_covering(screen, highs, covering)

if __name__ == "__main__":
    game = Game({
        'size_x' : 200000,
    })

    print(game.map.bioms[:10])

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    DATA = load_images('img_list')
    DATA['btn font'] = pygame.font.SysFont('ubuntu', 20)  

    clock = pygame.time.Clock()
    timer = pygame.time.get_ticks()
    game_over = False

    while not game_over:
        draw_game(screen, game)
        pygame.display.flip()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            game.map.get_player()['position'] += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        clock.tick(FPS)
