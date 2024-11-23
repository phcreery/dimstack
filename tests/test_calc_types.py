import unittest

import dimstack as ds


class Negative(unittest.TestCase):
    def test_Negative_Closed(self):
        t = ds.tolerance.UnequalBilateral(upper=0.05, lower=0)
        d1 = ds.dim.Basic(
            nom=1,
            tol=t,
            name="a",
            desc="",
        )

        t = ds.tolerance.UnequalBilateral(upper=0.05, lower=0)
        d2 = ds.dim.Basic(
            nom=-2,
            tol=t,
            name="a",
            desc="",
        )

        stack = ds.dim.Stack(name="stacks on stacks", dims=[d1, d2])
        c = ds.calc.Closed(stack)

        self.assertAlmostEqual(c.abs_upper, -0.95)
        self.assertAlmostEqual(c.abs_lower, -1.05)

    def test_Negative_Closed1(self):
        t = ds.tolerance.UnequalBilateral(upper=0.05, lower=0)
        d1 = ds.dim.Basic(
            nom=1,
            tol=t,
            name="a",
            desc="",
        )
        self.assertAlmostEqual(d1.abs_upper, 1.05)
        self.assertAlmostEqual(d1.abs_lower, 1)
        self.assertAlmostEqual(d1.abs_upper_tol, 0.05)
        self.assertAlmostEqual(d1.abs_lower_tol, 0)

        t = ds.tolerance.UnequalBilateral(upper=0, lower=-0.05)
        d2 = ds.dim.Basic(
            nom=-2,
            tol=t,
            name="a",
            desc="",
        )
        self.assertAlmostEqual(d2.dir, -1)
        self.assertAlmostEqual(d2.a, 1)
        self.assertAlmostEqual(d2.abs_upper, -1.95)
        self.assertAlmostEqual(d2.abs_lower, -2)
        self.assertAlmostEqual(d1.abs_upper_tol, 0.05)
        self.assertAlmostEqual(d1.abs_lower_tol, 0)

        stack = ds.dim.Stack(name="stacks on stacks", dims=[d1, d2])
        c = ds.calc.Closed(stack)

        self.assertAlmostEqual(c.abs_nominal, -1)
        self.assertAlmostEqual(c.abs_upper, -0.9)
        self.assertAlmostEqual(c.abs_lower, -1.0)


if __name__ == "__main__":
    unittest.main()
