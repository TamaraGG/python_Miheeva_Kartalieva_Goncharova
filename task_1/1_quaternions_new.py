import math
import unittest

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

    def normalize(self):
        """Нормализация кватерниона (деление всех компонент на его норму)"""
        n = self.norm
        if n == 0:
            raise ZeroDivisionError("Cannot normalize a quaternion with zero norm.")
        self.w /= n
        self.x /= n
        self.y /= n
        self.z /= n

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


# Unit-тесты для проверки функциональности
class TestQuaternionWithExampleData(unittest.TestCase):
    def test_scalar_operations(self):
        q1 = Quaternion(3, -2, 5, 8)
        self.assertEqual(q1 * 2, Quaternion(6, -4, 10, 16))
        self.assertEqual(q1 / 2, Quaternion(1.5, -1, 2.5, 4))

    def test_scalar_addition_and_subtraction(self):
        q2 = Quaternion(0, 4, -1, 1)
        self.assertEqual(q2 - 4.6, Quaternion(-4.6, 4, -1, 1))
        self.assertEqual(q2 + 0.1, Quaternion(0.1, 4, -1, 1))

    def test_quaternion_addition_and_subtraction(self):
        q1 = Quaternion(3, -2, 5, 8)
        q2 = Quaternion(0, 4, -1, 1)
        self.assertEqual(q1 + q2, Quaternion(3, 2, 4, 9))
        self.assertEqual(q1 - q2, Quaternion(3, -6, 6, 7))

    def test_quaternion_multiplication(self):
        q1 = Quaternion(3, -2, 5, 8)
        q2 = Quaternion(0, 4, -1, 1)
        expected_mul = Quaternion(5, 25, 31, -15)
        self.assertEqual(q1 * q2, expected_mul)

    def test_unary_negation(self):
        q1 = Quaternion(3, -2, 5, 8)
        self.assertEqual(-q1, Quaternion(-3, 2, -5, -8))

    def test_conjugate_and_norm(self):
        q2 = Quaternion(0, 4, -1, 1)
        self.assertEqual(q2.conjugate, Quaternion(0, -4, 1, -1))
        self.assertAlmostEqual(q2.norm, math.sqrt(0**2 + 4**2 + (-1)**2 + 1**2))

    def test_inverse_property(self):
        q2 = Quaternion(0, 4, -1, 1)
        self.assertTrue(q2 * q2.inverse == Quaternion(1, 0, 0, 0))

    def test_pure_imaginary_and_complex_checks(self):
        q2 = Quaternion(0, 4, -1, 1)
        self.assertTrue(q2.is_pure_imaginary())

        q_complex = Quaternion(1, 1, 0, 0)
        self.assertTrue(q_complex.is_complex())

    def test_normalization(self):
        q = Quaternion(3, -2, 5, 8)
        norm = math.sqrt(3**2 + (-2)**2 + 5**2 + 8**2)  # sqrt(9 + 4 + 25 + 64) = sqrt(102)
        
        q.normalize()

        self.assertAlmostEqual(q.w, 3 / norm)
        self.assertAlmostEqual(q.x, -2 / norm)
        self.assertAlmostEqual(q.y, 5 / norm)
        self.assertAlmostEqual(q.z, 8 / norm)

    def test_zero_norm(self):
        q = Quaternion(0, 0, 0, 0)
        with self.assertRaises(ZeroDivisionError):
            q.normalize()


if __name__ == "__main__":
    unittest.main()
