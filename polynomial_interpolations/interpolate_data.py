import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt


class InterpolateData:
    def __init__(self):
        self.ready = False

        self.x_points = []
        self.y_points = []

        self.fig = plt.figure(figsize=(8, 5), facecolor='#36454f')
        self.fig.canvas.mpl_connect("button_press_event", self.click)
        self.fig.canvas.mpl_connect('key_release_event', self.interp_ready)

        plt.title('Select at least 4 points (press Enter when finished)')
        self.config_plot()

    def click(self, event):
        self.x_points.append(event.xdata)
        self.y_points.append(event.ydata)

    def interp_ready(self, event):
        self.ready = True if event.key == 'enter' else False

    @staticmethod
    def config_plot():
        plt.xlabel('x [m]')
        plt.ylabel('y [m]')

        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['bottom'].set_color('white')
        plt.gca().spines['left'].set_color('white')
        plt.gca().xaxis.label.set_color('white')
        plt.gca().yaxis.label.set_color('white')
        plt.gca().title.set_color('white')
        plt.gca().set_facecolor('#36454f')
        plt.gca().tick_params(axis='x', colors='white')
        plt.gca().tick_params(axis='y', colors='white')

        plt.grid(visible=True, which='major', color='white', linestyle='-', alpha=0.2)
        plt.xlim([0, 10])
        plt.ylim([0, 10])

    def plot_result(self):
        plt.close()
        plt.figure(figsize=(8, 5), facecolor='#36454f')
        t = np.linspace(0, 10000, len(self.x_points))
        fx = interpolate.interp1d(t, self.x_points, kind='cubic')
        fy = interpolate.interp1d(t, self.y_points, kind='cubic')
        new_t = np.linspace(0, t.max(), t.shape[0] * 100)

        plt.title('Data Interpolation')

        self.config_plot()
        plt.plot(fx(new_t), fy(new_t), c='#8bfc81', linewidth=2, label='Interpolated Path')
        plt.scatter(self.x_points, self.y_points, marker='x', c='#f27777', label='Tracked Points')

        legend = plt.legend(frameon=False)
        plt.setp(legend.get_texts(), color='w')

        plt.show()

    def main(self):
        while not self.ready:
            plt.pause(0.1)
            plt.cla()
            plt.scatter(self.x_points, self.y_points, marker='x', c='#f27777')
            plt.title('Select at least 4 points (press Enter when finished)')
            self.config_plot()
            continue
        self.plot_result()


if __name__ == '__main__':
    my_script = InterpolateData()
    my_script.main()
