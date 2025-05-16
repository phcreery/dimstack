import unittest

import dimstack as ds


class Positive(unittest.TestCase):
    def test_Positive_Bilateral_unequal(self):
        t = ds.tolerance.Bilateral.unequal(upper=0.005, lower=-0.004)
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
    def test_Negative_Bilateral_unequal(self):
        t = ds.tolerance.Bilateral.unequal(upper=0.005, lower=-0.004)
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


class Reviewed(unittest.TestCase):
    def test_Reviewed(self):
        d1 = ds.dim.Reviewed(
            dim=ds.dim.Basic(
                nom=1,
                tol=ds.tolerance.Bilateral.symmetric(1),
                name="a",
                desc="",
            )
        ).assume_normal_dist(3)

        self.assertAlmostEqual(d1.distribution.std_dev, 0.33333333)

        d2 = ds.dim.Reviewed(
            dim=ds.dim.Basic(
                nom=1,
                tol=ds.tolerance.Bilateral.symmetric(1),
                name="a",
                desc="",
            )
        ).assume_normal_dist(6)

        self.assertAlmostEqual(d2.distribution.std_dev, 0.16666667)


if __name__ == "__main__":
    unittest.main()
