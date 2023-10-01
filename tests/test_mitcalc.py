import unittest
import dimstack

# this test is a copy of MITCalc User Interface diagram

m1 = dimstack.dim.Statistical(
    nom=208,
    tol=dimstack.tolerance.SymmetricBilateral(0.036),
    process_sigma=6,
    name="a",
    desc="Shaft",
)
m1.assume_normal_dist_skewed(0.25)
m2 = dimstack.dim.Statistical(
    nom=-1.75,
    tol=dimstack.tolerance.UnequalBilateral(0, -0.06),
    process_sigma=3,
    name="b",
    desc="Retainer ring",
)
m2.assume_normal_dist()
m3 = dimstack.dim.Statistical(nom=-23, tol=dimstack.tolerance.UnequalBilateral(0, -0.12), process_sigma=3, name="c", desc="Bearing")
m3.assume_normal_dist()
m4 = dimstack.dim.Statistical(
    nom=20,
    tol=dimstack.tolerance.SymmetricBilateral(0.026),
    process_sigma=3,
    name="d",
    desc="Bearing Sleeve",
)
m4.assume_normal_dist()
m5 = dimstack.dim.Statistical(nom=-200, tol=dimstack.tolerance.SymmetricBilateral(0.145), process_sigma=3, name="e", desc="Case")
m5.assume_normal_dist()
m6 = dimstack.dim.Statistical(
    nom=20,
    tol=dimstack.tolerance.SymmetricBilateral(0.026),
    process_sigma=3,
    name="f",
    desc="Bearing Sleeve",
)
m6.assume_normal_dist()
m7 = dimstack.dim.Statistical(nom=-23, tol=dimstack.tolerance.UnequalBilateral(0, -0.12), process_sigma=3, name="g", desc="Bearing")
m7.assume_normal_dist()
dims = [m1, m2, m3, m4, m5, m6, m7]

stack = dimstack.dim.Stack(name="stacks on stacks", dims=dims)


class MITCalc(unittest.TestCase):
    def test_input(self):
        self.assertEqual(len(stack.dims), 7)
        self.assertEqual(stack.dims[0].nominal, 208)
        self.assertEqual(stack.dims[0].tolerance.upper, 0.036)
        self.assertEqual(stack.dims[0].tolerance.lower, -0.036)

    def test_Closed(self):
        self.assertEqual(dimstack.utils.nround(stack.Closed.nominal), 0.25)
        self.assertEqual(dimstack.utils.nround(stack.Closed.tolerance.upper), 0.533)
        self.assertEqual(dimstack.utils.nround(stack.Closed.tolerance.lower), -0.233)

    def test_WC(self):
        self.assertEqual(dimstack.utils.nround(stack.WC.nominal), 0.4)
        self.assertEqual(dimstack.utils.nround(stack.WC.tolerance.T / 2), 0.383)
        self.assertEqual(dimstack.utils.nround(stack.WC.Z_min), 0.017)
        self.assertEqual(dimstack.utils.nround(stack.WC.Z_max), 0.783)

    def test_RSS(self):
        # self.assertEqual(dimstack.utils.nround(stack.RSS.mean), 0.4)
        self.assertEqual(dimstack.utils.nround(stack.RSS.nominal), 0.4)
        self.assertEqual(dimstack.utils.nround(stack.RSS.tolerance.T / 2), 0.17825)
        # self.assertEqual(dimstack.utils.nround(stack.RSS.stdev, 6), 0.059417)

    def test_RSS_assembly(self):
        eval = stack.RSS
        spec = dimstack.dim.Spec("spec", "", dim=eval, LL=0.05, UL=0.8)

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

        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).nominal), 0.4)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).nominal), 0.4)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).tolerance.T / 2), 0.26433)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).distribution.stdev, 6), 0.05874)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).Z_min), 0.13567)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).Z_max), 0.66433)

    def test_SixSigma_assembly(self):
        eval = stack.SixSigma(at=4.5)
        spec = dimstack.dim.Spec("spec", "", dim=eval, LL=0.05, UL=0.8)

        # self.assertEqual(dimstack.utils.nround(spec.C_p), 2.12804) # temporarily removed 20230623
        # self.assertEqual(dimstack.utils.nround(spec.C_pk), 1.98617) # temporarily removed 20230623
        self.assertEqual(dimstack.utils.nround(spec.R, 1), 0.0)


if __name__ == "__main__":
    unittest.main()
