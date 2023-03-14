import unittest
import dimstack.display
import dimstack.tolerance
import dimstack.eval
import dimstack.utils

# this test is a copy of MITCalc User Interface diagram

m1 = dimstack.eval.StatisticalDimension(
    nom=208,
    tol=dimstack.tolerance.SymmetricBilateral(0.036),
    process_sigma=6,
    k=0.25,
    name="a",
    desc="Shaft",
)
m2 = dimstack.eval.StatisticalDimension(
    nom=-1.75,
    tol=dimstack.tolerance.UnequalBilateral(0, 0.06),
    process_sigma=3,
    name="b",
    desc="Retainer ring",
)
m3 = dimstack.eval.StatisticalDimension(nom=-23, tol=dimstack.tolerance.UnequalBilateral(0, 0.12), process_sigma=3, name="c", desc="Bearing")
m4 = dimstack.eval.StatisticalDimension(
    nom=20,
    tol=dimstack.tolerance.SymmetricBilateral(0.026),
    process_sigma=3,
    name="d",
    desc="Bearing Sleeve",
)
m5 = dimstack.eval.StatisticalDimension(nom=-200, tol=dimstack.tolerance.SymmetricBilateral(0.145), process_sigma=3, name="e", desc="Case")
m6 = dimstack.eval.StatisticalDimension(
    nom=20,
    tol=dimstack.tolerance.SymmetricBilateral(0.026),
    process_sigma=3,
    name="f",
    desc="Bearing Sleeve",
)
m7 = dimstack.eval.StatisticalDimension(nom=-23, tol=dimstack.tolerance.UnequalBilateral(0, 0.12), process_sigma=3, name="g", desc="Bearing")
items = [m1, m2, m3, m4, m5, m6, m7]

stack = dimstack.eval.Stack(title="stacks on stacks", items=items)


class MITCalc(unittest.TestCase):
    def test_input(self):
        self.assertEqual(len(stack.items), 7)
        self.assertEqual(stack.items[0].nominal, 208)
        self.assertEqual(stack.items[0].tolerance.upper, 0.036)
        self.assertEqual(stack.items[0].tolerance.lower, 0.036)

    def test_Closed(self):
        self.assertEqual(dimstack.utils.nround(stack.Closed.nominal), 0.25)
        self.assertEqual(dimstack.utils.nround(stack.Closed.tolerance.upper), 0.533)
        self.assertEqual(dimstack.utils.nround(stack.Closed.tolerance.lower), 0.233)

    def test_WC(self):
        self.assertEqual(dimstack.utils.nround(stack.WC.mean), 0.4)
        self.assertEqual(dimstack.utils.nround(stack.WC.tolerance.T / 2), 0.383)
        self.assertEqual(dimstack.utils.nround(stack.WC.Z_min), 0.017)
        self.assertEqual(dimstack.utils.nround(stack.WC.Z_max), 0.783)

    def test_RSS(self):
        self.assertEqual(dimstack.utils.nround(stack.RSS.mean), 0.4)
        self.assertEqual(dimstack.utils.nround(stack.RSS.nominal), 0.4)
        self.assertEqual(dimstack.utils.nround(stack.RSS.tolerance.T / 2), 0.17825)
        # self.assertEqual(dimstack.utils.nround(stack.RSS.stdev, 6), 0.059417)

    def test_RSS_assembly(self):
        eval = stack.RSS
        assy = dimstack.eval.Assembly("assy", "", dim=eval, LL=0.05, UL=0.8, process_sigma=4.5)

        self.assertEqual(dimstack.utils.nround(assy.R, 1), 0.0)

    # def test_MRSS(self):
    #     self.assertEqual(dimstack.utils.nround(stack.MRSS.mean), 0.4)
    #     self.assertEqual(dimstack.utils.nround(stack.MRSS.nominal), 0.4)
    #     # self.assertEqual(dimstack.utils.nround(stack.MRSS.tolerance.T / 2), 0.17825)
    #     self.assertEqual(dimstack.utils.nround(stack.MRSS.tolerance.T / 2), 0.2405)
    #     self.assertEqual(dimstack.utils.nround(stack.MRSS.stdev, 6), 0.059417)

    def test_SixSigma(self):
        self.assertEqual(dimstack.utils.nround(stack.items[0].C_p), 2)
        self.assertEqual(dimstack.utils.nround(stack.items[0].k), 0.25)
        self.assertEqual(dimstack.utils.nround(stack.items[0].C_pk), 1.5)
        self.assertEqual(dimstack.utils.nround(stack.items[0].mean_eff), 208.0)
        self.assertEqual(dimstack.utils.nround(stack.items[0].stdev_eff), 0.008)

        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).mean), 0.4)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).nominal), 0.4)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).tolerance.T / 2), 0.26433)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).stdev, 6), 0.05874)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).Z_min), 0.13567)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).Z_max), 0.66433)

    def test_sixsigma_assembly(self):
        eval = stack.SixSigma(at=4.5)
        assy = dimstack.eval.Assembly("assy", "", dim=eval, LL=0.05, UL=0.8, process_sigma=4.5)

        self.assertEqual(dimstack.utils.nround(assy.C_p), 2.12804)
        self.assertEqual(dimstack.utils.nround(assy.C_pk), 1.98617)
        self.assertEqual(dimstack.utils.nround(assy.R, 1), 0.0)


if __name__ == "__main__":
    unittest.main()
