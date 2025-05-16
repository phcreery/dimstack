import dimstack as ds

ds.display.mode(ds.display.DisplayMode.RICH)

k = 0.25
target_process_sigma = 3
std_dev = 0.036 / target_process_sigma
m1 = dim = ds.dim.Basic(
    nom=208,
    tol=ds.tol.Bilateral.symmetric(0.036),
    name="a",
    desc="Shaft",
).review(
    distribution=ds.dist.Normal(208 + k * target_process_sigma * std_dev, std_dev),
)
m2 = dim = (
    ds.dim.Basic(
        nom=-1.75,
        tol=ds.tol.Bilateral.unequal(0, 0.06),
        name="b",
        desc="Retainer ring",
    )
    .review()
    .assume_normal_dist(3)
)

m3 = dim = (
    ds.dim.Basic(
        nom=-23,
        tol=ds.tol.Bilateral.unequal(0, 0.12),
        name="c",
        desc="Bearing",
    )
    .review()
    .assume_normal_dist(3)
)
m4 = dim = (
    ds.dim.Basic(
        nom=20,
        tol=ds.tol.Bilateral.symmetric(0.026),
        name="d",
        desc="Bearing Sleeve",
    )
    .review()
    .assume_normal_dist(3)
)
m5 = dim = (
    ds.dim.Basic(
        nom=-200,
        tol=ds.tol.Bilateral.symmetric(0.145),
        name="e",
        desc="Case",
    )
    .review()
    .assume_normal_dist(3)
)
m6 = (
    ds.dim.Basic(
        nom=20,
        tol=ds.tol.Bilateral.symmetric(0.026),
        name="f",
        desc="Bearing Sleeve",
    )
    .review()
    .assume_normal_dist(3)
)
m7 = dim = ds.dim.Basic(
    nom=-23,
    tol=ds.tol.Bilateral.unequal(0, 0.12),
    name="g",
    desc="Bearing",
).review()
items = [m1, m2, m3, m4, m5, m6, m7]

stack = ds.dim.ReviewedStack(name="stacks on stacks", dims=items)

stack.to_basic_stack().show()
stack.show()

ds.calc.Closed(stack).show()
ds.calc.WC(stack).show()
ds.calc.RSS(stack).show()
ds.calc.MRSS(stack).show()
designed_for = ds.calc.SixSigma(stack, at=4.5)
designed_for.show()

spec = ds.dim.Requirement("stack spec", "", distribution=designed_for.distribution, LL=0.05, UL=0.8)
spec.show()

ds.plot.StackPlot().add(stack).add(ds.calc.RSS(stack)).show()
