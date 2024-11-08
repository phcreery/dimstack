import unittest

import dimstack


class DoublePositiveBilateral(unittest.TestCase):
    def test_DoublePositiveBilateral(self):
        t = dimstack.tolerance.UnequalBilateral(upper=0.005, lower=0.004)
        self.assertEqual(t.upper, 0.005)
        self.assertEqual(t.lower, 0.004)


class DoubleNegativeBilateral(unittest.TestCase):
    def test_DoubleNegativeBilateral(self):
        t = dimstack.tolerance.UnequalBilateral(upper=-0.005, lower=-0.006)
        self.assertEqual(t.upper, -0.005)
        self.assertEqual(t.lower, -0.006)


class FlippedBilateral(unittest.TestCase):
    def test_FlippedBilateral(self):
        t = dimstack.tolerance.UnequalBilateral(upper=-0.005, lower=0.005)
        self.assertEqual(t.upper, 0.005)
        self.assertEqual(t.lower, -0.005)


class AbsRelPosNeg(unittest.TestCase):
    def test_Positive_Abs(self):
        d = dimstack.dim.Basic(
            nom=0.1,
            tol=dimstack.tolerance.SymmetricBilateral(0.2),
            name="B",
            desc="Washer Length",
        )
        self.assertAlmostEqual(d.abs_upper, 0.3)
        self.assertEqual(d.abs_lower, -0.1)

        self.assertAlmostEqual(d.rel_upper, 0.3)
        self.assertEqual(d.rel_lower, -0.1)

    def test_Negative_Abs(self):
        d = dimstack.dim.Basic(
            nom=-0.1,
            tol=dimstack.tolerance.SymmetricBilateral(0.2),
            name="B",
            desc="Washer Length",
        )
        self.assertAlmostEqual(d.abs_upper, 0.1)
        self.assertAlmostEqual(d.abs_lower, -0.3)  # Edge Case

        # self.assertEqual(d.rel_upper, 0.3)
        # self.assertEqual(d.rel_lower, -0.1)

    def test_Positive_Rel(self):
        d = dimstack.dim.Basic(
            nom=0.5,
            tol=dimstack.tolerance.UnequalBilateral(upper=0.1, lower=-0.2),
            name="B",
            desc="Washer Length",
        )
        self.assertAlmostEqual(d.rel_upper, 0.6)
        self.assertAlmostEqual(d.rel_lower, 0.3)

    def test_Negative_Rel(self):
        d = dimstack.dim.Basic(
            nom=-0.5,
            tol=dimstack.tolerance.UnequalBilateral(upper=0.1, lower=-0.2),
            name="B",
            desc="Washer Length",
        )
        self.assertEqual(d.rel_upper, 0.6)
        self.assertAlmostEqual(d.rel_lower, 0.3)


if __name__ == "__main__":
    unittest.main()
