import dimstack.tolerance
import reference.stackups.stackups as stackups

Unilateral = dimstack.tolerance.Unilateral
Bilateral = dimstack.tolerance.Bilateral

# dimstack.test()

stacks = stackups.Stacks()
stacks.title("Example stacks, i.e. an example for stackups.py")
stacks.append(stackups.Stack())
stacks[1].append(-0.3190, 0.0050, "PN16", "Mounting face to rt. end")
stacks[1].append(10.4860, 0.0100, "PN07", "Overall width")
stacks[1].append(-0.3190, 0.0050, "PN16", "Mounting face to rt. end")
# print(stacks[1].stack[0]["j"])
# print(f"RSS: {(0.0050**2 + 0.0100**2 + 0.0050**2)**0.5}")

# m1 = dimstack.tolerance.Measurement(nom=5, tol=Bilateral(0.1), name="a", desc="a")
# m2 = dimstack.tolerance.Measurement(nom=-10, tol=Bilateral(0.1), name="b", desc="b")
# m3 = dimstack.tolerance.Measurement(nom=5, tol=Bilateral(0.1), name="c", desc="c")
# m4 = dimstack.tolerance.Measurement(
#     nom=1, tol=Unilateral(0.100, 0.0000), name="t", desc="t"
# )
# items = [m1, m2, m3, m4]

m1 = dimstack.tolerance.Measurement(
    nom=208, tol=Bilateral(0.036), process_sigma=6, k=0.25, name="a", desc="Shaft"
)
m2 = dimstack.tolerance.Measurement(
    nom=-1.75, tol=Unilateral(0, 0.06), process_sigma=3, name="b", desc="Retainer ring"
)
m3 = dimstack.tolerance.Measurement(
    nom=-23, tol=Unilateral(0, 0.12), process_sigma=3, name="c", desc="Bearing"
)
m4 = dimstack.tolerance.Measurement(
    nom=20, tol=Bilateral(0.026), process_sigma=3, name="d", desc="Bearing Sleeve"
)
m5 = dimstack.tolerance.Measurement(
    nom=-200, tol=Bilateral(0.145), process_sigma=3, name="e", desc="Case"
)
m6 = dimstack.tolerance.Measurement(
    nom=20, tol=Bilateral(0.026), process_sigma=3, name="f", desc="Bearing Sleeve"
)
m7 = dimstack.tolerance.Measurement(
    nom=-23, tol=Unilateral(0, 0.12), process_sigma=3, name="g", desc="Bearing"
)
items = [m1, m2, m3, m4, m5, m6, m7]
stack = dimstack.tolerance.Stack(
    title="Example stacks, i.e. an example for stackups.py", items=items
)
# stack.append(m1)
# stack.append(m2)
# stack.append(m3)
print(stack.df_text())
print(stack.results_text_RSS_simple())
print(stack.results_text_RSS())
