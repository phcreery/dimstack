import dimstack as ds

# ds.display.mode("text")
ds.display.mode("rich")

k = 0.25
target_process_sigma = 6
stdev = 0.036 / target_process_sigma
m1 = ds.dim.Statistical(
    nom=208,
    tol=ds.tol.SymmetricBilateral(0.036),
    distribution=ds.dist.Normal(208 + k * target_process_sigma * stdev, stdev),
    target_process_sigma=target_process_sigma,
    name="a",
    desc="Shaft",
)
m2 = ds.dim.Statistical(
    nom=-1.75,
    tol=ds.tol.UnequalBilateral(0, 0.06),
    target_process_sigma=3,
    name="b",
    desc="Retainer ring",
)
m3 = ds.dim.Statistical(nom=-23, tol=ds.tol.UnequalBilateral(0, 0.12), target_process_sigma=3, name="c", desc="Bearing")
m4 = ds.dim.Statistical(
    nom=20,
    tol=ds.tol.SymmetricBilateral(0.026),
    target_process_sigma=3,
    name="d",
    desc="Bearing Sleeve",
)
m5 = ds.dim.Statistical(nom=-200, tol=ds.tol.SymmetricBilateral(0.145), target_process_sigma=3, name="e", desc="Case")
m6 = ds.dim.Basic(
    nom=20,
    tol=ds.tol.SymmetricBilateral(0.026),
    # target_process_sigma=3,
    name="f",
    desc="Bearing Sleeve",
)
m7 = ds.dim.Statistical(nom=-23, tol=ds.tol.UnequalBilateral(0, 0.12), target_process_sigma=3, name="g", desc="Bearing")
items = [m1, m2, m3, m4, m5, m6, m7]

stack = ds.Stack(name="stacks on stacks", dims=items)

stack.show()
ds.calc.Closed(stack).show()
ds.calc.WC(stack).show()
ds.calc.RSS(stack).show()
ds.calc.MRSS(stack).show()
designed_for = ds.calc.SixSigma(stack, at=4.5)
designed_for.show()

spec = ds.Spec("stack spec", "", dim=designed_for, LL=0.05, UL=0.8)
spec.show()

# ds.plot.StackPlot().add(stack).add(stack.RSS).show()
