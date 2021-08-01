'''
Модуль с классом игры, при помощи которого реализовано удобное управление событиями
в оной.
Класс является объектом типа Controller в патттерне MVC.  
'''

SIGHT_LEN = 19

from game_map import GameMap, get_from_BIOMS

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
        Возвращает массив высот для отрисовки, учитывая типы их биомов.
        '''
        highs = self.map.get_players_sight(SIGHT_LEN, 15)
        places = []
        x = self.get_player_sight_start(SIGHT_LEN)
        for high in highs:
            places.append((high, self.block_type(x)))
            x += 1
        return places

    def covering(self):
        '''
        Возвращает разность между уровнями покрытия и поверхности.
        Биомы учитываются 
        '''
        return self.map.get_covering(SIGHT_LEN)

    def objects(self):
        '''
        Возвращает все объекты в пределах видимости игрока, которые надо отрисовать.
        В следующем формате:
        [
        (
            str -- тип объекта (игрок, зомби и т.п.);
            int -- местонахождение объекта относительно поля зрения игрока;
        )
        ]
        '''
        obj = []
        for object_ in self.map.objects:
            obj.append(
                (
                    object_['name'],
                    object_["position"] - self.get_player_sight_start(SIGHT_LEN),
                )
            )
        return obj

    def get_player_sight_start(self, length):
        '''
        Возвращает координату на оси x, которая является началом поля видимости игрока,
        которое имеет длину length : int.
        '''
        player = self.map.get_player()
        start_sight = max(0, player['position'] - length)
        return start_sight

    def block_type(self, x):
        '''
        Возвращает тип блока, который находится в координате x : int.
        '''
        return get_from_BIOMS(self.map.get_bioms_type(x), 'block')

    def liquid_type(self, x):
        '''
        Возвращает тип жидкости, которая находится в координате x : int.
        '''
        return get_from_BIOMS(self.map.get_bioms_type(x), 'liquid')
