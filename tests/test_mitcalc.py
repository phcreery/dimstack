import unittest
import dimstack.tolerance as ds

# this test is a copy of MITCalc User Interface diagram

m1 = ds.Dimension(
    nom=208,
    tol=ds.SymmetricBilateral(0.036),
    process_sigma=6,
    k=0.25,
    name="a",
    desc="Shaft",
)
m2 = ds.Dimension(
    nom=-1.75,
    tol=ds.UnequalBilateral(0, 0.06),
    process_sigma=3,
    name="b",
    desc="Retainer ring",
)
m3 = ds.Dimension(
    nom=-23, tol=ds.UnequalBilateral(0, 0.12), process_sigma=3, name="c", desc="Bearing"
)
m4 = ds.Dimension(
    nom=20,
    tol=ds.SymmetricBilateral(0.026),
    process_sigma=3,
    name="d",
    desc="Bearing Sleeve",
)
m5 = ds.Dimension(
    nom=-200, tol=ds.SymmetricBilateral(0.145), process_sigma=3, name="e", desc="Case"
)
m6 = ds.Dimension(
    nom=20,
    tol=ds.SymmetricBilateral(0.026),
    process_sigma=3,
    name="f",
    desc="Bearing Sleeve",
)
m7 = ds.Dimension(
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

    def test_closed(self):
        self.assertEqual(ds.round(stack.Closed.nominal), 0.25)
        self.assertEqual(ds.round(stack.Closed.tolerance.upper), 0.533)
        self.assertEqual(ds.round(stack.Closed.tolerance.lower), 0.233)
        # self.assertEqual(ds.round(stack.RSS.sigma, 6), 0.059417)

    def test_wc(self):
        self.assertEqual(ds.round(stack.WC.mu), 0.4)
        self.assertEqual(ds.round(stack.WC.tolerance.T / 2), 0.383)
        self.assertEqual(ds.round(stack.WC.Z_min), 0.017)
        self.assertEqual(ds.round(stack.WC.Z_max), 0.783)

    def test_RSS(self):
        self.assertEqual(ds.round(stack.RSS.mu), 0.4)
        self.assertEqual(ds.round(stack.RSS.d_g), 0.4)
        self.assertEqual(ds.round(stack.RSS.t_rss), 0.1782)  # 0.176085
        self.assertEqual(ds.round(stack.RSS.t_mrss), 0.2405)  # 0.176085
        # self.assertEqual(ds.round(stack.RSS.sigma, 6), 0.059417)

    def test_sixsigma(self):
        self.assertEqual(ds.round(stack.items[0].C_p), 2)
        self.assertEqual(ds.round(stack.items[0].k), 0.25)
        self.assertEqual(ds.round(stack.items[0].C_pk), 1.5)
        self.assertEqual(ds.round(stack.items[0].mu_eff), 208.0)
        self.assertEqual(ds.round(stack.items[0].sigma_eff), 0.008)

        self.assertEqual(ds.round(stack.SixSigma.mu), 0.4)
        self.assertEqual(ds.round(stack.SixSigma.sigma, 6), 0.05874)
        # self.assertEqual(ds.round(stack.SixSigma.C_p), 2.12804)
        # self.assertEqual(ds.round(stack.SixSigma.C_pk, 6), 1.98617)

    # def test_sixsigma_assembly(self):
    # self.assertEqual(ds.round(stack.Z_min), 0.017)
    # self.assertEqual(ds.round(stack.Z_max), 0.783)


if __name__ == "__main__":
    unittest.main()
