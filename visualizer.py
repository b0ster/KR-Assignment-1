
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import Colormap, ListedColormap
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.animation as animation
plt.style.use('seaborn-pastel')

class Visualizer:
    def __init__(self, initial_unit_variables: list[int], variable_history: list[tuple], out_path=None) -> None:
        self.init_vars = dict()
        for num in initial_unit_variables:
            x, y, z = tuple(map(lambda x: int(x), str(num)))
            self.init_vars[(x, y)] = z
            
        self.var_history = [(int(str(num)[0]), int(str(num)[1]), int(str(num)[2]), b) for num, b in variable_history]

        self.current_vars = dict()

        self.fig, self.ax = plt.subplots()
        self.white_cmap = None
        self.setup_colormap()

        # if debug_mode:
        #     self.setup_test_data()

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

    # def setup_test_data(self) -> None:
    #     input_matrix = np.matrix([[5,3,0,0,7,0,0,0,0],
    #                     [6,0,0,1,9,5,0,0,0],
    #                     [0,9,8,0,0,0,0,6,0],
    #                     [8,0,0,0,6,0,0,0,3],
    #                     [4,0,0,8,0,3,0,0,1],
    #                     [7,0,0,0,2,0,0,0,6],
    #                     [0,6,0,0,0,0,2,8,0],
    #                     [0,0,0,4,1,9,0,0,5],
    #                     [0,0,0,0,8,0,0,7,9]])

    #     for i,j in np.ndindex(input_matrix.shape):
    #         x = i + 1
    #         y = j + 1
    #         if input_matrix[i, j] == 0:
    #             self.var_history.append((x, y, 1, True))
    #         else:
    #             self.init_vars.append((x, y, input_matrix[i, j]))

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

    def set_numbers(self) -> None:
        self.ax.clear()

        self.setup_axes(self.ax)

        for k, v in self.init_vars.items():
            x, y = k
            z = v
            self.ax.text(x-1, y-1, z, ha="center", va="center", color="black", size=25)

        for k, v in self.current_vars.items():
            x, y = k
            z = v
            self.ax.text(x-1, y-1, z, ha="center", va="center", color="red", size=25)

        self.ax.imshow(np.zeros((9,9)), cmap=self.white_cmap)

    def init(self) -> None:
        self.set_numbers()

    def update(self, i: int) -> None:
        if len(self.var_history) == 0:
            return

        for j in range(len(self.var_history)):
            x, y, z, is_added = self.var_history[j]
            
            if is_added and not (x, y) in self.init_vars:
                self.current_vars[(x, y)] = z
                self.var_history = self.var_history[j+1:]
                self.set_numbers()
                return

            elif not is_added and (x, y) in self.current_vars:
                if self.current_vars[(x, y)] == z:
                    del self.current_vars[(x, y)]
                    self.var_history = self.var_history[j+1:]
                    self.set_numbers()
                    return

        self.var_history = []
        return     

    # def run_animation(self) -> None:
    #     self.anim = FuncAnimation(fig=self.fig, func=self.update, frames=len(self.var_history), init_func=self.init, repeat=True, save_count=len(self.var_history))
    #     plt.show()

    #     self.anim.save(self.out_path, writer=PillowWriter(fps=15))

    def run_images(self) -> None:
        self.set_numbers()

        j: int = 0

        plt.savefig(self.out_path + 'plot_' + str(j) + '.png')
        j += 1

        for i in range(len(self.var_history)):
            x, y, z, is_added = self.var_history[i]
            
            if is_added and not (x, y) in self.init_vars:
                self.current_vars[(x, y)] = z
                self.set_numbers()
                plt.savefig(self.out_path + 'plot_' + str(j) + '.png')
                j += 1
                continue

            elif not is_added and (x, y) in self.current_vars:
                if self.current_vars[(x, y)] == z:
                    del self.current_vars[(x, y)]
                    self.set_numbers()
                    plt.savefig(self.out_path + 'plot_' + str(j) + '.png')
                    j += 1
                    continue

        return    


# if __name__ == '__main__':
#     viz = Visualizer([], [], out_path=None, debug_mode=True)
    

    #     # merge the SATProblems and solve it
    # total_problem = __merge_sat_problems__([SATProblem(s) for s in args.rest])
    # dpll = dplls[args.S](total_problem)
    # satisfied, assignments = dpll.solve()
    # init_vars = dpll.get_initial_unit_variables()
    # var_history = dpll.get_variable_assignment_history()

    # print("\nSatisfied: {}".format(satisfied))
    # if satisfied:
    #     # make a printable solution if there is one
    #     items = list(assignments.items())
    #     items.sort()
    #     print("Solution: {}".format([(k, j) for k, j in items if j]))
    #     output_dir = args.O if args.O else result_dir + strftime("%d_%m_%Y_%H_%M_%S", localtime(time()))
    #     id = args.ID
    #     __save_results__(assignments, '--is-sudoku' not in args or args['--is-sudoku'] == 'yes', dpll, output_dir, id)

    #     vis = Visualizer(init_vars, var_history, out_path='plots/sudoku_9x9_1/')
    #     vis.run_images()