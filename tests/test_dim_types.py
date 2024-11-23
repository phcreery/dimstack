import unittest

import dimstack as ds


class Positive(unittest.TestCase):
    def test_Positive_UnequalBilateral(self):
        t = ds.tolerance.UnequalBilateral(upper=0.005, lower=-0.004)
        self.assertEqual(t.upper, 0.005)
        self.assertEqual(t.lower, -0.004)
        d = ds.dim.Basic(
            nom=1,
            tol=t,
            name="a",
            desc="",
        )

        self.assertAlmostEqual(d.abs_upper, 1.005)
        self.assertAlmostEqual(d.abs_lower, 0.996)


class Negative(unittest.TestCase):
    def test_Negative_UnequalBilateral(self):
        t = ds.tolerance.UnequalBilateral(upper=0.005, lower=-0.004)
        d = ds.dim.Basic(
            nom=-1,
            tol=t,
            name="a",
            desc="",
        )

        self.assertEqual(d.nominal, 1)
        self.assertEqual(d.abs_nominal, -1)
        self.assertEqual(d.tolerance.upper, 0.005)
        self.assertEqual(d.tolerance.lower, -0.004)

        self.assertAlmostEqual(d.abs_upper_tol, 0.004)
        self.assertAlmostEqual(d.abs_lower_tol, -0.005)

        self.assertAlmostEqual(d.abs_upper, -0.996)
        self.assertAlmostEqual(d.abs_lower, -1.005)


if __name__ == "__main__":
    unittest.main()
