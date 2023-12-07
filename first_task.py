#Clawf

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Define electric constant
E_0 = 8.85e-12


def Capacity(s, d, E=1):
    return E * E_0 * s / d


def RoundCapacity(r, d, E=1):
    return E * E_0 * r * 2 * np.pi / d


def Draw(d, a):
    thick = 0.03

    # Define the parametric equations
    def x_equipotential_lines(P, Alpha):
        return (d / (2 * np.pi)) * (1 + 2 * np.log(P) - P ** 2 * np.cos(Alpha)) + a

    def y_equipotential_lines(P, Alpha):
        return (d / (2 * np.pi)) * (2 * Alpha - P ** 2 * np.sin(Alpha)) - d

    def x_lines_of_force(Alpha, P):
        return (d / (2 * np.pi)) * (1 + 2 * np.log(P) - P ** 2 * np.cos(Alpha)) + a

    def y_lines_of_force(Alpha, P):
        return (d / (2 * np.pi)) * (2 * Alpha - P ** 2 * np.sin(Alpha)) - d

    # Define the angle parameter range for equipotential lines
    A_values = np.arange(np.pi / 6, 2 * np.pi, np.pi / 6)
    # Plotting equipotential Lines
    for A in A_values:
        p_values = np.linspace(0.001, 3.5, 50)  # Define a range for p
        x = x_equipotential_lines(p_values, A)
        y = y_equipotential_lines(p_values, A)
        plt.plot(x, y, color='green', linewidth=1)
        plt.plot(-x, y, color='green', linewidth=1)
    # Internal equipotential lines
    x_1 = x_equipotential_lines(0.001, A_values)
    x_2 = -1 * x_equipotential_lines(0.001, A_values)
    y = y_equipotential_lines(0.001, A_values)
    for x1, x2, y in zip(x_1, x_2, y):
        plt.plot([x1, x2], [y, y], color='green', linewidth=1)

    # Define the P parameter range for force lines
    P_values = np.arange(0.5, 3.5, 0.5)
    # Plotting force lines
    for p in P_values:
        alpha_values = np.arange(np.pi / 128, 2 * np.pi, np.pi / 128)  # Define a range for p
        x = x_lines_of_force(alpha_values, p)
        y = y_lines_of_force(alpha_values, p)
        plt.plot(x, y, color='blue', linewidth=1)
        plt.plot(-x, y, color='blue', linewidth=1)
    # Internal force lines
    x_lines = np.arange(-a + 5, a - 4, 5)
    y1, y2 = d * (1 - thick), d * (thick - 1)
    for x in x_lines:
        plt.plot([x, x], [y1, y2], color='blue', linewidth=1)

    # Creating capacitor plates
    plate1 = patches.Rectangle((-a, d), 2 * a, d * thick, edgecolor='black', facecolor='yellow', alpha=1, linewidth=1)
    plate2 = patches.Rectangle((-a, -d), 2 * a, d * thick, edgecolor='black', facecolor='yellow', alpha=1, linewidth=1)
    # Adding plates
    current_ax = plt.gca()
    current_ax.add_patch(plate1)
    current_ax.add_patch(plate2)

    # Final Drawing
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Parametric Plot')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # length = int(input("Длина пластины a: "))
    # width = int(input("Ширина пластины b: "))
    # D = int(input("Расстояние между пластинами d: "))
    length = 40
    width = 60
    D = 5
    R = 20
    e = 100

    # print(Capacity(s, d, e))
    # print(RoundCapacity(r, d, e))
    Draw(D, length)
