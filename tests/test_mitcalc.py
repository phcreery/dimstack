import unittest
import dimstack.tolerance as ds

# this test is a copy of MITCalc User Interface diagram

m1 = ds.StatisticalDimension(
    nom=208,
    tol=ds.SymmetricBilateral(0.036),
    process_sigma=6,
    k=0.25,
    name="a",
    desc="Shaft",
)
m2 = ds.StatisticalDimension(
    nom=-1.75,
    tol=ds.UnequalBilateral(0, 0.06),
    process_sigma=3,
    name="b",
    desc="Retainer ring",
)
m3 = ds.StatisticalDimension(
    nom=-23, tol=ds.UnequalBilateral(0, 0.12), process_sigma=3, name="c", desc="Bearing"
)
m4 = ds.StatisticalDimension(
    nom=20,
    tol=ds.SymmetricBilateral(0.026),
    process_sigma=3,
    name="d",
    desc="Bearing Sleeve",
)
m5 = ds.StatisticalDimension(
    nom=-200, tol=ds.SymmetricBilateral(0.145), process_sigma=3, name="e", desc="Case"
)
m6 = ds.StatisticalDimension(
    nom=20,
    tol=ds.SymmetricBilateral(0.026),
    process_sigma=3,
    name="f",
    desc="Bearing Sleeve",
)
m7 = ds.StatisticalDimension(
    nom=-23, tol=ds.UnequalBilateral(0, 0.12), process_sigma=3, name="g", desc="Bearing"
)
items = [m1, m2, m3, m4, m5, m6, m7]

stack = ds.Stack(title="stacks on stacks", items=items)


class MITCalc(unittest.TestCase):
    def test_input(self):
        self.assertEqual(len(stack.items), 7)
        self.assertEqual(stack.items[0].nominal, 208)
        self.assertEqual(stack.items[0].tolerance.upper, 0.036)
        self.assertEqual(stack.items[0].tolerance.lower, 0.036)

    def test_Closed(self):
        self.assertEqual(ds.round(stack.Closed.nominal), 0.25)
        self.assertEqual(ds.round(stack.Closed.tolerance.upper), 0.533)
        self.assertEqual(ds.round(stack.Closed.tolerance.lower), 0.233)

    def test_WC(self):
        self.assertEqual(ds.round(stack.WC.mu), 0.4)
        self.assertEqual(ds.round(stack.WC.tolerance.T / 2), 0.383)
        self.assertEqual(ds.round(stack.WC.Z_min), 0.017)
        self.assertEqual(ds.round(stack.WC.Z_max), 0.783)

    def test_RSS(self):
        self.assertEqual(ds.round(stack.RSS.mu), 0.4)
        self.assertEqual(ds.round(stack.RSS.nominal), 0.4)
        self.assertEqual(ds.round(stack.RSS.tolerance.T / 2), 0.17825)
        # self.assertEqual(ds.round(stack.RSS.sigma, 6), 0.059417)

    def test_RSS_assembly(self):
        eval = stack.RSS
        assy = ds.Assembly("assy", "", dim=eval, LL=0.05, UL=0.8, process_sigma=4.5)

        self.assertEqual(ds.round(assy.R, 1), 0.0)

    # def test_MRSS(self):
    #     self.assertEqual(ds.round(stack.MRSS.mu), 0.4)
    #     self.assertEqual(ds.round(stack.MRSS.nominal), 0.4)
    #     # self.assertEqual(ds.round(stack.MRSS.tolerance.T / 2), 0.17825)
    #     self.assertEqual(ds.round(stack.MRSS.tolerance.T / 2), 0.2405)
    #     self.assertEqual(ds.round(stack.MRSS.sigma, 6), 0.059417)

    def test_SixSigma(self):
        self.assertEqual(ds.round(stack.items[0].C_p), 2)
        self.assertEqual(ds.round(stack.items[0].k), 0.25)
        self.assertEqual(ds.round(stack.items[0].C_pk), 1.5)
        self.assertEqual(ds.round(stack.items[0].mu_eff), 208.0)
        self.assertEqual(ds.round(stack.items[0].sigma_eff), 0.008)

        self.assertEqual(ds.round(stack.SixSigma(at=4.5).mu), 0.4)
        self.assertEqual(ds.round(stack.SixSigma(at=4.5).nominal), 0.4)
        self.assertEqual(ds.round(stack.SixSigma(at=4.5).tolerance.T / 2), 0.26433)
        self.assertEqual(ds.round(stack.SixSigma(at=4.5).sigma, 6), 0.05874)
        self.assertEqual(ds.round(stack.SixSigma(at=4.5).Z_min), 0.13567)
        self.assertEqual(ds.round(stack.SixSigma(at=4.5).Z_max), 0.66433)

    def test_sixsigma_assembly(self):
        eval = stack.SixSigma(at=4.5)
        assy = ds.Assembly("assy", "", dim=eval, LL=0.05, UL=0.8, process_sigma=4.5)

        self.assertEqual(ds.round(assy.C_p), 2.12804)
        self.assertEqual(ds.round(assy.C_pk), 1.98617)
        self.assertEqual(ds.round(assy.R, 1), 0.0)


if __name__ == "__main__":
    unittest.main()
