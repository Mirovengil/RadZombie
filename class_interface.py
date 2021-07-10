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

def get_img_by_name(name):
    '''
    Возвращает пригодную для pygame картинку с названием name : str.
    Картинка должна быть расположена в директории ./img и должна иметь
    расширение .png.
    '''
    print(name)
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

def draw_game(screen, game):
    '''
    Отрисовывает на экран состояние игры game : Game.
    '''
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WINDOW_SIZE_X, WINDOW_SIZE_Y))
    highs = game.landscapes()
    cnt = 0
    for high, block in highs:
        if high <= 0:
            continue
        block_pos = WINDOW_SIZE_Y
        for i in range(high):
            screen.blit(DATA[block], (cnt * CELL_SIZE, block_pos - CELL_SIZE))
            block_pos -= CELL_SIZE
        cnt += 1
    

if __name__ == "__main__":
    game = Game({
        'size_x' : 200000,
    })

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    DATA = load_images('img_list')
    DATA['btn font'] = pygame.font.SysFont('ubuntu', 20)
    clock = pygame.time.Clock()

    print(game.map.get_players_sight(19, 15))
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
