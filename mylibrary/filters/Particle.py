from math import pi

class Particle():
    def __init__(self, x, y, a, w):
        self.x = x
        self.y = y
        self.__a = a
        self.w = w

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, value):
        while self.__a < 0:
            self.__a += 2 * pi
        while self.__a > 2*pi:
            self.__a -= 2 * pi