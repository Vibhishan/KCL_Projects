import numpy as np
import matplotlib.pyplot as plt


class MyGrid:
    """
    Class to encapsulate your n-by-n grid data and methods required to compute
    the longest path(s)
    """
    def __init__(self, dim=10, int_range=(0, 5), seed=None):
        """
        Constructor that given a size and intensity range generates a random
        square grid
        :param dim: Dimension used to generate a grid
        :param int_range: Intensity range of value to randomly sample
        :param seed: Seed value used to generate the random grid.
        """
        if not isinstance(dim, int):
            raise TypeError("The dim argument is expected to be an integer")
        if not isinstance(int_range, (list, tuple)) or \
                len(int_range) != 2 or \
                not all(isinstance(i, int) for i in int_range):
            raise TypeError("The int_range argument is expected to a a list"
                            "or a tuple containing two integers")
        np.random.seed(seed)
        # Given the input arguments generate a grid. Note that the max
        # intensity value is inclusive
        self._grid = np.random.random_integers(int_range[0],
                                               int_range[1],
                                               (dim, dim))
        self.dim = dim

    def get_longest_path_bf(self):
        """ Method to be completed """
        return None

    def get_longest_path(self):
        """ Method to be completed """
        return None

    def draw_grid(self, paths=None):
        """
        Display the current grid and any path provided as argument
        :param paths: List of path(s) to be overlaid on the grid
        """
        # Display the grid using the blue-white-red colourmap
        plt.imshow(self._grid.T, cmap='bwr')
        plt.axis("off")
        # overlay numbers (slow so only do it for small images)
        if self._grid.size <= 100:
            for (i, j), z in np.ndenumerate(self._grid):
                plt.text(i, j, str(z), ha='center', va='center',
                         fontsize=15)

        # overlay any paths
        if paths is not None:
            colours = 'rgbcmykw'
            for i, path in enumerate(paths):
                # offset so lines don't overlap
                offset = -0.3 + (i * .7 / len(paths))
                y = np.array([j[0] for j in path]) + offset
                x = np.array([j[1] for j in path]) + offset
                plt.plot(x, y, color=colours[i % len(colours)],
                         linewidth=2)
        plt.show()
