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

    DIFFERENCE_BETWEEN влияет на разницу между стартовой и конечной точками карты.
    В принципе, никто не запрещает выставлять вручную, чтобы было интереснее.
    '''
    def __init__(self, size_x):
        DIFFERENCE_BETWEEN = randint(1, 200)
        self.size_x = size_x
        self.highs = []
        for i in range(self.size_x):
            self.highs.append(0)
        #Генерируется карта высот. Подробнее можно прочитать в документации.
        self.highs[0] = 0
        self.highs[self.size_x - 1] = DIFFERENCE_BETWEEN
        broke_line(0, size_x - 1, self.highs)       
        shift = min(self.highs)
        if (shift < 0):
            shift = -shift
            x = 0
            while x < self.size_x:
                self.highs[x] += shift
                x += 1

if __name__ == "__main__":
    temp = GameMap(200)
    print(temp.highs)
