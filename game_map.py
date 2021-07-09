'''
Модуль со всем необходимым для работы с игровой картой.
'''

from random import  randint

def broke_line(start_point, end_point, line):
    '''
    Функция для рекурсивной генерации карты высот. Де-факто, карта высот является
    шумом.
    Параметры:
        start_point : int -- начало прямой.
        end_point : int -- конец прямой.
        line : [int] -- массив, хранящий высоты для всех точек прямой.
    Чем больше MAX_BROKE, тем большие перепады высот могут встретиться на карте. 
    '''
    MAX_BROKE = 3
    if end_point - start_point == 1:
        return 0
    middle = (start_point + end_point) // 2
    middle_value = (line[start_point] + line[end_point]) // 2
    broke = (end_point - start_point) * randint(-MAX_BROKE, MAX_BROKE)
    line[middle] = middle_value + broke
    broke_line(start_point, middle, line)
    broke_line(middle, end_point, line)

def generate_highs(size_x):
    '''
    Генерирует игровую карту высот и возвращает её в виде одномерного массива целых чисел.
    Все высоты больше нуля.
    Об алгоритме можно почитать в документации.
    DIFFERENCE_BETWEEN влияет на разницу между стартовой и конечной точками карты.
    В принципе, никто не запрещает выставлять вручную, чтобы было интереснее.
    '''
    DIFFERENCE_BETWEEN = randint(1, 200)
    highs = []
    for i in range(size_x):
        highs.append(0)
    highs[0] = 0
    highs[size_x - 1] = DIFFERENCE_BETWEEN
    broke_line(0, size_x - 1, highs)       
    shift = min(highs)
    if (shift < 0):
        shift = -shift
        x = 0
        while x < size_x:
            highs[x] += shift
            x += 1
    return highs

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
        objects : [Object] -- массив игровых объектов (за подробностями -- в документацию).
        player : int -- номер игрока в массиве self.objects (для быстрого доступа к нему). 
    '''
    def __init__(self, size_x):
        self.highs = generate_highs(size_x)

if __name__ == "__main__":
    temp = GameMap(200)
    print(temp.highs)