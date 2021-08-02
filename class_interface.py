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

GLOBAL_SHIFT = 0

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
        screen.blit(DATA[block_type], ((shift + GLOBAL_SHIFT) * CELL_SIZE, i * CELL_SIZE))
        i += 1

def draw_terrain(screen, line):
    '''
    Отрисовывает почву при условии, что line[x : int]: 
    (
        int -- y для текущего x;
        str -- название типа блока в точке x;
    ).
    '''
    x = 0
    for high, block in line:
        draw_column(screen, 0, high, x, block)
        x += 1

def draw_covering(screen, line, covering):
    '''
    Отрисовывает все покрытия поверх почвы при условии, что 
    line[x : int]: 
        (
            int -- y для текущего x;
            str -- название типа блока в точке x;
        );
    covering[x : int]:
        (
            int -- высота покрытия в точке x;
            str -- название типа покрытия в точке x;
        );
    '''
    x = 0
    for covering_level, block in covering:
        draw_column(screen, line[x][0] + 1, line[x][0] + covering_level, x, block)
        x += 1

def draw_objects(screen, line, objects):
    '''
    Отрисовывает игровые объекты (пока только мобов) при условии, что:
        line[x : int]: 
            (
                int -- y для текущего x;
                str -- название типа блока в точке x;
            );
        objects[i : int]:
            (
                str -- тип объекта (игрок, зомби и т.п.) под индексом i;
                int -- местонахождение объекта под индексом i относительно поля зрения игрока;
            );
    '''
    for name, position in objects:
            draw_column(screen, line[position][0] + 2, line[position][0] + 2, position, name)

def draw_game(screen, game):
    '''
    Отрисовывает на экран состояние игры game : Game.
    '''
    cls(screen)
    highs = game.landscapes()
    covering = game.covering()
    objects = game.objects()
    draw_terrain(screen, highs)
    draw_covering(screen, highs, covering)
    draw_objects(screen, highs, objects)

if __name__ == "__main__":
    game = Game({
        'size_x' : 200000,
    })

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    DATA = load_images('img_list')
    DATA['btn font'] = pygame.font.SysFont('ubuntu', 20)  

    clock = pygame.time.Clock()
    timer = pygame.time.get_ticks()
    game_over = False

    while not game_over:
        GLOBAL_SHIFT = game.global_shift
        draw_game(screen, game)
        pygame.display.flip()
        game.manipulate(pygame.key.get_pressed())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        clock.tick(FPS)
