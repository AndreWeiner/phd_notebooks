"""Helper module to process simulation data.

Cotains the following data structures:
- Logfile: read and analyze simulation log-files

"""

import pandas as pd
import numpy as np
import matplotlib.tri as tri

# parameters for uniform plot appearance
alpha_contour = 0.75
fontsize_contour = 14
fontsize_label = 24
fontsize_legend = 20
fontsize_tick = 20
figure_width = 16
line_width = 3


class Logfile():
    """Load and evaluate simulation log-files."""

    def __init__(self, path=None):
        """Initialize a Logfile object.

        Parameters
        ----------
        path - String : path to the log-file

        """
        self.path = path

    def read_logfile(self, usecols=None):
        """Read log-file from source.abs

        Parameters
        ----------
        usecols - List : list of columns to use as String

        """
        try:
            self.log = pd.read_csv(self.path, sep=',', usecols=usecols)
            print("Successfully read file \033[1m{}\033[0m".format(self.path))
        except Exception as general_exception:
            print("Error reading file \033[1m{}\033[0m".format(self.path))
            print(str(general_exception))

    def get_profile(self, x_axis=None, y_axis=None):
        """Get x-y-profile, e.g. for plotting y over x.

        Parameters
        ----------
        x_axis - String : column name for the first variable
        y_axis - String : column name for the second variable

        Returns
        -------
        x, y

        """
        return self.log[x_axis].values, self.log[y_axis].values

    def apply_to_range(self, range_name, start, end, value_name, function):
        """Apply function to values in a given range.

        A typical use would be to compute the average velocity between t=10 and
        t=15:
        range_name = "time"
        start = 10
        end = 15
        value_name = "u_x"
        function = np.mean

        Parameters
        ----------
        range_name - String : name of column which determines the range
        start - float       : start of range to consider
        end - float         : end of range to consider
        value_name - String : column on which to apply the function
        function - Function : function to apply to the extracted values

        Returns
        -------
        function(value)

        """
        values = self.log[(self.log[range_name] >= start) & (self.log[range_name] <= end)]
        return function(values[value_name].values)

    def get_min_max(self, range_name, start, end, value_name):
        """Get min and max of value_name in a given range.

        Parameters
        ----------
        range_name - String : name of column that determines the range
        start - Float       : start of range
        end - Float         : end of range
        value_name - String : name of column where to compute min and max

        Returns
        -------
        min_val, max_val

        """
        values = self.log[(self.log[range_name] >= start) & (self.log[range_name] <= end)]
        return np.amin(values[value_name].values), np.amax(values[value_name].values)

    def find_closest(self, value_name, value):
        """Find row where the value of value_name is closest to value.

        Parameters
        ----------
        value_name - String : name of the column to search in
        value - Float       : value to search for

        Returns
        -------
        row

        """
        row = self.log.iloc[(self.log[value_name] - value).abs().argsort()[:1]]
        return row


class CenterFieldValues2D():
    def __init__(self, path=None, center=None, u_b=None):
        """Initialize CenterFieldValue2D object.

        Parameters
        ----------
        path - String : path to data file
        center - array-like : [x,y] coordinates of the center of mass
        U_b - array-like : [u_x, u_y] components of the bubble rise velocity

        """
        self.path = path
        self.center = center
        self.u_b = u_b
        self.read_field()
        self.create_triangulation()

    def read_field(self):
        """Read center values from disk."""
        try:
            names = ['f', 'ref', 'u_x', 'u_y', 'u_z', 'x', 'y', 'z']
            usecols = ['f', 'u_x', 'u_y', 'x', 'y']
            self.data = pd.read_csv(self.path, sep=',', header=0, names=names, usecols=usecols)
            print("Successfully read file \033[1m{}\033[0m".format(self.path))
        except Exception as read_exc:
            print("Error reading data from disk for file \033[1m{}\033[0m".format(self.path))
            print(str(read_exc))

    def create_triangulation(self):
        """Create a triangulation from points."""
        self.triang = tri.Triangulation(
            self.data['x'].values-self.center[0],
            self.data['y'].values-self.center[1])

    def interpolate_velocity(self, xi, yi, relative=False, magnitude=True):
        """Interpolate velocity at given points.

        Parameters
        ----------
        xi, yi - array-like : x and y coordinates of interpolation points
        relative - Boolean : compute velocity relative to u_b if True
        magnitude - Boolean : return magnitude of vector if True

        Return
        ------
        u_xi, u_yi - array-like : interpolated velocity components
        mag(u_i) - array-like : magnitude of interpolated velocity

        """
        interpolator_u_x = tri.CubicTriInterpolator(
            self.triang, self.data['u_x'].values, kind='geom')
        interpolator_u_y = tri.CubicTriInterpolator(
            self.triang, self.data['u_y'].values, kind='geom')
        u_xi = interpolator_u_x(xi, yi)
        u_yi = interpolator_u_y(xi, yi)
        if relative:
            u_xi -= self.u_b[0]
            u_yi -= self.u_b[1]

        if magnitude:
            return np.sqrt(np.square(u_xi) + np.square(u_yi))
        else:
            return u_yi, u_xi  # paraview bug: the transform filter does not swap the vector components

    def interpolate_volume_fraction(self, xi, yi):
        """Interpolate volume fraction at given points.

        Parameters
        ----------
        xi, yi - array-like : x and y coordinates of interpolation points

        Return
        ------
        f - array-like : interpolated volume fraction

        """
        self.interpolator_f = tri.CubicTriInterpolator(
            self.triang, self.data['f'].values, kind='geom')
        return self.interpolator_f(xi, yi)
