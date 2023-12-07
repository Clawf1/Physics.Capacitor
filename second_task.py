#Clawf

import math
import numpy as np
from math import sin, cos
import matplotlib.pyplot as plt

E_0 = 8.85e-12


def Capacity(S, D, E=1):
    return E * E_0 * S / D


def CapacityWithDielectric(S, D, H, E1=1, Ed=5):
    C1 = E1 * E_0 * S / (D - H)
    C2 = Ed * E_0 * S / H
    return C1 * C2 / (C1 + C2)


class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        s = str(self.x) + " " + str(self.y)
        return s


# Поворот точки на угол Alpha
def RotatePoint(A, angle):
    x = A.x * cos(angle) + A.y * sin(angle)
    y = -A.x * sin(angle) + A.y * cos(angle)
    return Pair(x, y)


def IntersectionOfLines(A, B, C, D):
    if (A.x - B.x == 0) and (C.x - D.x == 0):
        print("Intersection of parallel lines???")
        exit(-1)
    if A.x - B.x == 0:
        k2 = (C.y - D.y) / (C.x - D.x)
        b2 = C.y - k2 * C.x
        x = A.x
        y = k2 * x + b2
        return Pair(x, y)
    if C.x - D.x == 0:
        k1 = (A.y - B.y) / (A.x - B.x)
        b1 = A.y - k1 * A.x
        x = C.x
        y = k1 * x + b1
        return Pair(x, y)
    k1 = (A.y - B.y) / (A.x - B.x)
    b1 = A.y - k1 * A.x
    k2 = (C.y - D.y) / (C.x - D.x)
    b2 = C.y - k2 * C.x
    x = (b2 - b1) / (k1 - k2)
    y = k1 * x + b1
    return Pair(x, y)


def ParallelogramArea(A, B, C):
    vec_a_x = B.x - A.x
    vec_a_y = B.y - A.y
    vec_b_x = C.x - A.x
    vec_b_y = C.y - A.y

    area = abs(vec_a_x * vec_b_y - vec_a_y * vec_b_x)
    return area


def TriangleArea(A, B, C):
    area = 1 / 2 * ((B.x - A.x) * (C.y - A.y) - (C.x - A.x) * (B.y - A.y))
    return area


def IntersectionArea(a, b, angle):
    if a < b:
        a, b = b, a

    angle %= np.pi
    if angle == 0:
        return a * b

    A = Pair(-a / 2, -b / 2)
    B = Pair(-a / 2, b / 2)
    C = Pair(a / 2, b / 2)
    D = Pair(a / 2, -b / 2)

    if angle > np.pi / 2:
        angle = np.pi - angle

    A2 = RotatePoint(A, angle)
    B2 = RotatePoint(B, angle)
    C2 = RotatePoint(C, angle)
    D2 = RotatePoint(D, angle)

    # Случай X
    if angle <= 2 * math.atan(b / a):
        X = IntersectionOfLines(A2, B2, A, B)
        Y = IntersectionOfLines(A2, D2, A, B)
        s = 2 * TriangleArea(A2, X, Y)

        X = IntersectionOfLines(A2, B2, B, C)
        Y = IntersectionOfLines(B2, C2, B, C)
        s += 2 * TriangleArea(B2, X, Y)

        return a * b - s

    X = IntersectionOfLines(A2, D2, A, D)
    Y = IntersectionOfLines(A2, D2, B, C)
    Z = IntersectionOfLines(B2, C2, A, D)

    return ParallelogramArea(X, Y, Z)  # Классический случай


# Полный подсчет емкости конденсатора с диэлектриком
def ComputeCapacity(L, W, D, H, Alpha):
    S = L * W
    Sd = IntersectionArea(L, W, Alpha)
    Sw = S - Sd
    Cap = Capacity(Sw, D)
    Cap += CapacityWithDielectric(Sd, D, H)
    return Cap


def Draw(AlphaValues, FunctionValues):
    plt.figure(figsize=(8, 6))
    plt.plot(AlphaValues, FunctionValues, label='my_function')  # Построение графика

    plt.xlabel('alpha, рад')
    plt.ylabel('Емкость, нФ')
    plt.title('f(alpha)')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # length = int(input("Длина пластины a: "))
    # width = int(input("Ширина пластины b: "))
    # d = int(input("Расстояние между пластинами d: "))
    # h = int(input("Толщина диэлектрика h: "))

    length = 40
    width = 20
    d = 5
    h = 2

    alpha_values = np.linspace(0, np.pi, 300)  # Генерация углов для f(a)

    # Вычисление значений функции для каждого угла
    function_values = [1e9 * ComputeCapacity(length, width, d, h, alpha) for alpha in alpha_values]

    # Отрисовка f(a)
    Draw(alpha_values, function_values)
