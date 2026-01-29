import math
import unittest

import dimstack as ds

# this test against some work previously done with sensitivity factors

m0 = ds.dim.Basic(
    nom=0.03377,
    tol=ds.tol.Bilateral.symmetric(0.0035),
    name="Ap zigzag corn to Ap edge",
    desc="",
)
m1 = ds.dim.Basic(
    nom=0,
    tol=ds.tol.Bilateral.symmetric(0.012 / 2),
    name="Ap edge to Ap Center",
    desc="",
)
m2 = ds.dim.Basic(
    nom=0,
    tol=ds.tol.Bilateral.symmetric(0.015 / 2),
    name="Ap Center to AP Datum L",
    desc="",
)
m3 = ds.dim.Basic(
    nom=0,
    tol=ds.tol.Bilateral.symmetric(0.030 / 2),
    name="AP Datum L to IP Seed Mtl Reticle Fid",
    desc="",
)
m4 = ds.dim.Basic(
    nom=0,
    tol=ds.tol.Bilateral.symmetric(0.010 / 2),
    name="IP Seed Mtl Reticle Fid to IP Seed Mtl Bond Fid",
    desc="",
)
m5 = ds.dim.Basic(
    nom=0,
    tol=ds.tol.Bilateral.symmetric(0.050 / 2),
    name="IP Seed Mtl Bond Fid to CMOS Bond Fid",
    desc="",
)
m6 = ds.dim.Basic(
    nom=0,
    tol=ds.tol.Bilateral.symmetric(0.0),
    name="CMOS Bond Fid to PoM",
    desc="(CMOS feature-feature too small to care)",
)
m7 = ds.dim.Basic(
    nom=0.096,
    tol=ds.tol.Bilateral.symmetric(0.0),
    name="PoM to Arr",
    desc="(CMOS feature-feature too small to care)",
)


a_mmax = math.tan(math.radians(6.38))  # MMax Cone Angle
mz1 = ds.dim.Basic(
    nom=0.006,
    tol=ds.tol.Bilateral.symmetric(0.002),
    a=a_mmax,
    name="CMOS to IP bondline",
    desc="Metal Bond",
)
mz2 = ds.dim.Basic(
    nom=0.3,
    tol=ds.tol.Bilateral.symmetric(0.025),
    a=a_mmax,
    name="IP bottom to IP Top",
    desc="",
)
mz3 = ds.dim.Basic(
    nom=0.001,
    tol=ds.tol.Bilateral.symmetric(0.0001),
    a=a_mmax,
    name="IP to Coated Glass",
    desc="Fusion Bond",
)

items = [m0, m1, m2, m3, m4, m5, m6, m7, mz1, mz2, mz3]
stack = ds.Stack(name="Ap to Array", dims=items)
closed = ds.calc.WC(stack)


class ApArr(unittest.TestCase):
    def test_result(self):
        self.assertAlmostEqual(closed.nominal, 0.16408, 4)
        self.assertAlmostEqual(closed.tolerance.upper, 0.064985046, 4)
        self.assertAlmostEqual(closed.tolerance.lower, -0.064985046, 4)
