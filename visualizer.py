
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')

class Visualizer:
    def __init__(self, initial_unit_variables: list[int], variable_history: list[tuple], out_path=None, debug_mode=False) -> None:
        self.init_vars = initial_unit_variables
        self.var_history = variable_history
        self.current_vars = set()

        self.fig, self.ax = plt.subplots()
        self.white_cmap = None
        self.setup_colormap()

        if debug_mode:
            self.setup_test_data()

        plt.minorticks_on()
        self.fig.tight_layout()
        self.setup_axes(self.ax)

        self.out_path = out_path
        self.anim = None

    def setup_colormap(self) -> None:
        binary = cm.get_cmap('binary', 256)
        newcolors = binary(np.linspace(0, 1, 256))
        white = np.array([1, 1, 1, 1])
        newcolors[:, :] = white
        self.white_cmap = ListedColormap(newcolors)

    def setup_test_data(self) -> None:
        input_matrix = np.matrix([[5,3,0,0,7,0,0,0,0],
                        [6,0,0,1,9,5,0,0,0],
                        [0,9,8,0,0,0,0,6,0],
                        [8,0,0,0,6,0,0,0,3],
                        [4,0,0,8,0,3,0,0,1],
                        [7,0,0,0,2,0,0,0,6],
                        [0,6,0,0,0,0,2,8,0],
                        [0,0,0,4,1,9,0,0,5],
                        [0,0,0,0,8,0,0,7,9]])

        for i,j in np.ndindex(input_matrix.shape):
            x = i + 1
            y = j + 1
            if input_matrix[i, j] == 0:
                var = int(f"{x}{y}{1}")
                self.var_history.append((var, True))
            else:
                var = int(f"{x}{y}{input_matrix[i, j]}")
                self.init_vars.append(var)

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

    def set_numbers(self, i: int) -> None:
        self.setup_axes(self.ax)

        for num in self.init_vars:
            num_str = str(num)
            x, y, z = tuple(map(lambda x: int(x), num_str))
            self.ax.text(x-1, y-1, z, ha="center", va="center", color="black", size=25)

        if i < len(self.var_history):
            var, is_added = self.var_history[i]
            if is_added:
                self.current_vars.add(var)
            elif not is_added:
                self.current_vars.remove(var)

        for num in self.current_vars:
            num_str = str(num)
            x, y, z = tuple(map(lambda x: int(x), num_str))
            self.ax.text(x-1, y-1, z, ha="center", va="center", color="red", size=25)

    def update(self, i: int) -> None:
        self.ax.clear()

        self.set_numbers(i)

        self.ax.imshow(np.zeros((9,9)), cmap=self.white_cmap)

    def run(self) -> None:
        self.anim = FuncAnimation(self.fig, self.update, frames=len(self.var_history), repeat=False)
        plt.show()

        if self.out_path is not None:
            self.save(self.out_path)

    def save(self, path='sudoku.gif') -> None:
        self.anim.save(path, writer='imagemagick')

if __name__ == '__main__':
    viz = Visualizer([], [], out_path=None, debug_mode=True)
    viz.run()