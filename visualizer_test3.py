
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')

class Visualizer:
    def __init__(self, debug_mode=True) -> None:
        self.input_matrix = np.zeros((9,9))
        self.solved_matrix = np.zeros((9,9))
        self.fig, self.ax = plt.subplots()
        self.white_cmap = None
        self.setup_colormap()

        if debug_mode:
            self.setup_test_data()
        plt.minorticks_on()
        self.fig.tight_layout()
        self.setup_axes(self.ax)

        self.anim = None

    def setup_colormap(self) -> None:
        binary = cm.get_cmap('binary', 256)
        newcolors = binary(np.linspace(0, 1, 256))
        white = np.array([1, 1, 1, 1])
        newcolors[:, :] = white
        self.white_cmap = ListedColormap(newcolors)

    def setup_test_data(self) -> None:
        self.input_matrix = np.matrix([[5,3,0,0,7,0,0,0,0],
                        [6,0,0,1,9,5,0,0,0],
                        [0,9,8,0,0,0,0,6,0],
                        [8,0,0,0,6,0,0,0,3],
                        [4,0,0,8,0,3,0,0,1],
                        [7,0,0,0,2,0,0,0,6],
                        [0,6,0,0,0,0,2,8,0],
                        [0,0,0,4,1,9,0,0,5],
                        [0,0,0,0,8,0,0,7,9]])

        self.solved_matrix = np.zeros(self.input_matrix.shape)
        for i, j in np.ndindex(self.solved_matrix.shape):
            if not self.input_matrix[i, j] == 0:
                self.solved_matrix[i, j] = -1

    def setup_axes(self, ax: plt.Axes) -> None:
        # Minor ticks
        self.ax.set_xticks(np.arange(-.5, 9, 1), minor=True)
        self.ax.set_yticks(np.arange(-.5, 9, 1), minor=True)

        # Major ticks
        self.ax.set_xticks(np.arange(-.5, 9, 3))
        self.ax.set_yticks(np.arange(-.5, 9, 3))

        # Gridlines based on minor ticks
        self.ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
        self.ax.grid(which='major', color='black', linestyle='-', linewidth=5)

        self.ax.get_xaxis().set_ticklabels([])
        self.ax.get_yaxis().set_ticklabels([])

    def set_numbers(self, ax : plt.Axes, input_matrix: np.matrix, solved_matrix: np.matrix) -> None:
        self.setup_axes(self.ax)

        for i, j in np.ndindex(input_matrix.shape):
            if input_matrix[i, j] > 0:
                self.ax.text(j, i, input_matrix[i, j], ha="center", va="center", color="black", size=25)

        for i, j in np.ndindex(solved_matrix.shape):
            if solved_matrix[i, j] > 0:
                self.ax.text(j, i, int(solved_matrix[i, j]), ha="center", va="center", color="red", size=25)

    def update(self, i: int) -> None:
        row, col = np.where(self.solved_matrix == 0)
        if len(row) > 0 and len(col) > 0:
            self.solved_matrix[row[0], col[0]] = np.random.randint(1, 10)
        self.ax.clear()
        self.set_numbers(self.ax, self.input_matrix, self.solved_matrix)
        self.ax.imshow(self.input_matrix, cmap=self.white_cmap)

    def run(self) -> None:
        self.anim = FuncAnimation(self.fig, self.update, frames=1000, repeat=False)
        plt.show()

    def save(self, path='sudoku.gif') -> None:
        self.anim.save(path, writer='imagemagick')

if __name__ == '__main__':
    viz = Visualizer(debug_mode=True)
    viz.run()