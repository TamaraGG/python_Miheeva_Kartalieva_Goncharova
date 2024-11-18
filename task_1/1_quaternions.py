import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w  # Скалярная часть
        self.x = x  # Мнимая часть i
        self.y = y  # Мнимая часть j
        self.z = z  # Мнимая часть k

    def __repr__(self):
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        """Сложение кватернионов с кватернионом или вещественным числом"""
        if isinstance(other, Quaternion):
            return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, (int, float)):
            return Quaternion(self.w + other, self.x, self.y, self.z)
        else:
            return NotImplemented

    def __sub__(self, other):
        """Вычитание кватернионов с кватернионами или вещественными числами"""
        if isinstance(other, Quaternion):
            return Quaternion(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, (int, float)):
            return Quaternion(self.w - other, self.x, self.y, self.z)
        else:
            return NotImplemented

    def __mul__(self, other):
        """Умножение кватернионов на кветернионы или вещественные числа"""
        if isinstance(other, Quaternion):
            # Умножение кватерниона на другой кватернион
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z)
        elif isinstance(other, (int, float)):
            # Умножение кватерниона на вещественное число
            return Quaternion(self.w * other, self.x * other, self.y * other, self.z * other)
        else:
            return NotImplemented

    def __truediv__(self, other):
        """деление на вещественное число"""
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Division by zero is not allowed for quaternions.")
            # Деление кватерниона на вещественное число
            return Quaternion(self.w / other, self.x / other, self.y / other, self.z / other)
        else:
            return NotImplemented

    def __neg__(self):
        """унарный минус"""
        return Quaternion(-self.w, -self.x, -self.y, -self.z)

    def __pos__(self):
        """унарный плюс"""
        return Quaternion(self.w, self.x, self.y, self.z)

    @property
    def norm(self):
        """Норма кватерниона."""
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    @property
    def conjugate(self):
        """Сопряжение кватерниона."""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    @property
    def inverse(self):
        """Обратный кватернион."""
        norm_sq = self.norm ** 2
        return Quaternion(
            self.conjugate.w / norm_sq,
            self.conjugate.x / norm_sq,
            self.conjugate.y / norm_sq,
            self.conjugate.z / norm_sq
        )

    def rotate_vector(self, vector):
        """Поворот вектора с использованием кватернионов"""
        q_vector = Quaternion(0, vector[0], vector[1], vector[2])
        rotated_q = self * q_vector * self.inverse
        return (rotated_q.x, rotated_q.y, rotated_q.z)

    @staticmethod
    def from_axis_angle(axis, angle):
        """Создание кватерниона поворота на основе оси и угла"""
        half_angle = angle / 2
        norm =  math.sqrt(axis[0]**2 + axis[1]**2 + axis[2]**2)
        sin_half_angle = math.sin(half_angle)
        return Quaternion(
            math.cos(half_angle),
            axis[0] / norm * sin_half_angle,
            axis[1] / norm * sin_half_angle,
            axis[2] / norm * sin_half_angle
        )
    
    def __eq__(self, other):
        """Сравнение кватерниона с другим кватернионом или вещественным числом."""
        if isinstance(other, Quaternion):
            return (
                math.isclose(self.w, other.w) and
                math.isclose(self.x, other.x) and
                math.isclose(self.y, other.y) and
                math.isclose(self.z, other.z)
            )
        elif isinstance(other, (int, float)):
            # Сравнение с вещественным числом (сравнивается только скалярная часть w)
            return math.isclose(self.w, other) and math.isclose(self.x, 0) and math.isclose(self.y, 0) and math.isclose(self.z, 0)
        else:
            return False

    def is_real(self):
        """Проверка, является ли кватернион вещественным."""
        return math.isclose(self.x, 0) and math.isclose(self.y, 0) and math.isclose(self.z, 0)

    def is_pure_imaginary(self):
        """Проверка, является ли кватернион чисто мнимым."""
        return math.isclose(self.w, 0) and (not math.isclose(self.x, 0) or not math.isclose(self.y, 0) or not math.isclose(self.z, 0))

    def is_complex(self):
        """Проверка, является ли кватернион комплексным (имеет ненулевую скалярную и мнимую части)."""
        return not math.isclose(self.w, 0) and (not math.isclose(self.x, 0) or not math.isclose(self.y, 0) or not math.isclose(self.z, 0))

    def __str__(self):
        """Преобразование кватерниона в строку для удобного вывода"""
        return f"({'- ' if self.w < 0 else ''}{abs(self.w)} {'+' if self.x >= 0 else '-'} {abs(self.x)}i {'+' if self.y >= 0 else '-'} {abs(self.y)}j {'+' if self.z >= 0 else '-'} {abs(self.z)}k)"


def visualize_quaterion_rotation(initial_vector, rotation_axis, theta_degrees):
        theta = math.radians(theta_degrees)     #угол поворота в радианах
        q_rotation = Quaternion.from_axis_angle(rotation_axis, theta)   # кватерион поворота

        # цвета векторов
        colors = {'initial' : 'lime',
                  'rotated' : 'orange',
                  'axis' : 'darkslategray'}

        # поворачиваем вектор
        rotated_vector = q_rotation.rotate_vector(initial_vector)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Построение начального вектора
        ax.quiver(0, 0, 0, initial_vector[0], initial_vector[1], initial_vector[2], 
            color=colors['initial'], label='Initial Vector')

        # Построение повернутого вектора
        ax.quiver(0, 0, 0, rotated_vector[0], rotated_vector[1], rotated_vector[2], color=colors['rotated'], label='Rotated Vector')

        vect_len = math.sqrt(initial_vector[0] ** 2 + initial_vector[1] ** 2 + initial_vector[2] ** 2)
        max_len = vect_len * 1.5 + 1

        # Построение координатных осей
        ax.quiver(0, 0, 0, max_len, 0, 0, color='dimgray', linestyle='--', label='X Axis')
        ax.quiver(0, 0, 0, 0, max_len, 0, color='dimgray', linestyle='--', label='Y Axis')
        ax.quiver(0, 0, 0, 0, 0, max_len, color='dimgray', linestyle='--', label='Z Axis')

        # Построение оси поворота
        rotation_axis_length = max_len  # Длина оси поворота для визуализации
        ax.quiver(0, 0, 0, 
                rotation_axis[0] * rotation_axis_length, 
                rotation_axis[1] * rotation_axis_length, 
                rotation_axis[2] * rotation_axis_length, 
                color=colors['axis'], label='Rotation Axis')

        # Настройка графика
        ax.set_xlim([-max_len, max_len])
        ax.set_ylim([-max_len, max_len])
        ax.set_zlim([-max_len, max_len])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.show()



if __name__ == "__main__":
    # пример поворота с помощью кватерниона
    # visualize_quaterion_rotation([4, 6, 1], [1,0,0], 90)

    # пример операций над кватернионами
    q1 = Quaternion(3, -2, 5, 8)
    q2 = Quaternion(0, 4, -1, 1)

    print()
    print()
    print(f"{'q1':<15}     {q1}")
    print(f"{'q2':<15}     {q2}")
    print()
    print(f"{'q1 * 2':<15}     {q1 * 2}")
    print(f"{'q1 / 2':<15}     {q1 / 2}")
    print(f"{'q2 - 4.6':<15}     {q2 - 4.6}")
    print(f"{'q2 + 0.1':<15}     {q2 + 0.1}")
    print()
    print(f"{'q1 + q2':<15}     {q1 + q2}")
    print(f"{'q1 - q2':<15}     {q1 - q2}")
    print(f"{'q1 * q2':<15}     {q1 * q2}")
    print()
    print(f"{'-q1':<15}     {-q1}")
    print(f"{'сопряженное q2':<15}     {q2.conjugate}")
    print(f"{'норма q2':<15}     {q2.norm}")
    print()
    print(f"q2 * q2^-1 == 1 (проверка свойства кватернионов) : {q2 * q2.inverse == 1}")
    print(f"является ли q2 чисто мнимым : {q2.is_pure_imaginary()}")
    print(f"явялется ли (1+i) комплексным : {Quaternion(1,1,0,0).is_complex()}")
    print()
