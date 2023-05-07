import dimstack
from copy import deepcopy

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

stack.show()
stack.Closed.show()
stack.WC.show()
stack.RSS.show()
stack.MRSS.show()
stack.SixSigma(at=4.5).show()
