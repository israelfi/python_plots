from scipy.interpolate import interp1d
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np


def interpolate_time():
    original_data_x = [1000, 2500, 5000, 10000]
    original_data_y = [24, 19, 16, 14]

    f = interp1d(original_data_x, original_data_y)
    f2 = interp1d(original_data_x, original_data_y, kind='cubic')
    f3 = interp1d(original_data_x, original_data_y, kind='zero')
    f4 = interp1d(original_data_x, original_data_y, kind='quadratic')

    x_new = np.linspace(min(original_data_x), max(original_data_x), num=10 * len(original_data_x), endpoint=True)

    plt.figure(figsize=(10, 6))
    plt.plot(original_data_x, original_data_y, 'o', x_new, f(x_new), '-', x_new, f2(x_new), '--', x_new, f3(x_new), ':',
             x_new, f4(x_new), '-.')
    plt.legend(['data', 'linear', 'cubic', 'zero', 'quadratic', 'splev'], loc='best', title='Interpolation')

    plt.grid(True)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

    plt.xlabel('Y data')
    plt.ylabel('X data')
    plt.show()


if __name__ == '__main__':
    interpolate_time()
