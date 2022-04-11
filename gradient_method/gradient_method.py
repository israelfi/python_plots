"""
Algoritmo do Gradiente
k ← 0
enquanto (não critério de parada)
gk ← gradiente(f(·), xk)
dk ← −gk
αk ← arg minα f(xk + αdk)
xk+1 ← xk + αkdk
k ← k + 1
fim-enquanto
"""

import numpy as np
import sympy as sym
import matplotlib.pyplot as plt


def define_func(n):
    """
    :param n: Vector with the variables
    :return: returns the function and the gradient of it at a given point (n[0], n[1])
    """

    # Initializeng the variables x1 and x2
    N1, N2 = np.meshgrid(n[0], n[1])

    # Defining f(x) = (x1 - 1)² + 2(x2)²
    f = (N1 - 1) ** 2 + 2 * N2 ** 2

    # Since f is differentiable, grad(f) = [2*x1 - 2; 4*x2]:
    f_diff = np.array([2 * n[0] - 2, 4 * n[1]])
    return f, f_diff


def plot_func(n, func):
    """
    :param n: Variables of the function (x1 and x2)
    :param func: Function values
    :return: Plots the contour of f(x)
    """
    N1, N2 = np.meshgrid(n[0], n[1])
    fig, ax = plt.subplots()
    CS = plt.contour(N1, N2, func, cmap=plt.get_cmap('rainbow'))
    ax.clabel(CS, inline=1, fontsize=10)

    plt.grid(color='white', linestyle='-', linewidth=0.7)  # Grid settings
    ax.set_facecolor((0.9, 0.9, 0.9))  # Backgroung color
    plt.style.use('ggplot')
    ax.set_xlabel('$x_1$')
    ax.set_ylabel('$x_2$')

    plt.draw()


def plot_f(f_values):
    fig, ax = plt.subplots()
    ax.plot(f_values, 'ro', label='f(X)')
    ax.set_ylabel('$f(X)$')
    ax.set_xlabel('Iterations')
    plt.legend()


def func_value():
    """
    :return: Returns the value of the function and its gradient in a point chosen by the user.
    """
    print('--------------------------------')
    values = input("Choose two values (separeted with space): ").split()
    values = [float(i) for i in values]
    f_value, f_grad = define_func(values)
    print(f'Function value at {values[0], values[1]}: {f_value[0][0]:.2f}\n'
          f'Gradient value at {values[0], values[1]}: {f_grad}')


def find_alfa(xk, grad_xk):
    """
    :param xk: Value of x in the current iteration
    :param grad_xk: Value of the gradient at xk
    :return: Value of alfa that minimizes f(alfa)
    """
    # Creating a symbolic variable alfa
    alfa = sym.Symbol('alfa')

    x_new = xk - alfa * grad_xk

    # Function f in terms of alfa
    f_alfa = (x_new[0] - 1) ** 2 + 2 * x_new[1] ** 2

    # Finding the value of alfa that minimizes f(alfa), i.e., df(alfa)/dalfa = 0
    f_alfa_dif = sym.diff(f_alfa)
    coefficients = sym.Poly(f_alfa_dif, alfa).coeffs()
    poly = np.poly1d(coefficients)

    # This will return the roots of the polynome
    return poly.r


def gradient_method():
    """
    :return: Returns the optimal value found, considering the stopping criteria (number of
    iteration and the gradient module)
    """
    k = 0
    grad_min = 1e6
    xk = np.array([10, 10])
    f_xk, grad_xk = define_func(xk)

    f_iter = [f_xk[0][0]]

    while k < n_iter and grad_min >= e:
        print(f'Iteration {k}: f(x) = {f_xk[0][0]}')

        alfa_min = find_alfa(xk, grad_xk)
        xk_new = xk - alfa_min * grad_xk
        f_xk, grad_xk = define_func(xk_new)

        # Gradient module
        grad_min = (grad_xk[0] ** 2 + grad_xk[1] ** 2) ** 0.5
        xk = xk_new
        f_iter.append(f_xk[0][0])
        k += 1

    print(f'Iteration {k}: f(x) = {f_xk[0][0]}')

    return xk, f_iter


if __name__ == '__main__':
    # Number of iterations
    n_iter = 100

    # Precision
    e = 0.01

    # -10 <= x1, x2 <= 10
    x1 = np.linspace(-10, 10, n_iter)
    x2 = np.linspace(-10, 10, n_iter)
    x = [x1, x2]

    F, _ = define_func(x)

    # Plot function
    plot_func(x, F)

    x_otm, f_hist = gradient_method()
    plt.plot(x_otm[0], x_otm[1], color='green', marker='o')
    plt.annotate(f'$x^*$ = ({x_otm[0]:.2f}, {x_otm[1]:.2f})', (x_otm[0] + 0.25, x_otm[1] + 0.25))

    plot_f(f_hist)

    # Return the value of the function and the gradient in a given point
    # func_value()

    plt.show()
