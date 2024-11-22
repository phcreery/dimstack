import dimstack as ds

# ds.display.mode("text")
ds.display.mode("rich")

# k = 0.25
# target_process_sigma = 6
# stdev = 0.036 / target_process_sigma

# dim = ds.dim.Basic(
#     nom=208,
#     tol=ds.tol.SymmetricBilateral(0.036),
#     name="a",
#     desc="Shaft",
# )

# dim.show()

# stack = ds.BasicStack(name="stacks on stacks", dims=[dim, dim])
# stack.show()

# m1 = ds.dim.Reviewed(
#     dim=dim,
#     distribution=ds.dist.Normal(208 + k * target_process_sigma * stdev, stdev),
#     target_process_sigma=target_process_sigma,
# )

# m1.show()
# stack = ds.ReviewedStack(name="stacks on stacks", dims=[m1, m1])
# stack.show()

dim = ds.dim.Basic(
    nom=-2,
    # tol=ds.tol.SymmetricBilateral(1),
    tol=ds.tol.Bilateral(0.1, -0.2),
    name="a",
    desc="Shaft",
)
dim.show()
