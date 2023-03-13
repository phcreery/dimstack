import dimstack.display
import dimstack.tolerance
import dimstack.eval
from copy import deepcopy

# import reference.stackups.stackups as stackups

SymmetricBilateral = dimstack.tolerance.SymmetricBilateral
UnequalBilateral = dimstack.tolerance.UnequalBilateral

dimstack.display.display_mode("text")

# stacks = stackups.Stacks()
# stacks.title("Example stacks, i.e. an example for stackups.py")
# stacks.append(stackups.Stack())
# stacks[1].append(-0.3190, 0.0050, "PN16", "Mounting face to rt. end")
# stacks[1].append(10.4860, 0.0100, "PN07", "Overall width")
# stacks[1].append(-0.3190, 0.0050, "PN16", "Mounting face to rt. end")
# print(stacks[1].stack[0]["j"])
# print(f"RSS: {(0.0050**2 + 0.0100**2 + 0.0050**2)**0.5}")

# m1 = dimstack.tolerance.BasicDimension(
#     nom=-0.3190,
#     tol=SymmetricBilateral(0.0050),
#     name="PN16",
#     desc="Mounting face to rt. end",
# )
# m2 = dimstack.tolerance.BasicDimension(
#     nom=10.4860, tol=SymmetricBilateral(0.0100), name="PN07", desc="Overall width"
# )
# m3 = dimstack.tolerance.BasicDimension(
#     nom=-0.3190,
#     tol=SymmetricBilateral(0.0050),
#     name="PN16",
#     desc="Mounting face to rt. end",
# )
# items = [m1, m2, m3]

# m1 = dimstack.tolerance.BasicDimension(
#     nom=5, tol=SymmetricBilateral(0.1), name="a", desc="a"
# )
# m2 = dimstack.tolerance.BasicDimension(
#     nom=-10, tol=SymmetricBilateral(0.1), name="b", desc="b"
# )
# m3 = dimstack.tolerance.BasicDimension(
#     nom=5, tol=SymmetricBilateral(0.1), name="c", desc="c"
# )
# m4 = dimstack.tolerance.BasicDimension(
#     nom=1, tol=UnequalBilateral(0.100, 0.0000), name="t", desc="t"
# )
# items = [m1, m2, m3, m4]


m1 = dimstack.eval.StatisticalDimension(
    nom=208,
    tol=SymmetricBilateral(0.036),
    process_sigma=6,
    k=0.25,
    name="a",
    desc="Shaft",
)
m2 = dimstack.eval.StatisticalDimension(
    nom=-1.75,
    tol=UnequalBilateral(0, 0.06),
    process_sigma=3,
    name="b",
    desc="Retainer ring",
)
m3 = dimstack.eval.StatisticalDimension(nom=-23, tol=UnequalBilateral(0, 0.12), process_sigma=3, name="c", desc="Bearing")
m4 = dimstack.eval.StatisticalDimension(
    nom=20,
    tol=SymmetricBilateral(0.026),
    process_sigma=3,
    name="d",
    desc="Bearing Sleeve",
)
m5 = dimstack.eval.StatisticalDimension(nom=-200, tol=SymmetricBilateral(0.145), process_sigma=3, name="e", desc="Case")
m6 = dimstack.eval.BasicDimension(
    nom=20,
    tol=SymmetricBilateral(0.026),
    # process_sigma=3,
    name="f",
    desc="Bearing Sleeve",
)
m7 = dimstack.eval.StatisticalDimension(nom=-23, tol=UnequalBilateral(0, 0.12), process_sigma=3, name="g", desc="Bearing")
items = [m1, m2, m3, m4, m5, m6, m7]

# m1 = dimstack.eval.BasicDimension(
#     nom=-0.375,
#     tol=dimstack.tolerance.UnequalBilateral(0, 0.031),
#     name="A",
#     desc="Screw thread length",
# )
# m2 = dimstack.eval.BasicDimension(
#     nom=0.032,
#     tol=dimstack.tolerance.SymmetricBilateral(0.002),
#     name="B",
#     desc="Washer Length",
# )
# m3 = dimstack.eval.BasicDimension(
#     nom=0.06,
#     tol=dimstack.tolerance.SymmetricBilateral(0.003),
#     name="C",
#     desc="Inner bearing cap turned length",
# )
# m4 = dimstack.eval.BasicDimension(
#     nom=0.438,
#     tol=dimstack.tolerance.UnequalBilateral(0, 0.015),
#     name="D",
#     desc="Bearing length",
# )
# m5 = dimstack.eval.BasicDimension(
#     nom=0.12,
#     tol=dimstack.tolerance.SymmetricBilateral(0.005),
#     name="E",
#     desc="Spacer turned length",
# )
# m6 = dimstack.eval.BasicDimension(
#     nom=1.5,
#     tol=dimstack.tolerance.UnequalBilateral(0.01, 0.004),
#     name="F",
#     desc="Rotor length",
# )
# m7 = deepcopy(m5)
# m7.name = "G"
# m8 = deepcopy(m4)
# m8.name = "H"
# m9 = dimstack.eval.BasicDimension(
#     nom=0.450,
#     tol=dimstack.tolerance.SymmetricBilateral(0.007),
#     name="I",
#     desc="Pulley casting length",
# )
# m10 = dimstack.eval.BasicDimension(
#     nom=-3.019,
#     tol=dimstack.tolerance.UnequalBilateral(0.012, 0),
#     name="J",
#     desc="Shaft turned length",
# )
# m11 = dimstack.eval.BasicDimension(
#     nom=0.3,
#     tol=dimstack.tolerance.SymmetricBilateral(0.03),
#     name="K",
#     desc="Tapped hole depth",
# )
# items = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11]

# stack = dimstack.eval.Stack(title="stacks on stacks", items=items)

stack = dimstack.eval.Stack(title="stacks on stacks", items=items)

stack.show()
stack.Closed.show()
stack.WC.show()

eval = stack.RSS
eval.show()

stack.MRSS.show()

eval = stack.SixSigma(at=4.5)
eval.show()

assy = dimstack.eval.Assembly("assy", "", dim=eval, LL=0.05, UL=0.8, process_sigma=4.5)
assy.show()
