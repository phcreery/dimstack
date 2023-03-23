import dimstack

SymmetricBilateral = dimstack.tolerance.SymmetricBilateral
UnequalBilateral = dimstack.tolerance.UnequalBilateral

dimstack.display.display_mode("text")

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

stack = dimstack.eval.Stack(title="stacks on stacks", items=items)

stack.show()
stack.Closed.show()
stack.WC.show()
stack.RSS.show()
stack.MRSS.show()
stack.SixSigma(at=4.5).show()

spec = dimstack.eval.Spec("stack spec", "", dim=stack.SixSigma(at=4.5), LL=0.05, UL=0.8)
spec.show()
