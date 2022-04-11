import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def poly(x, a, b, c, d, e, f, g):
    return (a * x) + (b * x ** 2) + (c * x ** 3) + (d * x ** 4) + (e * x ** 5) + (f * x ** 6) + g


def plot_curves(df1, df2):
    plt.plot(df1['Wind'], df1['CP'], '-o', df2['Wind'], df2['CP'], '-o')
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

    plt.legend(['E-101 (3050kW)', 'E-101 (3500kW)'])

    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('CP')
    plt.show()


if __name__ == '__main__':
    file_1 = 'e-101_3050.txt'
    file_2 = 'e-101_3500.txt'
    df1 = pd.read_csv(file_1, delimiter='\t')
    df2 = pd.read_csv(file_2, delimiter='\t')

    popt, _ = curve_fit(poly, df1['Wind'], df1['CP'])
    a, b, c, d, e, f, g = popt
    print(a, b, c, d, e, f, g)

    x = np.arange(1, 25, 0.01)
    y = np.array([poly(i, a, b, c, d, e, f, g) for i in x])

    plt.figure(figsize=(10, 8))
    plt.subplot(211)
    plt.plot(x, y)
    plt.plot(df1['Wind'], df1['CP'], 'o')
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.legend(['6 Degree Polynomial', 'Data'])
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('CP')

    plt.subplot(212)
    plt.plot(df1['Wind'], df1['CP'], '-o', df2['Wind'], df2['CP'], '-o')
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

    plt.legend(['E-101 (3050kW)', 'E-101 (3500kW)'])

    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('CP')
    plt.show()
