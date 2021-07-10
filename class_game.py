'''
Модуль с классом игры, при помощи которого реализовано удобное управление событиями
в оной.
Класс является объектом типа Controller в патттерне MVC.  
'''

from game_map import GameMap

class Game:
    '''
    Собсна, про этот класс всё уже сказано в описании модуля.
    '''
    def __init__(self, options):
        '''
        options : dict -- словарь с настройками создаваемой игры.
        Имеет следующие поля:
            size_x : int -- длина игровой карты (в блоках).
        '''
        self.map = GameMap(options['size_x'])

    def landscapes(self):
        '''
        Возвращает массив высот, которые надо отрисовать, с учётом типов их биомов (пока не
        реализованы!).
        '''
        highs = self.map.get_players_sight(19, 15)
        places = []
        cnt = 0
        for high in highs:
            cnt += 1
            if cnt != len(highs) // 2 + 1:
                places.append((high, 'dirt_block'))
            else:
                places.append((high, 'marker'))
        return places
        
