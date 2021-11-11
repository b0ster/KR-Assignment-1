"""
This module contains the functions needed to graphically display
the solution to Sudoku puzzle. This module depends on matplotlib
library. The graphical output displays the cell evaluated in each
iteration, time taken to solve and shades the cells based on difficulty.
"""

__author__ = 'krishnakumarramamoorthy'

import time

import matplotlib.pyplot as plt
import matplotlib.patches as patch

import numpy as np


def visualize_solution(input_matrix, solved_matrix, graph, zero_indices, ts, out_path, time_to_solution):
    """
    Plotting function that takes sudoku solution and intermediate data
    and plots them. It create three axes, one for plotting the progress,
    one for printing the summary metrics, and one for solved sudoku.
    """
    # prepare figure window for plotting
    plt.figure().patch.set_facecolor('white')
    plt.suptitle('Sudoku Solver\n', fontsize=20, color=plt.cm.Blues(0.9))

    # plot the performance: number of iterations vs. numbers filled
    ax1 = plt.subplot2grid((20, 3), (1, 0), rowspan=17, colspan=2)
    [x, y, ylabels, eval_histogram, n] = generate_progress_data(graph, zero_indices)
    max_eval_per_cell = max(eval_histogram)
    total_iterations = n
    plot_decorate_performance_data(ax1, x, y, ylabels)

    # work on sudoku box area
    ax2 = plt.subplot2grid((20, 3), (10, 2), rowspan=10, colspan=1)
    create_colorbar(ax2, max_eval_per_cell)
    decorate_sudoku_box(ax2)
    fill_numbers(ax2, input_matrix, solved_matrix)
    shade_cell_by_difficulty(ax2, zero_indices, eval_histogram, max_eval_per_cell)

    # work on statistics area
    ax3 = plt.subplot2grid((20, 3), (1, 2), rowspan=7, colspan=1)
    time_to_plot = time.time() - ts
    write_statistics(ax3, time_to_solution, time_to_plot, total_iterations)

    # save figure and show
    plt.savefig(out_path)
    plt.show()


def generate_progress_data(graph, zero_indices):
    """
    Generate data for plotting the number of evaluations and cell being evaluated
    """
    counter = 0
    n = 0
    eval_histogram = [0] * len(zero_indices[0])
    ylabels = []
    x = []
    y = []
    for n in range(len(graph['index'])):
        y.append(graph['index'][n][1])
        eval_histogram[graph['index'][n][1]] += 1
        ylabels.append('[{},{}]'.format(zero_indices[0][graph['index'][n][1]] + 1,
                                        zero_indices[1][graph['index'][n][1]] + 1))
        x.append(counter)
        counter += 1
    return [x, y, ylabels, eval_histogram, n]


def plot_decorate_performance_data(ax1, x, y, ylabels):
    """
    Modify the objects in performance plot. Add labels, resize font, etc.
    """
    ax1.plot(x, y)
    ax1.set_title('Progress', fontsize=11, color='black', alpha=0.9)
    plt.xlabel('How long did it take to solve? \n (Number of Evaluations)', fontsize=10)
    plt.ylabel('Which cell was evaluated? (Unfilled Cell Index)', fontsize=10)
    # label the y-axis with the cell location in sudoku grid
    plt.yticks(y, ylabels, color='gray', fontsize=8)
    plt.xticks(color='gray')


def create_colorbar(ax2, max_eval_per_cell):
    """
    Create a color index for the colors used to show difficulty of cells in sudoku grid
    """
    # create a temporary imshow and use it to create a colorbar, then remove the imshow object
    data = np.random.randn(10, 10, max_eval_per_cell)
    cax = plt.imshow(data, interpolation='nearest', cmap=plt.cm.Blues)
    cbar = plt.colorbar(cax, orientation='horizontal', ticks=[])
    cbar.solids.set_edgecolor(None)
    cbar.ax.set_xlabel('How difficult was it to solve?\n(Easy - - - > Difficult)', fontsize=10)
    # clear dummy imshow plot; anything plotted before in ax2 won't persist. cbar is on its own axes
    ax2.cla()


def decorate_sudoku_box(ax2):
    """
    Modify line and color properties of sudoku grid to make it look good
    """
    [x, y, xr, yr] = generate_sudoku_box_lines()
    ax2.set_title('Solution\n\n', fontsize=11, color='black', alpha=0.9)
    ax2.plot(x, y, color='gray')
    ax2.plot(xr, yr, color='gray', linewidth=2)
    # move the x tick to top
    ax2.xaxis.tick_top()
    # turn off the tick markers
    ax2.tick_params(bottom='off', top='off', left='off', right='off')
    # rewrite the tick labels so that they are aligned at the center of each box and not at the border
    plt.xticks(np.arange(0.5, 9.5, 1), np.arange(1, 10, 1), color='gray', fontsize=8)
    # start numbering y labels from the top
    plt.yticks(np.arange(0.5, 9.5, 1), np.arange(1, 10, 1), color='gray', fontsize=8)


def fill_numbers(ax2, input_matrix, solved_matrix):
    # fill the numbers
    for i in range(9):
        for j in range(9):
            # quirk: when plotting matrix, transpose it; i is in y-axis and j is in x-axis
            if input_matrix[i,j] == 0:
                ax2.text(j + 0.5, i + 0.5, solved_matrix[i,j], horizontalalignment='center',
                         verticalalignment='center', color='black', fontsize=10)
            else:
                ax2.text(j + 0.5, i + 0.5, solved_matrix[i,j], horizontalalignment='center',
                         verticalalignment='center', color='gray', alpha=0.7, fontsize=10)


def shade_cell_by_difficulty(ax2, zero_indices, eval_histogram, max_eval_per_cell):
    """
    Shade the unfilled cells in sudoku box with a color representing
    difficulty. Difficulty is defined as number of times that cell
    was evaluated.
    """
    # fill the background with difficulty metric
    for c in range(len(zero_indices[0])):
        i = zero_indices[0][c]
        j = zero_indices[1][c]
        # quirk: when plotting matrix, transpose it; i is in y-axis and j is in x-axis
        ax2.add_patch(patch.Rectangle((j, i), 1, 1, facecolor=plt.cm.Blues(eval_histogram[c] * 1.0 / max_eval_per_cell),
                                      alpha=0.5))


def write_statistics(ax3, time_to_solution, time_to_plot, total_iterations):
    ax3.get_xaxis().set_visible(False)
    ax3.get_yaxis().set_visible(False)
    ax3.spines['left'].set_color('white')
    ax3.spines['right'].set_color('white')
    ax3.spines['top'].set_color('white')
    ax3.spines['bottom'].set_color('white')
    ax3.text(0.5, 0.9, '{:.2f} secs\n'.format(time_to_solution),
             horizontalalignment='center', verticalalignment='center', fontsize=16)
    ax3.text(0.5, 0.85, 'Time to solution', horizontalalignment='center', verticalalignment='center',
             fontsize=12, color='gray')
    ax3.text(0.5, 0.6, '{:.2f} secs\n'.format(time_to_plot), horizontalalignment='center',
             verticalalignment='center', fontsize=16)
    ax3.text(0.5, 0.55, 'Time to plot', horizontalalignment='center', verticalalignment='center',
             fontsize=12, color='gray')
    ax3.text(0.5, 0.3, '{} \n'.format(total_iterations), horizontalalignment='center',
             verticalalignment='center', fontsize=16)
    ax3.text(0.5, 0.25, 'Number of evaluations', horizontalalignment='center', verticalalignment='center',
             fontsize=12, color='gray')


def generate_sudoku_box_lines():
    # lines for cells
    x = []
    y = []
    # lines for regions
    xr = []
    yr = []

    # data for vertical lines
    for i in range(9):
        x.append(i)
        x.append(i)
        y.append(0)
        y.append(9)
        x.append(None)
        y.append(None)
        if divmod(i, 3)[1] == 0:
            xr.append(i)
            xr.append(i)
            yr.append(0)
            yr.append(9)
            xr.append(None)
            yr.append(None)

    # data for horizontal lines
    for j in range(9):
        x.append(0)
        x.append(9)
        y.append(j)
        y.append(j)
        x.append(None)
        y.append(None)
        if divmod(j, 3)[1] == 0:
            xr.append(0)
            xr.append(9)
            yr.append(j)
            yr.append(j)
            xr.append(None)
            yr.append(None)

    return [x, y, xr, yr]

input_matrix = np.matrix([[5,3,0,0,7,0,0,0,0],
                        [6,0,0,1,9,5,0,0,0],
                        [0,9,8,0,0,0,0,6,0],
                        [8,0,0,0,6,0,0,0,3],
                        [4,0,0,8,0,3,0,0,1],
                        [7,0,0,0,2,0,0,0,6],
                        [0,6,0,0,0,0,2,8,0],
                        [0,0,0,4,1,9,0,0,5],
                        [0,0,0,0,8,0,0,7,9]])
solved_matrix = np.matrix([[5,3,4,6,7,8,9,1,2],
                        [6,7,2,1,9,5,3,4,8],
                        [1,9,8,3,4,2,5,6,7],
                        [8,5,9,7,6,1,4,2,3],
                        [4,2,6,8,5,3,7,9,1],
                        [7,1,3,9,2,4,8,5,6],
                        [9,6,1,5,3,7,2,8,4],
                        [2,8,7,4,1,9,6,3,5],
                        [3,4,5,2,8,6,1,7,9]])
graph = {'index': [], 'values': []}
zero_indices = np.where(input_matrix == 0)
for i in zero_indices:
    graph['index'].append(i)
    graph['values'].append(solved_matrix[i])
ts = 1
time_to_solution = 10
out_path = 'plot'

visualize_solution(input_matrix, solved_matrix, graph, zero_indices, ts, out_path, time_to_solution)