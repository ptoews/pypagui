import matplotlib.pyplot as plt
import numpy as np

import pypagui


@pypagui.wrap_function
def plot_sin(amplitude: float = 1, phase_shift: float = 0):
    t = np.arange(0.0, 2 * np.pi, 0.01)
    plt.plot(t, amplitude * np.sin(t + phase_shift))
    plt.show()


if __name__ == '__main__':
    plot_sin(2)
