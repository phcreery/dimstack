import unittest

import dimstack

# this test is a copy of MITCalc User Interface diagram

m1 = dimstack.dim.Reviewed(
    dim=dimstack.dim.Basic(
        nom=208,
        tol=dimstack.tolerance.Bilateral.symmetric(0.036),
        name="a",
        desc="Shaft",
    ),
    target_process_sigma=6,
)
m1.assume_normal_dist_skewed(0.25)
m2 = dimstack.dim.Reviewed(
    dim=dimstack.dim.Basic(
        nom=-1.75,
        tol=dimstack.tolerance.Bilateral.unequal(0, -0.06),
        name="b",
        desc="Retainer ring",
    ),
    target_process_sigma=3,
)
m2.assume_normal_dist()
m3 = dimstack.dim.Reviewed(
    dim=dimstack.dim.Basic(nom=-23, tol=dimstack.tolerance.Bilateral.unequal(0, -0.12), name="c", desc="Bearing"),
    target_process_sigma=3,
)
m3.assume_normal_dist()
m4 = dimstack.dim.Reviewed(
    dim=dimstack.dim.Basic(
        nom=20,
        tol=dimstack.tolerance.Bilateral.symmetric(0.026),
        name="d",
        desc="Bearing Sleeve",
    ),
    target_process_sigma=3,
)
m4.assume_normal_dist()
m5 = dimstack.dim.Reviewed(
    dim=dimstack.dim.Basic(nom=-200, tol=dimstack.tolerance.Bilateral.symmetric(0.145), name="e", desc="Case"),
    target_process_sigma=3,
)
m5.assume_normal_dist()
m6 = dimstack.dim.Reviewed(
    dim=dimstack.dim.Basic(
        nom=20,
        tol=dimstack.tolerance.Bilateral.symmetric(0.026),
        name="f",
        desc="Bearing Sleeve",
    ),
    target_process_sigma=3,
)
m6.assume_normal_dist()
m7 = dimstack.dim.Reviewed(
    dim=dimstack.dim.Basic(nom=-23, tol=dimstack.tolerance.Bilateral.unequal(0, -0.12), name="g", desc="Bearing"),
    target_process_sigma=3,
)
m7.assume_normal_dist()
dims = [m1, m2, m3, m4, m5, m6, m7]

stack = dimstack.dim.ReviewedStack(name="stacks on stacks", dims=dims)


class MITCalc(unittest.TestCase):
    def test_input(self):
        self.assertEqual(len(stack.dims), 7)
        self.assertEqual(stack.dims[0].dim.nominal, 208)
        self.assertEqual(stack.dims[0].dim.tolerance.upper, 0.036)
        self.assertEqual(stack.dims[0].dim.tolerance.lower, -0.036)

    def test_Closed(self):
        self.assertEqual(dimstack.utils.nround(dimstack.calc.Closed(stack).nominal), 0.25)
        self.assertEqual(dimstack.utils.nround(dimstack.calc.Closed(stack).tolerance.upper), 0.533)
        self.assertEqual(dimstack.utils.nround(dimstack.calc.Closed(stack).tolerance.lower), -0.233)

    def test_WC(self):
        self.assertEqual(dimstack.utils.nround(dimstack.calc.WC(stack).nominal), 0.4)
        self.assertEqual(dimstack.utils.nround(dimstack.calc.WC(stack).tolerance.T / 2), 0.383)
        self.assertEqual(dimstack.utils.nround(dimstack.calc.WC(stack).abs_lower), 0.017)
        self.assertEqual(dimstack.utils.nround(dimstack.calc.WC(stack).abs_upper), 0.783)

    def test_RSS(self):
        # self.assertEqual(dimstack.utils.nround(stack.RSS.mean), 0.4)
        self.assertEqual(dimstack.utils.nround(dimstack.calc.RSS(stack).nominal), 0.4)
        self.assertEqual(dimstack.utils.nround(dimstack.calc.RSS(stack).tolerance.T / 2), 0.17825)
        # self.assertEqual(dimstack.utils.nround(stack.RSS.stdev, 6), 0.059417)

    def test_RSS_assembly(self):
        eval = dimstack.calc.RSS(stack)
        eval_dist = dimstack.dim.Reviewed(dim=eval)
        spec = dimstack.dim.Requirement("spec", "", distribution=eval_dist.distribution, LL=0.05, UL=0.8)

        self.assertEqual(dimstack.utils.nround(spec.R, 1), 0.0)

    # def test_MRSS(self):
    #     self.assertEqual(dimstack.utils.nround(stack.MRSS.mean), 0.4)
    #     self.assertEqual(dimstack.utils.nround(stack.MRSS.nominal), 0.4)
    #     # self.assertEqual(dimstack.utils.nround(stack.MRSS.tolerance.T / 2), 0.17825)
    #     self.assertEqual(dimstack.utils.nround(stack.MRSS.tolerance.T / 2), 0.2405)
    #     self.assertEqual(dimstack.utils.nround(stack.MRSS.stdev, 6), 0.059417)

    def test_SixSigma(self):
        self.assertEqual(dimstack.utils.nround(stack.dims[0].C_p), 2)
        self.assertEqual(dimstack.utils.nround(stack.dims[0].k), 0.25)
        self.assertEqual(dimstack.utils.nround(stack.dims[0].C_pk), 1.5)
        self.assertEqual(dimstack.utils.nround(stack.dims[0].mean_eff), 208.0)
        self.assertEqual(dimstack.utils.nround(stack.dims[0].stdev_eff), 0.008)

        self.assertEqual(dimstack.utils.nround(dimstack.calc.SixSigma(stack, at=4.5).dim.nominal), 0.4)
        # self.assertEqual(dimstack.utils.nround(dimstack.calc.SixSigma(stack, at=4.5).mean_eff), 0.4)
        self.assertEqual(dimstack.utils.nround(dimstack.calc.SixSigma(stack, at=4.5).dim.tolerance.T / 2), 0.26433)
        self.assertEqual(dimstack.utils.nround(dimstack.calc.SixSigma(stack, at=4.5).distribution.stdev, 6), 0.05874)
        self.assertEqual(dimstack.utils.nround(dimstack.calc.SixSigma(stack, at=4.5).dim.abs_lower), 0.13567)
        self.assertEqual(dimstack.utils.nround(dimstack.calc.SixSigma(stack, at=4.5).dim.abs_upper), 0.66433)

    def test_SixSigma_assembly(self):
        eval = dimstack.calc.SixSigma(stack, at=4.5)
        spec = dimstack.dim.Requirement("spec", "", distribution=eval.distribution, LL=0.05, UL=0.8)

        # self.assertEqual(dimstack.utils.nround(spec.C_p), 2.12804) # temporarily removed 20230623
        # self.assertEqual(dimstack.utils.nround(spec.C_pk), 1.98617) # temporarily removed 20230623
        self.assertEqual(dimstack.utils.nround(spec.R, 1), 0.0)


if __name__ == "__main__":
    unittest.main()
