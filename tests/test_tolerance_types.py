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


if __name__ == "__main__":
    unittest.main()
