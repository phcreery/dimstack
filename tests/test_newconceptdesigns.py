import unittest
import dimstack

# this test is a copy of "My First Stackup" in newconceptzdesign http://www.newconceptzdesign.com/tutorial/Tutorial-My_first_stackup.html

m1 = dimstack.eval.StatisticalDimension(
    nom=-0.3190,
    tol=dimstack.tolerance.SymmetricBilateral(0.0050),
    process_sigma=6,
    name="PN16",
    desc="Mounting face to rt. end",
)
m2 = dimstack.eval.StatisticalDimension(
    nom=10.4860,
    tol=dimstack.tolerance.SymmetricBilateral(0.0100),
    process_sigma=6,
    name="PN07",
    desc="Overall width",
)
m3 = dimstack.eval.StatisticalDimension(
    nom=-0.3190, tol=dimstack.tolerance.SymmetricBilateral(0.0050), process_sigma=6, name="PN16", desc="Mounting face to rt. end"
)
items = [m1, m2, m3]

stack = dimstack.eval.Stack(title="PN16/NJ210E - gap between cover and bearing (shaft pushed rt.)", items=items)


class MITCalc(unittest.TestCase):
    def test_Closed(self):
        self.assertEqual(dimstack.utils.nround(stack.Closed.nominal), 9.8480)
        self.assertEqual(dimstack.utils.nround(stack.Closed.tolerance.T / 2), 0.0200)
        self.assertEqual(dimstack.utils.nround(stack.Closed.Z_min), 9.8280)
        self.assertEqual(dimstack.utils.nround(stack.Closed.Z_max), 9.8680)

    def test_WC(self):
        self.assertEqual(dimstack.utils.nround(stack.WC.nominal), 9.8480)
        self.assertEqual(dimstack.utils.nround(stack.WC.tolerance.T / 2), 0.0200)
        self.assertEqual(dimstack.utils.nround(stack.WC.Z_min), 9.8280)
        self.assertEqual(dimstack.utils.nround(stack.WC.Z_max), 9.8680)

    def test_SixSigma(self):
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=6).mean), 9.8480)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=6).nominal), 9.8480)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=6).tolerance.T / 2, 4), 0.0122)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=6).stdev * 2, 5), 0.00408)  # times 2 !?!?
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=6).Z_min, 4), 9.8358)
        self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=6).Z_max, 4), 9.8602)

    # def test_SixSigma_assembly(self):
    #     eval = stack.SixSigma(at=4.5)
    #     assy = dimstack.eval.Assembly("assy", "", dim=eval, LL=0.05, UL=0.8, process_sigma=4.5)

    #     self.assertEqual(dimstack.utils.nround(assy.C_p), 2.12804)
    #     self.assertEqual(dimstack.utils.nround(assy.C_pk), 1.98617)
    #     self.assertEqual(dimstack.utils.nround(assy.R, 1), 0.0)


if __name__ == "__main__":
    # stack.show()
    # stack.WC.show()
    # stack.SixSigma(at=6).show()
    # stack.SixSigma(at=3).show()
    unittest.main()
