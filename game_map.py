'''
Модуль со всем необходимым для работы с игровой картой.
'''

from random import  randint
from class_object import get_object

def broke_line(start_point, end_point, line, arg):
    '''
    Функция для рекурсивной генерации карты высот. Де-факто, карта высот является
    шумом.
    Параметры:
        start_point : int -- начало прямой.
        end_point : int -- конец прямой.
        line : [int] -- массив, хранящий высоты для всех точек прямой.
    Чем больше MAX_BROKE, тем большие перепады высот могут встретиться на карте. 
    '''
    MAX_BROKE = 1
    if end_point - start_point == 1:
        return 0
    middle = (start_point + end_point) // 2
    middle_value = (line[start_point] + line[end_point]) // 2
    broke = randint(-MAX_BROKE, MAX_BROKE)
    if arg is None:
        broke *= (end_point - start_point)
    line[middle] = middle_value + broke
    broke_line(start_point, middle, line, arg)
    broke_line(middle, end_point, line, arg)

def generate_highs(size_x):
    '''
    Генерирует игровую карту высот и возвращает её в виде одномерного массива целых чисел.
    Все высоты больше нуля.
    Об алгоритме можно почитать в документации.
    DIFFERENCE_BETWEEN влияет на разницу между стартовой и конечной точками карты.
    В принципе, никто не запрещает выставлять вручную, чтобы было интереснее.
    START_HIGH задаёт стартовую высоту всей карты.
    MIN_LANDSCAPES задаёт минимальное количество искривлений на карте.
    MAX_LANDSCAPES задаёт максимальное количество искривлений на карте.
    '''
    DIFFERENCE_BETWEEN = randint(1, 200)
    START_HIGH = 100
    MIN_LANDSCAPES = size_x // 128
    MAX_LANDSCAPES = size_x // 64
    highs = []
    for i in range(size_x):
        highs.append(START_HIGH)
    broken_len = [9, 17, 33, 65]
    broke_line(0, size_x - 1, highs, 'no proportional')
    for i in range(randint(MIN_LANDSCAPES, MAX_LANDSCAPES)):
        start_point = randint(0, size_x - 1)
        end_point = start_point + broken_len[randint(0, len(broken_len) - 1)]
        if end_point < size_x:
            broke_line(start_point, end_point, highs, None)       
    shift = min(highs)
    if (shift < 0):
        shift = -shift
        x = 0
        while x < size_x:
            highs[x] += shift
            x += 1
    return highs

def generate_objects(size_x):
    '''
    Генерирует случайное количество объектов в пределах игровой карты длиной size_x : int.
    Среди объектов обязательно будет присутствовать игрок.
    '''
    objects = []
    player = get_object('player')
    objects.append(player)
    return objects

def make_water(line, level, covering):
    '''
    Заполняет те блоки, которые ниже уровня level : int, водой.
    '''
    x = 0
    for y in line:
        if y <= level:
            covering[x] = (level - y + 1, 'water_block')
        x += 1
class GameMap:
    '''
    Класс игровой карты.
    В модели MVC носит характер объекта Model.

    Хранение всех блоков на карте слишком затратно.
    Вместо этого выполняется хранение высоты карты в каждой точке, хранение всех объектов, 
    биомов и структур на карте. Имея эти данные, карту можно отрисовать не хуже
    обычного хранения, но место (и быстродействие определённых функций повысится!)
    будет экономиться очень неплохо.

    Поля:
        size_x : int -- длина игровой карты (в блоках).
        highs : [int] -- массив, где элемент под индексом x : int соответствует высоте карты в точке x.
        covering : [int] -- массив, где элемент под индексом x : int соответсвует высоте покрытия
        относительно highs[x] в точке x. 0 означает, что покрытия на данной координате нет.
        bioms : [{
            'start' : int -- координата начала биома.
            'end' : int -- координата окончания биома.
            'type' : string -- тип биома.
        }] -- массив биомов, которые хранятся в виде словарей (за неимением в python3 классов).
        objects : [Object] -- массив игровых объектов (за подробностями -- в документацию).
        player : int -- номер игрока в массиве self.objects (для быстрого доступа к нему). 
    '''
    def __init__(self, size_x):
        self.highs = generate_highs(size_x)
        middle_level = sum(self.highs) // len(self.highs)
        self.covering = dict()
        make_water(self.highs, middle_level, self.covering)
        self.objects = generate_objects(size_x)
        for index, value in enumerate(self.objects):
            if value['name'] == 'player':
                self.player = index
                break

    def get_player(self):
        '''
        Возвращает игрока, как объект.
        '''
        return self.objects[self.player]

    def get_len(self):
        '''
        Возвращает длину карты (по оси x, естественно) в клетках.
        '''
        return len(self.highs)

    def get_players_sight(self, sight_len, player_position_on_screen):
        '''
        Возвращает массив высот : [int], которые игрок может наблюдать на расстоянии sight_len : int
        справа и слева от себя.
        При этом, игрок помещается на высоту player_position_on_screen : int.
        '''
        player = self.get_player()
        start = max(0, player['position'] - sight_len)
        finish = min(player['position'] + sight_len, self.get_len() - 1)
        x = start
        sight = []
        while x <= finish:
            sight.append(self.highs[x] -  self.highs[player['position']] + player_position_on_screen)
            x += 1
        return sight

    def get_covering(self, length):
        '''
        Возвращает массив с разницей между уровнями покрытия и поверхности так, чтобы с
        обеих сторон от игрока находилось length : int блоков.
        '''
        player = self.get_player()
        start = max(0, player['position'] - length)
        finish = min(player['position'] + length, self.get_len() - 1)
        x = start
        covering = []
        while x <= finish:
            if x in self.covering:
                covering.append(self.covering[x])
            else:
                covering.append((0, 'none'))
            x += 1
        return covering

if __name__ == "__main__":
    temp = GameMap(200)
    print(temp.highs)
    print(temp.objects)
    print(temp.player)
