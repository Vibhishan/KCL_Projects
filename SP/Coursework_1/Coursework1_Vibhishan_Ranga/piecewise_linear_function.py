import random

INTERPOLATIONTYPE = ['nearestNeighboor', 'linear']
EXTRAPOLATIONTYPE = ['nearestNeighboor', 'linear']


class PiecewiseLinearFunction:
    """
    Class that represents a piecewise linear function. The function is
    parametrised by a list of points encoded each by a coordinate (1D) and a
    value.
    """

    def __init__(self,
                 values=None,
                 rand_num_values=None,
                 interpolation=INTERPOLATIONTYPE[0],
                 extrapolation=EXTRAPOLATIONTYPE[0]):
        self.inputs = dict()

        # if the values are not null values and if random num values are not null, then we raise a Key Error.
        if values is not None and rand_num_values is not None:
            raise KeyError

        # if values are not null, we iterate through all the values in given tuple and check if the instance of value
        # is interger or float (datatype). If it is not, we raise a Type Error. Otherwise, we add them into the dictionary.
        if values is not None:
            for (key, value) in values:
                if key not in self.inputs:
                    if not isinstance(value, (int, float)):
                        raise TypeError
                    else:
                        self.inputs[key] = value
                else:
                    # if a duplicate key is given then we raise a Value Error.
                    raise ValueError

        # if interpolation type is not nearest neighbor of linear, we raise Value Error.
        # if extrapolation type is not nearest neighbor of linear, we raise Value Error.
        if (interpolation not in INTERPOLATIONTYPE) or (extrapolation not in EXTRAPOLATIONTYPE):
            raise ValueError

        self.interpolation = interpolation
        self.extrapolation = extrapolation

        # if random number values are not null and it is of type integer or float then we create a input dictionary
        # with random values. Otherwise, we raise a Type Error.
        if rand_num_values is not None:
            if isinstance(rand_num_values, (int, float)):
                self.inputs = dict(zip(
                    random.sample(range(-1000, 1000), rand_num_values),
                    random.sample(range(-100, 100), rand_num_values)))
            else:
                raise TypeError
        self._update_params()

    def _update_params(self):
        self.num = len(self.inputs)
        self.min_coord, self.max_coord = self.get_min_max_coord()

    def get_min_max_coord(self):
        if len(self.inputs) == 0:
            return None, None
        min_coord = float('+inf')
        max_coord = float('-inf')
        for v in self.inputs.keys():
            if v < min_coord:
                min_coord = v
            if v > max_coord:
                max_coord = v
        return min_coord, max_coord

    def __iter__(self):
        return self.inputs.items().__iter__()

    def interp(self, coord):
        """
        Interpolate the value at any coordinate using linear interpolation
        from the two closest points
        :param coord: real scalar value that encodes the coordinate of the
        value to interpolate
        :return: the interpolated value
        """
        # if coordinates are not of the type integer or float, we raise Type Error.
        if not isinstance(coord, (int, float)):
            raise TypeError
        # Call the extrapolation function if the coordinate is outside of the
        # range
        if not self.min_coord < coord < self.max_coord:
            return self.extrap(coord)
        if self.interpolation == 'nearestNeighboor':
            # Extract the closest point and return the corresponding value
            closest = sorted(self.inputs.keys(),
                             key=lambda c: abs(c - coord))[0]
            return self.inputs[closest]
        else:
            # implemented the following formula.
            # ratio = (C-A)/(B-A)
            # value[C] = value[A] * (1-ratio) + value[B] * ratio
            minKey = self.min_coord
            minValue = self.inputs[minKey]
            maxKey = self.max_coord
            maxValue = self.inputs[maxKey]
            def interp(c): return minValue * (1-(c-minKey) /
                                              (maxKey-minKey)) + maxValue * (c-minKey)/(maxKey-minKey)

            return interp(coord)

    def extrap(self, coord):
        """
        Extrapolate the value at any coordinate
        :param coord: real scalar value that encodes the coordinate of the
        value to extrapolate
        :return: the extrapolated value
        """
        # if coordinates are not of type integer or float, we raise Type Error.
        if not isinstance(coord, (int, float)):
            raise TypeError
        if self.extrapolation == 'nearestNeighboor':
            if coord <= self.min_coord:
                return self.inputs[self.min_coord]
            elif coord >= self.max_coord:
                return self.inputs[self.max_coord]
            else:
                return self.interp(coord)
        else:
            # implemented the following formula.
            # ratio = (C-A)/(B-A)
            # value[C] = value[A] * (1-ratio) + value[B] * ratio
            minKey = self.min_coord
            minValue = self.inputs[minKey]
            maxKey = self.max_coord
            maxValue = self.inputs[maxKey]
            def extrap(c): return minValue * (1-(c-minKey) /
                                              (maxKey-minKey)) + maxValue * (c-minKey)/(maxKey-minKey)

            return extrap(coord)

    def remove_point(self, coord):
        """
        Remove a data point from the dictionary encoding the parameters.
        :param coord: Coordinate of the point to remove
        """
        if not isinstance(coord, (int, float)):
            raise TypeError('A real numerical value is expected as '
                            'a coordinate')
        if coord in self.inputs.keys():
            del self.inputs[coord]
        else:
            raise ValueError('The specified coordinate does not exist')
        self._update_params()

    def add_point(self, coord_value):
        """
        Add a data point to parametrise the function
        :param coord_value: tuple encoding the coordinate and associated value
        """
        if not isinstance(coord_value, tuple):
            raise TypeError('The point to be added is expected to be encoded'
                            ' as a tuple containing (coordinate, value)')
        if not isinstance(coord_value[0], (int, float)):
            raise TypeError('A real numerical value is expected as '
                            'a coordinate')
        if not isinstance(coord_value[1], (int, float)):
            raise TypeError('A real numerical value is expected as '
                            'a value')
        if coord_value[0] in self.inputs.keys():
            raise ValueError('The specified coordinate already exists')
        self.inputs[coord_value[0]] = coord_value[1]
        self._update_params()

    def __iadd__(self, other):
        """
        Define the addition operator for two objects of type
        PiecewiseLinearFunction or one PiecewiseLinearFunction and a real
        number
        :param other: right-hand side argument
        :return: A PiecewiseLinearFunction object
        """
        # Declaring the new inputs dictionary
        new_values = dict()
        # Add two functions
        # Check if the other is of type PiecewiseLinearFunction
        if isinstance(other, PiecewiseLinearFunction):
            # Iterate over all the items in self.inputs and add the intercept using other instance.
            # Then new values are added in the new dictionary
            for c, v in self.inputs.items():
                new_values[c] = v + other.interp(c)
            # If there are some remaining coord value pairs in other they are added to the new dictionary
            for c2, v2 in other:
                if c2 not in new_values.keys():
                    new_values[c2] = self.interp(c2) + v2
        # Add a constant if the other is of type integer or float
        elif isinstance(other, (int, float)):
            for c, v in self.inputs.items():
                new_values[c] = v + other
        else:
            # Raise a TypeError if the other is not of type integer or float or PiecewiseLinearFunction
            raise TypeError('Unsupported data type')

        # Finally we add the new values to self.inputs, thus making it += opertor i.e., modifying the values
        # of the self.inputs.items
        # We use remove point and add point functions to perform this task
        for c, v in new_values.items():
            if c in self.inputs:
                self.remove_point(c)
                self.add_point((c, v))
            else:
                self.add_point((c, v))
        return self

    def __add__(self, other):
        """
        Define the addition operator for two objects of type
        PiecewiseLinearFunction or one PiecewiseLinearFunction and a real
        number
        :param other: right-hand side argument
        :return: A PiecewiseLinearFunction object
        """
        new_values = dict()
        # Add two functions
        if isinstance(other, PiecewiseLinearFunction):
            for c, v in self.inputs.items():
                new_values[c] = v + other.interp(c)
            for c2, v2 in other:
                if c2 not in new_values.keys():
                    new_values[c2] = self.interp(c2) + v2
        # Add a constant to the left-hand side operand
        elif isinstance(other, (int, float)):
            for c, v in self.inputs.items():
                new_values[c] = v + other
        else:
            raise TypeError('Unsupported data type')
        return PiecewiseLinearFunction(new_values)

    def get_lists_sorted_by_coord(self):
        """
        Returns two lists as a tuple containing the ordered coordinates and the
        corresponding values in the corresponding order.
        :return: a tuple of two lists
        """
        sorted_dict = sorted(self.inputs.items())
        sorted_keys = [i[0] for i in sorted_dict]
        sorted_values = [i[1] for i in sorted_dict]
        return sorted_keys, sorted_values
