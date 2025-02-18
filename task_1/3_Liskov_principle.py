# -*- coding: utf-8 -*-
"""принципЛисков.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w4nSz6aXt5Puif3AChruOhqci_Xareis

Single responsibility principle — принцип подстановки Барбары Лисков: если для любого объекта o1 типа S существует такой объект o2 типа Т, что для всех программ Р, определенных в терминах Т, поведение Р не изменяется при подстановке o1 вместо o2, то S —
подтип Т.

Функции, которые используют базовый тип, должны иметь возможность использовать подтипы базового типа, не зная об этом.

Пример. В чем проблема с наследованием квадратов от прямоугольника?
"""

class Rectangle(Shape):
  ...
  def __init__(self, width, height, x=0, y=0):
    super().__init__(x, y)
    self.width = width
    self.height = height

class Square(Rectangle):
  ...
  def __init__(self, side, x=0, y=0):
    super().__init__(side, side, x, y)

"""Код, использующий атрибуты width и height класса Rectangle независимым образом, может работать некорректно для экземпляров класса Square, нарушая ограничение на равенство сторон

Можно ли все-таки исправить класс Square?
Да, например, с помощью свойств

property() - встроенная в Pyrhon функция, позволяющая превратить атрибут класса в свойство:

property(fget=None, fset=None, fdel=None, doc=None)

"""

class Shape:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Rectangle(Shape):
    def __init__(self, width, height, x=0, y=0):
        super().__init__(x, y)
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

class Square(Rectangle):
    def __init__(self, side, x=0, y=0):
        super().__init__(side, side, x, y)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = self._height = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._width = self._height = value

shape = Shape(x=10, y=15)
print(f"Shape: x={shape.x}, y={shape.y}")

rectangle = Rectangle(width=20, height=10, x=5, y=5)
print(f"Rectangle: x={rectangle.x}, y={rectangle.y}, width={rectangle.width}, height={rectangle.height}")

square = Square(side=30, x=2, y=3)
print(f"Square: x={square.x}, y={square.y}, width={square.width}, height={square.height}")

# изменим ширину квадрата и проверим, что высота также изменилась
square.width = 40
print(f"После изменения ширины, Square: width={square.width}, height={square.height}")

# изменим высоту квадрата и проверим, что ширина также изменилась
square.height = 50
print(f"После изменения высоты, Square: width={square.width}, height={square.height}")