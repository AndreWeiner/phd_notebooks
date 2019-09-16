"""Helper module to process simulation data.

Cotains the following data structures:
- Logfile: read and analyze simulation log-files

"""

import pandas as pd
import numpy as np


class Logfile():
    def __init__(self, path=None, ga=None):
        """Initialize a Logfile object.

        Parameters
        ----------
        path - String : path to the log-file

        """
        self.path = path
        self.read_logfile()

    def read_logfile(self, names=None, usecols=None):
        """Read log-file from source.abs

        Parameters
        ----------
        names - List   : list containing the column names as String
        usecols - List : list of columns to use as String

        """
        try:
            self.log = pd.read_csv(self.path, sep=',', header=None,
                                   names=names, usecols=usecols)
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
        return row.values
