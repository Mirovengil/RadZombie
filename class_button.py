'''
Модуль, реализующий работу кнопки при помощи модуля pygame.
'''

import pygame

class Btn:
    '''
    Класс кнопки в pygame. Авторский.
    '''

    colors = {
        'black' : (0, 0, 0),
        'red' : (255, 0, 0),
        'green' : (0, 255, 0),
        'blue' : (0, 0, 255),
        'yellow' : (255, 255, 0),
        'magenta' : (255, 0, 255),
        'cyan' : (0, 255, 255),
        'white' : (255, 255, 255)
    }

    colors_text = { #Использовать для выбора цвета текста.
        'white' : 'black',
        'black' : 'white',
        'red' : 'white',
        'blue' : 'white',
        'green' : 'black',
        'yellow' : 'black',
        'magenta' : 'white',
        'cyan' : 'black',
    }

    colors_next = { #Использовать для выделения кнопки.
        'white' : 'magenta',
        'black' : 'yellow',
        'red' : 'green',
        'blue' : 'magenta',
        'green' : 'cyan',
        'yellow' : 'red',
        'magenta' : 'red',
        'cyan' : 'blue',
    }

    def __init__(self, color, text='Кнопка, блеат!', pos=(0, 0)):
        if not color in Btn.colors:
            raise ValueError('Цвета ' + color + ' не существует!')
        self.main_color = color
        self.second_color = Btn.colors_next[color]
        self.text_color = Btn.colors_text[color]
        self.text = text
        self.pos = pos
        self.is_pressed = False
        self.is_hold = False
        self.can_be_pressed = True

    def draw(self, screen, font):
        '''
        Отрисовывает кнопку на screen : pygame.surface.
        '''
        if not self.is_hold:
            rez = font.render(self.text, True, Btn.colors[self.text_color])
            pygame.draw.rect(screen, Btn.colors[self.main_color], (self.pos[0] - 5, self.pos[1] - 5, rez.get_width() + 10, rez.get_height() + 10))
        else:
            rez = font.render(self.text, True, Btn.colors[Btn.colors_text[self.second_color]])
            pygame.draw.rect(screen, Btn.colors[self.second_color], (self.pos[0] - 5, self.pos[1] - 5, rez.get_width() + 10, rez.get_height() + 10))
        screen.blit(rez, self.pos)

    def check(self, font):
        '''
        Обновляет состояние кнопки в зависимости от event : pygame.event.
        '''
        mouse_position = pygame.mouse.get_pos()
        mouse_state = pygame.mouse.get_pressed()[0]
        # 0 -- правая кнопка мыши.
        # 1 -- левая кнопка мыши.
        # 2 -- колёсико мыши.
        rez = font.render(self.text, True, Btn.colors[self.text_color])
        min_x = self.pos[0]
        min_y = self.pos[1]
        max_y = min_y + rez.get_height()
        max_x = min_x + rez.get_width()
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        if min_x <= mouse_x <= max_x and min_y <= mouse_y <= max_y:
            self.is_hold = True
        else:
            self.is_hold = False
        if self.can_be_pressed and mouse_state and (min_x <= mouse_x <= max_x and min_y <= mouse_y <= max_y):
            self.pressed = True
            self.can_be_pressed = False
        else:
            self.pressed = False
        if not mouse_state:
            self.can_be_pressed = True
