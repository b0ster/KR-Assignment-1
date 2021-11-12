
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')

input_matrix = np.matrix([[5,3,0,0,7,0,0,0,0],
                        [6,0,0,1,9,5,0,0,0],
                        [0,9,8,0,0,0,0,6,0],
                        [8,0,0,0,6,0,0,0,3],
                        [4,0,0,8,0,3,0,0,1],
                        [7,0,0,0,2,0,0,0,6],
                        [0,6,0,0,0,0,2,8,0],
                        [0,0,0,4,1,9,0,0,5],
                        [0,0,0,0,8,0,0,7,9]])

solved_matrix = np.zeros(input_matrix.shape)
for i, j in np.ndindex(solved_matrix.shape):
    if not input_matrix[i, j] == 0:
        solved_matrix[i, j] = -1

binary = cm.get_cmap('binary', 256)
newcolors = binary(np.linspace(0, 1, 256))
white = np.array([1, 1, 1, 1])
newcolors[:, :] = white
newcmp = ListedColormap(newcolors)

fig, ax = plt.subplots()
# im = ax.imshow(input_matrix, cmap=newcmp)

plt.minorticks_on()

fig.tight_layout()

def set_numbers(ax, input_matrix, solved_matrix):
    # Minor ticks
    ax.set_xticks(np.arange(-.5, 9, 1), minor=True)
    ax.set_yticks(np.arange(-.5, 9, 1), minor=True)

    # Major ticks
    ax.set_xticks(np.arange(-.5, 9, 3))
    ax.set_yticks(np.arange(-.5, 9, 3))

    # Gridlines based on minor ticks
    ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
    ax.grid(which='major', color='black', linestyle='-', linewidth=5)

    ax.get_xaxis().set_ticklabels([])
    ax.get_yaxis().set_ticklabels([])

    for i, j in np.ndindex(input_matrix.shape):
        if input_matrix[i, j] > 0:
            ax.text(j, i, input_matrix[i, j], ha="center", va="center", color="black", size=25)

    for i, j in np.ndindex(solved_matrix.shape):
        if solved_matrix[i, j] > 0:
            ax.text(j, i, solved_matrix[i, j], ha="center", va="center", color="red", size=25)
    return ax

while(True):
    row, col = np.where(solved_matrix == 0)
    if len(row) > 0 and len(col) > 0:
        solved_matrix[row[0], col[0]] = np.random.randint(1,10)
    else:
        break
    ax, im = set_numbers(ax, im, input_matrix, solved_matrix)
    plt.draw()
    plt.pause(1)
    plt.clf()

def update(i):
    row, col = np.where(solved_matrix == 0)
    if len(row) > 0 and len(col) > 0:
        solved_matrix[row[0], col[0]] = np.random.randint(1, 10)
    ax.clear()
    ax = set_numbers(ax, input_matrix, solved_matrix)
    ax.imshow(input_matrix, cmap=newcmp)


anim = FuncAnimation(fig, update, frames=1000, repeat=False)
plt.show()

# anim.save('sudoku.gif', writer='imagemagick')