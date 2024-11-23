import dimstack as ds

# ds.display.mode("text")
ds.display.mode("rich")

k = 0.25
target_process_sigma = 3
stdev = 0.036 / target_process_sigma
m1 = ds.dim.Reviewed(
    dim=ds.dim.Basic(
        nom=208,
        tol=ds.tol.SymmetricBilateral(0.036),
        name="a",
        desc="Shaft",
    ),
    distribution=ds.dist.Normal(208 + k * target_process_sigma * stdev, stdev),
    target_process_sigma=target_process_sigma,
)
m2 = ds.dim.Reviewed(
    dim=ds.dim.Basic(
        nom=-1.75,
        tol=ds.tol.UnequalBilateral(0, 0.06),
        name="b",
        desc="Retainer ring",
    ),
    target_process_sigma=3,
)
m3 = ds.dim.Reviewed(
    dim=ds.dim.Basic(
        nom=-23,
        tol=ds.tol.UnequalBilateral(0, 0.12),
        name="c",
        desc="Bearing",
    ),
    target_process_sigma=3,
)
m4 = ds.dim.Reviewed(
    dim=ds.dim.Basic(
        nom=20,
        tol=ds.tol.SymmetricBilateral(0.026),
        name="d",
        desc="Bearing Sleeve",
    ),
    target_process_sigma=3,
)
m5 = ds.dim.Reviewed(
    dim=ds.dim.Basic(
        nom=-200,
        tol=ds.tol.SymmetricBilateral(0.145),
        name="e",
        desc="Case",
    ),
    target_process_sigma=3,
)
m6 = ds.dim.Basic(
    nom=20,
    tol=ds.tol.SymmetricBilateral(0.026),
    name="f",
    desc="Bearing Sleeve",
)
m7 = ds.dim.Reviewed(
    dim=ds.dim.Basic(
        nom=-23,
        tol=ds.tol.UnequalBilateral(0, 0.12),
        name="g",
        desc="Bearing",
    ),
    target_process_sigma=3,
)
items = [m1, m2, m3, m4, m5, m7]

stack = ds.ReviewedStack(name="stacks on stacks", dims=items)

stack.to_basic_stack().show()
stack.show()

ds.calc.Closed(stack).show()
ds.calc.WC(stack).show()
ds.calc.RSS(stack).show()
ds.calc.MRSS(stack).show()
designed_for = ds.calc.SixSigma(stack, at=4.5)
designed_for.show()

spec = ds.Requirement("stack spec", "", distribution=designed_for.distribution, LL=0.05, UL=0.8)
spec.show()

ds.plot.StackPlot().add(stack).add(ds.calc.RSS(stack)).show()
