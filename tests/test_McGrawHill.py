import unittest
from copy import deepcopy

import dimstack.display
import dimstack.tolerance
import dimstack.eval
import dimstack.utils

# this test is a copy Dimensioning and Tolerancing Handbook by McGraw Hill, Chaper 9

m1 = dimstack.eval.BasicDimension(
    nom=-0.375,
    tol=dimstack.tolerance.UnequalBilateral(0, 0.031),
    name="A",
    desc="Screw thread length",
)
m2 = dimstack.eval.BasicDimension(
    nom=0.032,
    tol=dimstack.tolerance.SymmetricBilateral(0.002),
    name="B",
    desc="Washer Length",
)
m3 = dimstack.eval.BasicDimension(
    nom=0.06,
    tol=dimstack.tolerance.SymmetricBilateral(0.003),
    name="C",
    desc="Inner bearing cap turned length",
)
m4 = dimstack.eval.BasicDimension(
    nom=0.438,
    tol=dimstack.tolerance.UnequalBilateral(0, 0.015),
    name="D",
    desc="Bearing length",
)
m5 = dimstack.eval.BasicDimension(
    nom=0.12,
    tol=dimstack.tolerance.SymmetricBilateral(0.005),
    name="E",
    desc="Spacer turned length",
)
m6 = dimstack.eval.BasicDimension(
    nom=1.5,
    tol=dimstack.tolerance.UnequalBilateral(0.01, 0.004),
    name="F",
    desc="Rotor length",
)
m7 = deepcopy(m5)
m7.name = "G"
m8 = deepcopy(m4)
m8.name = "H"
m9 = dimstack.eval.BasicDimension(
    nom=0.450,
    tol=dimstack.tolerance.SymmetricBilateral(0.007),
    name="I",
    desc="Pulley casting length",
)
m10 = dimstack.eval.BasicDimension(
    nom=-3.019,
    tol=dimstack.tolerance.UnequalBilateral(0.012, 0),
    name="J",
    desc="Shaft turned length",
)
m11 = dimstack.eval.BasicDimension(
    nom=0.3,
    tol=dimstack.tolerance.SymmetricBilateral(0.03),
    name="K",
    desc="Tapped hole depth",
)
items = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11]

stack = dimstack.eval.Stack(title="stacks on stacks", items=items)


class McGrawHill(unittest.TestCase):
    # def test_input(self):
    #     self.assertEqual(len(stack.items), 7)
    #     self.assertEqual(stack.items[0].nominal, 208)
    #     self.assertEqual(stack.items[0].tolerance.upper, 0.036)
    #     self.assertEqual(stack.items[0].tolerance.lower, 0.036)

    # def test_Closed(self):
    # self.assertEqual(dimstack.utils.nround(stack.Closed.nominal), 0.25)
    # self.assertEqual(dimstack.utils.nround(stack.Closed.tolerance.upper), 0.533)
    # self.assertEqual(dimstack.utils.nround(stack.Closed.tolerance.lower), 0.233)

    def test_WC(self):
        self.assertEqual(dimstack.utils.nround(stack.WC.mu), 0.0615)
        self.assertEqual(dimstack.utils.nround(stack.WC.tolerance.T / 2), 0.0955)
        self.assertEqual(dimstack.utils.nround(stack.WC.Z_min, 5), -0.034)
        self.assertEqual(dimstack.utils.nround(stack.WC.Z_max, 3), 0.157)

    def test_RSS(self):
        self.assertEqual(dimstack.utils.nround(stack.RSS.mu), 0.0615)
        self.assertEqual(dimstack.utils.nround(stack.RSS.tolerance.T / 2, 3), 0.038)  # 0.0381
        self.assertEqual(dimstack.utils.nround(stack.RSS.Z_min), 0.02395)  # 0.0234
        self.assertEqual(dimstack.utils.nround(stack.RSS.Z_max), 0.09905)  # 0.0996
        # self.assertEqual(dimstack.utils.nround(stack.RSS.sigma, 6), 0.059417)

    # def test_RSS_assembly(self):
    #     eval = stack.RSS
    #     assy = dimstack.eval.Assembly("assy", "", dim=eval, LL=0.05, UL=0.8, process_sigma=4.5)

    #     self.assertEqual(dimstack.utils.nround(assy.R, 1), 0.0)

    def test_MRSS(self):
        self.assertEqual(dimstack.utils.nround(stack.MRSS.mu), 0.0615)
        self.assertEqual(dimstack.utils.nround(stack.MRSS.tolerance.T / 2), 0.04919)  # 0.0505
        self.assertEqual(dimstack.utils.nround(stack.MRSS.Z_min, 3), 0.012)  # 0.0110
        self.assertEqual(dimstack.utils.nround(stack.MRSS.Z_max, 3), 0.111)  # 0.1120

    # def test_SixSigma(self):
    #     self.assertEqual(dimstack.utils.nround(stack.items[0].C_p), 2)
    #     self.assertEqual(dimstack.utils.nround(stack.items[0].k), 0.25)
    #     self.assertEqual(dimstack.utils.nround(stack.items[0].C_pk), 1.5)
    #     self.assertEqual(dimstack.utils.nround(stack.items[0].mu_eff), 208.0)
    #     self.assertEqual(dimstack.utils.nround(stack.items[0].sigma_eff), 0.008)

    #     self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).mu), 0.4)
    #     self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).nominal), 0.4)
    #     self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).tolerance.T / 2), 0.26433)
    #     self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).sigma, 6), 0.05874)
    #     self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).Z_min), 0.13567)
    #     self.assertEqual(dimstack.utils.nround(stack.SixSigma(at=4.5).Z_max), 0.66433)

    # def test_SixSigma_assembly(self):
    #     eval = stack.SixSigma(at=4.5)
    #     assy = dimstack.eval.Assembly("assy", "", dim=eval, LL=0.05, UL=0.8, process_sigma=4.5)

    #     self.assertEqual(dimstack.utils.nround(assy.C_p), 2.12804)
    #     self.assertEqual(dimstack.utils.nround(assy.C_pk), 1.98617)
    #     self.assertEqual(dimstack.utils.nround(assy.R, 1), 0.0)


if __name__ == "__main__":
    unittest.main()
