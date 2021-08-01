'''
Модуль для работы с внутриигровыми объектами.
К оным относятся игрок и мобы.
'''

import json

def get_object(name):
    '''
    Возвращает игровой объект типа name : string в виде словаря:
        'name' : string -- название игрового объекта.
        'max hp' : int -- максимальный запас здоровья.
        'hp' : int -- текущий запас здоровья.
        'position' : int -- позиция объекта на игровой карте (по оси x).
    '''
    fin = open('./data/' + name + ".json")
    obj = json.load(fin)
    obj['position'] = 20 #ИСПРАВИТЬ!!
    obj['hp'] = obj['max hp']
    obj['name'] = name
    fin.close()
    return obj

