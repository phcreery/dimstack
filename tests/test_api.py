import unittest

import dimstack as ds


class API(unittest.TestCase):
    def test_dim(self):
        """
        test inferred symmetric tolerance
        and root alias
        """
        d = ds.Basic(10, 0.1)
        self.assertEqual(d.nominal, 10)
        self.assertEqual(d.tolerance.upper, 0.1)
        self.assertEqual(d.tolerance.lower, -0.1)

    def test_dim_printing(self):
        """
        test print result
        """
        d = ds.Basic(10, 0.1)
        self.assertEqual(f"{d}", "10 ± 0.1")
        d.nominal = -10
        self.assertEqual(f"{d}", "-10 ± 0.1")

    def test_stack_printing(self):
        """
        test print result
        """
        d1 = ds.Basic(10, 0.1)
        d2 = ds.Basic(-10, 0.1)
        stack = ds.Stack(name="test stack", dims=[d1, d2])
        expected = "test stack (2 dims)\n10 ± 0.1\n-10 ± 0.1"
        self.assertEqual(f"{stack}", expected)

    def test_reviewed_dim_printing(self):
        """
        test print result
        """
        d = ds.Basic(10, 0.1)
        r = ds.Reviewed(d)
        self.assertEqual(f"{r}", "10 ± 0.1 @ Normal Dist. μ=10.0, σ=0.01667")

    def test_reviewed_stack_printing(self):
        """
        test print result
        """
        d1 = ds.Basic(10, 0.1)
        d2 = ds.Basic(-10, 0.1)
        r1 = ds.Reviewed(d1)
        r2 = ds.Reviewed(d2)
        stack = ds.ReviewedStack(name="test reviewed stack", dims=[r1, r2])
        expected = "test reviewed stack (2 dims)\n10 ± 0.1 @ Normal Dist. μ=10.0, σ=0.01667\n-10 ± 0.1 @ Normal Dist. μ=-10.0, σ=0.01667"
        self.assertEqual(f"{stack}", expected)

    def test_requirement_printing(self):
        """
        test print result
        """
        measurement = ds.Basic(11, 0.1).review()
        r = ds.Requirement(LL=9, UL=11, name="spec", desc="", distribution=measurement.distribution)
        self.assertEqual(f"{r}", "spec [9, 11] Normal Dist. μ=11.0, σ=0.01667")
