import unittest
from copy import deepcopy

import dimstack

# this test is a copy Dimensioning and Tolerancing Handbook by McGraw Hill, Chapter 9


class McGrawHill_1(unittest.TestCase):
    m1 = dimstack.dim.Basic(
        nom=-0.375,
        tol=dimstack.tolerance.UnequalBilateral(0, -0.031),
        name="A",
        desc="Screw thread length",
    )
    m2 = dimstack.dim.Basic(
        nom=0.032,
        tol=dimstack.tolerance.SymmetricBilateral(0.002),
        name="B",
        desc="Washer Length",
    )
    m3 = dimstack.dim.Basic(
        nom=0.06,
        tol=dimstack.tolerance.SymmetricBilateral(0.003),
        name="C",
        desc="Inner bearing cap turned length",
    )
    m4 = dimstack.dim.Basic(
        nom=0.438,
        tol=dimstack.tolerance.UnequalBilateral(0, -0.015),
        name="D",
        desc="Bearing length",
    )
    m5 = dimstack.dim.Basic(
        nom=0.12,
        tol=dimstack.tolerance.SymmetricBilateral(0.005),
        name="E",
        desc="Spacer turned length",
    )
    m6 = dimstack.dim.Basic(
        nom=1.5,
        tol=dimstack.tolerance.UnequalBilateral(0.01, -0.004),
        name="F",
        desc="Rotor length",
    )
    m7 = deepcopy(m5)
    m7.name = "G"
    m8 = deepcopy(m4)
    m8.name = "H"
    m9 = dimstack.dim.Basic(
        nom=0.450,
        tol=dimstack.tolerance.SymmetricBilateral(0.007),
        name="I",
        desc="Pulley casting length",
    )
    m10 = dimstack.dim.Basic(
        nom=-3.019,
        tol=dimstack.tolerance.UnequalBilateral(0.012, 0),
        name="J",
        desc="Shaft turned length",
    )
    m11 = dimstack.dim.Basic(
        nom=0.3,
        tol=dimstack.tolerance.SymmetricBilateral(0.03),
        name="K",
        desc="Tapped hole depth",
    )
    dims = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11]

    stack = dimstack.dim.Stack(name="stacks on stacks", dims=dims)

    def test_WC(self):
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.WC.nominal), 0.0615)
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.WC.tolerance.T / 2), 0.0955)
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.WC.Z_min, 5), -0.034)
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.WC.Z_max, 3), 0.157)

    def test_RSS(self):
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.RSS.nominal), 0.0615)
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.RSS.tolerance.T / 2), 0.03808)
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.RSS.Z_min), 0.02342)
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.RSS.Z_max), 0.09958)

    def test_MRSS(self):
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.MRSS.nominal), 0.0615)
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.MRSS.tolerance.T / 2), 0.05047)
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.MRSS.Z_min, 3), 0.011)
        self.assertEqual(dimstack.utils.nround(McGrawHill_1.stack.MRSS.Z_max, 3), 0.112)


# this test is a copy Dimensioning and Tolerancing Handbook by McGraw Hill, Chaper 12-12


class McGrawHill_2(unittest.TestCase):
    m1 = dimstack.dim.Basic(nom=0.875, tol=dimstack.tolerance.SymmetricBilateral(0.010), a=-0.5146, name="A")
    m2 = dimstack.dim.Basic(nom=1.625, tol=dimstack.tolerance.SymmetricBilateral(0.020), a=0.1567, name="B")
    m3 = dimstack.dim.Basic(nom=1.700, tol=dimstack.tolerance.SymmetricBilateral(0.012), a=0.4180, name="C")
    m4 = dimstack.dim.Basic(nom=0.875, tol=dimstack.tolerance.SymmetricBilateral(0.010), a=-1.000, name="D")
    m5 = dimstack.dim.Basic(nom=2.625, tol=dimstack.tolerance.SymmetricBilateral(0.020), a=-0.0540, name="E")
    m6 = dimstack.dim.Basic(nom=7.875, tol=dimstack.tolerance.SymmetricBilateral(0.030), a=0.4372, name="F")
    m7 = dimstack.dim.Basic(nom=4.125, tol=dimstack.tolerance.SymmetricBilateral(0.010), a=1.000, name="G")
    m8 = dimstack.dim.Basic(nom=1.125, tol=dimstack.tolerance.SymmetricBilateral(0.020), a=-0.9956, name="H")
    m9 = dimstack.dim.Basic(nom=3.625, tol=dimstack.tolerance.SymmetricBilateral(0.015), a=-0.7530, name="J")
    m10 = dimstack.dim.Basic(nom=5.125, tol=dimstack.tolerance.SymmetricBilateral(0.020), a=-0.4006, name="K")
    m11 = dimstack.dim.Basic(nom=1.000, tol=dimstack.tolerance.SymmetricBilateral(0.010), a=-1.0914, name="M")
    dims = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11]

    stack = dimstack.dim.Stack(name="stacks on stacks", dims=dims)

    def test_WC(self):
        self.assertEqual(dimstack.utils.nround(McGrawHill_2.stack.WC.nominal), 0.07201)  # 0.0719
        self.assertEqual(dimstack.utils.nround(McGrawHill_2.stack.WC.tolerance.T / 2), 0.09763)  # 0.0967
        self.assertEqual(dimstack.utils.nround(McGrawHill_2.stack.WC.Z_min, 5), -0.02561)  # -0.0248


if __name__ == "__main__":
    unittest.main()
