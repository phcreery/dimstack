## Interactive Jupyter Notebook

[Example Notebook](example.html)

## Motor Assembly textbook example, Chapter 9 through 11, Dimensioning and Tolerancing Handbook, McGraw Hill

```python
import dimstack as ds

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
stack.Closed.show()
stack.WC.show()
stack.RSS.show()
stack.MRSS.show()
designed_for = stack.SixSigma(at=4.5)
designed_for.show()

spec = ds.Spec("stack spec", "", dim=designed_for, LL=0.05, UL=0.8)
spec.show()

ds.plot.StackPlot().add(stack).add(stack.RSS).show()
```

Returns:

```
                                   STACK: stacks on stacks
┏━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Name ┃ Desc.          ┃ dir ┃ Nom.  ┃ Tol.           ┃ Sens. (a) ┃ Rel. Bounds        ┃
┡━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ 0  │ a    │ Shaft          │ +   │ 208.0 │ ± 0.036        │ 1         │ [207.964, 208.036] │
│ 1  │ b    │ Retainer ring  │ -   │ 1.75  │ + 0.06 / + 0   │ 1         │ [1.75, 1.81]       │
│ 2  │ c    │ Bearing        │ -   │ 23.0  │ + 0.12 / + 0   │ 1         │ [23, 23.12]        │
│ 3  │ d    │ Bearing Sleeve │ +   │ 20.0  │ ± 0.026        │ 1         │ [19.974, 20.026]   │
│ 4  │ e    │ Case           │ -   │ 200.0 │ ± 0.145        │ 1         │ [199.855, 200.145] │
│ 5  │ f    │ Bearing Sleeve │ +   │ 20.0  │ ± 0.026        │ 1         │ [19.974, 20.026]   │
│ 6  │ g    │ Bearing        │ -   │ 23.0  │ + 0.12 / + 0   │ 1         │ [23, 23.12]        │
└────┴──────┴────────────────┴─────┴───────┴────────────────┴───────────┴────────────────────┘
                                    Dimension: stacks on stacks - Closed Analysis -
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Name                               ┃ Description ┃ dir ┃ Nom. ┃ Tol.              ┃ Sens. (a) ┃ Relative Bounds ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 7  │ stacks on stacks - Closed Analysis │             │ +   │ 0.25 │ + 0.233 / - 0.533 │ 1         │ [-0.283, 0.483] │
└────┴────────────────────────────────────┴─────────────┴─────┴──────┴───────────────────┴───────────┴─────────────────┘
                                   Dimension: stacks on stacks - WC Analysis -
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Name                           ┃ Description ┃ dir ┃ Nom. ┃ Tol.           ┃ Sens. (a) ┃ Relative Bounds ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 8  │ stacks on stacks - WC Analysis │             │ +   │ 0.1  │ ± 0.383        │ 1         │ [-0.283, 0.483] │
└────┴────────────────────────────────┴─────────────┴─────┴──────┴────────────────┴───────────┴─────────────────┘
WARNING:root:Converting Basic Dim. (5: f Bearing Sleeve +20 ± 0.026) to Statistical Dim.
              DIMENSION: stacks on stacks - RSS Analysis - (assuming inputs with Normal Distribution & ± 3σ)
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Desc.                                             ┃ dir ┃ Nom. ┃ Tol.           ┃ Sens. (a) ┃ Rel. Bounds         ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 10 │ (assuming inputs with Normal Distribution & ± 3σ) │ +   │ 0.1  │ ± 0.17825      │ 1         │ [-0.07825, 0.27825] │
└────┴───────────────────────────────────────────────────┴─────┴──────┴────────────────┴───────────┴─────────────────────┘
WARNING:root:Converting Basic Dim. (5: f Bearing Sleeve +20 ± 0.026) to Statistical Dim.
             DIMENSION: stacks on stacks - MRSS Analysis - (assuming inputs with Normal Distribution & ± 3σ)
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Desc.                                             ┃ dir ┃ Nom. ┃ Tol.           ┃ Sens. (a) ┃ Rel. Bounds         ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 12 │ (assuming inputs with Normal Distribution & ± 3σ) │ +   │ 0.1  │ ± 0.24046      │ 1         │ [-0.14046, 0.34046] │
└────┴───────────────────────────────────────────────────┴─────┴──────┴────────────────┴───────────┴─────────────────────┘
WARNING:root:Converting Basic Dim. (5: f Bearing Sleeve +20 ± 0.026) to Statistical Dim.
        DIMENSION: stacks on stacks - '6 Sigma' Analysis - (assuming inputs with Normal Distribution)
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ ID ┃ Desc.                                      ┃ dir ┃ Nom. ┃ Tol.           ┃ Sens. (a) ┃ Rel. Bounds    ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ 14 │ (assuming inputs with Normal Distribution) │ +   │ 0.1  │ ± 0.036        │ 1         │ [0.064, 0.136] │
└────┴────────────────────────────────────────────┴─────┴──────┴────────────────┴───────────┴────────────────┘
                                                     SPEC: stack spec
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Desc. ┃ Dimension                                                    ┃ Median ┃ Spec. Limits ┃ Yield Prob. ┃ Reject PPM ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│       │ 14: stacks on stacks - '6 Sigma' Analysis (assuming inputs   │ 0.425  │ [0.05, 0.8]  │ 99.99999998 │ 0.0        │
│       │ with Normal Distribution) +0.1 ± 0.036 @ ± 4.5σ & k=0.0      │        │              │             │            │
└───────┴──────────────────────────────────────────────────────────────┴────────┴──────────────┴─────────────┴────────────┘
```
