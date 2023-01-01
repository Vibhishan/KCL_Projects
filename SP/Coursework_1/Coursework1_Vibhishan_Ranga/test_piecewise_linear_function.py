import unittest
from piecewise_linear_function import (PiecewiseLinearFunction,
                                       INTERPOLATIONTYPE,
                                       EXTRAPOLATIONTYPE)


class PiecewiseLinearFunctionInitTest(unittest.TestCase):
    # Test to check if we are able to invoke the PiecewiseLinearFunction correctly
    def test_type(self):
        F = PiecewiseLinearFunction()
        self.assertIsInstance(F, PiecewiseLinearFunction)

    # Test if values passed are correctly taken in.
    @staticmethod
    def test_input_values():
        PiecewiseLinearFunction(values=((1, 2), (2, 3), (3, 4)))

    # Test if rand_num_values passed are correct instance type and if program
    # runs without errors for one test case.
    @staticmethod
    def test_input_rand_num():
        PiecewiseLinearFunction(rand_num_values=2)

    # Test to raise Key Error if both values and rand_num_values are passed in same instance.
    def test_input_wrong_key(self):
        with self.assertRaises(KeyError):
            PiecewiseLinearFunction(values=((1, 2), (1, 2)),
                                    rand_num_values=3)

    # Test to check if Value error is raised if no value is passed for a coordinate.
    def test_input_wrong_size1(self):
        with self.assertRaises(ValueError):
            PiecewiseLinearFunction(values=((1, 2), (2,)))

    # Test to check if Value error is raised when more than 2 values are passed for one coordinate.
    def test_input_wrong_size2(self):
        with self.assertRaises(ValueError):
            PiecewiseLinearFunction(values=((1, 2, 3), (2, 3, 4)))

    # Test to check if Value Error raised if a duplicate key is given in the input.
    def test_input_duplicated_key(self):
        with self.assertRaises(ValueError):
            PiecewiseLinearFunction(values=((1, 1), (1, 2)))

    # Test to check if all interpolation types are accepted by the program.
    @staticmethod
    def test_input_interp():
        for t in INTERPOLATIONTYPE:
            PiecewiseLinearFunction(interpolation=t)

    # Test to check if all extrapolation types are accepted by the program.
    @staticmethod
    def test_input_extrap():
        for t in EXTRAPOLATIONTYPE:
            PiecewiseLinearFunction(extrapolation=t)

    # Test to check if Value Error raised when invalid value is passed as the interpolation type.
    def test_input_wong_interp(self):
        with self.assertRaises(ValueError):
            PiecewiseLinearFunction(interpolation='bla')

    # Test to check if Value Error raised when invalid value is passed as the extrapolation type.
    def test_input_wong_extrap(self):
        with self.assertRaises(ValueError):
            PiecewiseLinearFunction(extrapolation='bla')

    # Test to check if program is running without any errors if both int and float datatypes are passed in tuple
    # for the (coordinate,  value) pair.
    @staticmethod
    def test_input_type():
        PiecewiseLinearFunction(values=((1, 2), (3, 4)))
        PiecewiseLinearFunction(values=((1., 2), (3, 4)))
        PiecewiseLinearFunction(values=((float(1), 2), (3, 4)))

    # Test to check if Type Error is raised if any datatype other than integer or float is passed in
    # the (coordinate, value) pair.
    def test_input_wrong_type1(self):
        with self.assertRaises(TypeError):
            PiecewiseLinearFunction(values=((1, 'a'), (2, 3)))

    # Test to check if TypeError is raised if rand_num_values is not of instance integer or float.
    def test_input_wrong_type2(self):
        with self.assertRaises(TypeError):
            PiecewiseLinearFunction(rand_num_values='three')

    # Test to check intrapolation formula for the nearest neighbor method by giving correct inputs.
    def test_interp_nearest_neighbor(self):
        plf = PiecewiseLinearFunction(values=((2, 4), (3, 5)))
        result_plf = plf.interp(2.2)
        self.assertTrue(result_plf, 4)

    # Test to check extrapolation formula for the nearest neighbor method by giving correct inputs.
    def test_extrap_nearest_neighbor(self):
        plf = PiecewiseLinearFunction(values=((2, 4), (3, 5)))
        result_plf = plf.extrap(5.6)
        self.assertTrue(result_plf, 5)

    # Test to check intrapolation formula for the linear method by giving correct inputs.
    def test_interp_linear(self):
        plf = PiecewiseLinearFunction(
            values=((2, 4), (3, 5)), interpolation=INTERPOLATIONTYPE[1])
        result_plf = plf.interp(2.2)
        self.assertTrue(result_plf, 4.2)

    # Test to check extrapolation formula for the linear method by giving correct inputs.
    def test_extrap_linear(self):
        plf = PiecewiseLinearFunction(
            values=((2, 4), (3, 5)), extrapolation=EXTRAPOLATIONTYPE[1])
        result_plf = plf.extrap(5.6)
        self.assertTrue(result_plf, 7.600000000000001)

    # Test to check the Type Error raised when the input is string datatype in intrapolation function.
    def test_input_interp(self):
        with self.assertRaises(TypeError):
            plf = PiecewiseLinearFunction(values=((2, 4), (3, 5)))
            result_plf = plf.interp('f')

    # Test to check the Type Error raised when the input is list of strings in extrapolation function.
    def test_input_extrap(self):
        with self.assertRaises(TypeError):
            plf = PiecewiseLinearFunction(values=((2, 4), (3, 5)))
            result_plf = plf.extrap(['a', 'f', 'l'])

    # Test to check the intrapolation function value at infinity for nearest neighbor method.
    def test_input_inf_interp_nearest_neighbor(self):
        plf = PiecewiseLinearFunction(values=((0, 0), (float('+inf'), 0)))
        result_plf = plf.interp(2.2)
        self.assertEqual(result_plf, 0)

    # Test to check the intrapolation function value at infinity for linear method.
    def test_input_inf_interp_linear(self):
        plf = PiecewiseLinearFunction(
            values=((0, 0), (float('+inf'), 0)), interpolation=INTERPOLATIONTYPE[1])
        result_plf = plf.interp(2.2)
        self.assertEqual(result_plf, 0.0)

    # Test to check the extrapolation function value at infinity for nearest neighbor method.
        plf = PiecewiseLinearFunction(values=((0, 0), (float('+inf'), 0)))
        result_plf = plf.extrap(-2.2)
        self.assertEqual(result_plf, 0)

    # Test to check the extrapolation function value at infinity for linear method.
    def test_input_inf_extrap_linear(self):
        plf = PiecewiseLinearFunction(
            values=((0, 0), (float('+inf'), 0)), extrapolation=EXTRAPOLATIONTYPE[1])
        result_plf = plf.extrap(-2.2)
        self.assertEqual(result_plf, 0.0)

    # Test to check the Type Error raised when the input is string datatype in iadd (+=) function.
    def test_iadd_wrong_input_type(self):
        with self.assertRaises(TypeError):
            plf = PiecewiseLinearFunction(values=((2, 4), (3, 5)))
            plf2 = 'afl'
            plf.__iadd__(plf2).inputs

    # Test to check if input values are correct in the iadd (+=) function with 2 different gradient lines.
    def test_iadd_input_type(self):
        plf2 = PiecewiseLinearFunction(values=((3, 4), (6, 9)))
        plf = PiecewiseLinearFunction(values=((2, 4), (3, 5)))
        self.assertEqual(plf.__iadd__(plf2).inputs, {2: 8, 3: 9, 6: 14})

    # Test giving one input as an instance of PiecewiseLinearFunction and other as a integer.
    def test_iadd_input_type_integer(self):
        plf2 = 18
        plf = PiecewiseLinearFunction(values=((2, 4), (3, 5)))
        self.assertEqual(plf.__iadd__(plf2).inputs, {2: 22, 3: 23})

    # Test to add two PiecewiseLinearFunctions with different size of inputs.
    def test_iadd_different_sizes(self):
        plf2 = PiecewiseLinearFunction(values=((3, 4), (6, 9), (10, 15)))
        plf = PiecewiseLinearFunction(values=((2, 4), (3, 5)))
        self.assertEqual(plf.__iadd__(plf2).inputs, {
                         2: 8, 3: 9, 6: 14, 10: 20})


if __name__ == '__main__':
    unittest.main()
