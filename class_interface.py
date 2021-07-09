'''
Модуль, что отвечает за отрисовку пользовательского интерфейса.
В моделе MVC является объектом типа View.
'''

import pygame
from class_game import Game

#SVGA разрешение. Сделать круче не позволяют устройство и религия.
WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 600

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
    DATA = dict()
    fin = open('./' + name + '.txt', 'r' )
    for image in fin:
        DATA[image.replace('/n', '')] = get_img_by_name(image.replace('/n', '')) 
    fin.close()

def draw_game(game):
    '''
    Отрисовывает на экран состояние игры game : Game.
    '''
    
    

if __name__ == "__main__":
    game = Game({
        'size_x' : 100,
    })
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    print(game.map.get_players_sight(5, 15))
    DATA = load_images('img_list')
    game_over = False
    while not game_over:
        draw_game(game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
