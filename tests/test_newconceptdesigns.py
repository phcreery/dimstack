import unittest

import dimstack

# this test is a copy of "My First Stackup" in newconceptzdesign http://www.newconceptzdesign.com/tutorial/Tutorial-My_first_stackup.html

m1 = dimstack.dim.Statistical(
    nom=-0.3190,
    tol=dimstack.tolerance.SymmetricBilateral(0.0050),
    target_process_sigma=6,
    name="PN16",
    desc="Mounting face to rt. end",
)
m1.assume_normal_dist()
m2 = dimstack.dim.Statistical(
    nom=10.4860,
    tol=dimstack.tolerance.SymmetricBilateral(0.0100),
    target_process_sigma=6,
    name="PN07",
    desc="Overall width",
)
m2.assume_normal_dist()
m3 = dimstack.dim.Statistical(
    nom=-0.3190, tol=dimstack.tolerance.SymmetricBilateral(0.0050), target_process_sigma=6, name="PN16", desc="Mounting face to rt. end"
)
m3.assume_normal_dist()
dims = [m1, m2, m3]

stack = dimstack.dim.Stack(name="PN16/NJ210E - gap between cover and bearing (shaft pushed rt.)", dims=dims)


class MITCalc(unittest.TestCase):
    def test_Closed(self):
        Closed = dimstack.calc.Closed(stack)
        self.assertEqual(dimstack.utils.nround(Closed.nominal), 9.8480)
        self.assertEqual(dimstack.utils.nround(Closed.tolerance.T / 2), 0.0200)
        self.assertEqual(dimstack.utils.nround(Closed.abs_lower), 9.8280)
        self.assertEqual(dimstack.utils.nround(Closed.abs_upper), 9.8680)

    def test_WC(self):
        WC = dimstack.calc.WC(stack)
        self.assertEqual(dimstack.utils.nround(WC.nominal), 9.8480)
        self.assertEqual(dimstack.utils.nround(WC.tolerance.T / 2), 0.0200)
        self.assertEqual(dimstack.utils.nround(WC.abs_lower), 9.8280)
        self.assertEqual(dimstack.utils.nround(WC.abs_upper), 9.8680)

    def test_SixSigma(self):
        SixSigma = dimstack.calc.SixSigma(stack, at=6)
        self.assertEqual(dimstack.utils.nround(SixSigma.nominal), 9.8480)
        self.assertEqual(dimstack.utils.nround(SixSigma.nominal), 9.8480)
        self.assertEqual(dimstack.utils.nround(SixSigma.tolerance.T / 2, 4), 0.0122)
        self.assertEqual(dimstack.utils.nround(SixSigma.distribution.stdev * 2, 5), 0.00408)  # times 2 !?!?
        self.assertEqual(dimstack.utils.nround(SixSigma.abs_lower, 4), 9.8358)
        self.assertEqual(dimstack.utils.nround(SixSigma.abs_upper, 4), 9.8602)

    # def test_SixSigma_assembly(self):
    #     dim = stack.SixSigma(at=4.5)
    #     assy = dimstack.dim.Assembly("assy", "", dim=dim, LL=0.05, UL=0.8, target_process_sigma=4.5)

    #     self.assertEqual(dimstack.utils.nround(assy.C_p), 2.12804)
    #     self.assertEqual(dimstack.utils.nround(assy.C_pk), 1.98617)
    #     self.assertEqual(dimstack.utils.nround(assy.R, 1), 0.0)


if __name__ == "__main__":
    # stack.show()
    # stack.WC.show()
    # stack.SixSigma(at=6).show()
    # stack.SixSigma(at=3).show()
    unittest.main()
