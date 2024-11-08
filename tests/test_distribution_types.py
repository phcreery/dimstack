import unittest

import numpy as np

import dimstack

dimstack.display.mode("rich")


class PositiveDist(unittest.TestCase):
    def test_DoublePositiveBilateral(self):
        measurements = np.array([1.1, 0.9])
        measurements_dist = dimstack.dist.Normal.fit(measurements)
        tol = dimstack.tol.SymmetricBilateral(0.3)
        dim = dimstack.dim.Statistical(
            nom=1,
            tol=tol,
            distribution=measurements_dist,
            name="1",
        )

        self.assertEqual(dim.nominal, 1)
        self.assertEqual(dim.abs_lower, 0.7)
        self.assertEqual(dim.abs_upper, 1.3)

        self.assertEqual(measurements_dist.mean, 1)

        self.assertAlmostEqual(float(dim.yield_probability), 0.9973, 4)


class NegativeDist(unittest.TestCase):
    def test_DoublePositiveBilateral(self):
        measurements = np.array([-1.1, -0.9])
        measurements_dist = dimstack.dist.Normal.fit(measurements)
        tol = dimstack.tol.SymmetricBilateral(0.3)
        dim = dimstack.dim.Statistical(
            nom=-1,
            tol=tol,
            distribution=measurements_dist,
            name="1",
        )

        self.assertEqual(dim.nominal * dim.dir, -1)
        self.assertEqual(dim.abs_lower, -1.3)
        self.assertEqual(dim.abs_upper, -0.7)

        self.assertEqual(measurements_dist.mean, -1)

        self.assertAlmostEqual(float(dim.yield_probability), 0.9973, 4)


if __name__ == "__main__":
    unittest.main()
