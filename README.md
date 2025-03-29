# dimstack

Python library for mechanical engineers to help with statistical tolerancing analysis and design.

https://pypi.org/project/dimstack/

## Example (MIT Calc Demonstration Analysis)

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
ds.calc.Closed(stack).show()
ds.calc.WC(stack).show()
ds.calc.RSS(stack).show()
ds.calc.MRSS(stack).show()
designed_for = ds.calc.SixSigma(stack, at=4.5)
designed_for.show()

spec = ds.Spec("stack spec", "", distribution=designed_for.distribution, LL=0.05, UL=0.8)
spec.show()

ds.plot.StackPlot().add(stack).add(stack.RSS).show()
```

Returns:

```
                                     STACK: stacks on stacks
┏━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Name ┃ Desc.          ┃ ± ┃ Nom.     ┃ Tol.           ┃ Sens. (a) ┃ Abs. Bounds          ┃
┡━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ 0  │ a    │ Shaft          │ + │      208 │ ± 0.036        │ 1         │ [207.964, 208.036]   │
│ 1  │ b    │ Retainer ring  │ - │     1.75 │ + 0.06 / + 0   │ 1         │ [-1.75, -1.69]       │
│ 2  │ c    │ Bearing        │ - │       23 │ + 0.12 / + 0   │ 1         │ [-23, -22.88]        │
│ 3  │ d    │ Bearing Sleeve │ + │       20 │ ± 0.026        │ 1         │ [19.974, 20.026]     │
│ 4  │ e    │ Case           │ - │      200 │ ± 0.145        │ 1         │ [-200.145, -199.855] │
│ 5  │ f    │ Bearing Sleeve │ + │       20 │ ± 0.026        │ 1         │ [19.974, 20.026]     │
│ 6  │ g    │ Bearing        │ - │       23 │ + 0.12 / + 0   │ 1         │ [-23, -22.88]        │
└────┴──────┴────────────────┴───┴──────────┴────────────────┴───────────┴──────────────────────┘
                                DIMENSION: stacks on stacks - Closed Analysis -
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Name                               ┃ Desc. ┃ ± ┃ Nom. ┃ Tol.              ┃ Sens. (a) ┃ Rel. Bounds     ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 7  │ stacks on stacks - Closed Analysis │       │ + │ 0.25 │ + 0.233 / - 0.533 │ 1         │ [-0.283, 0.483] │
└────┴────────────────────────────────────┴───────┴───┴──────┴───────────────────┴───────────┴─────────────────┘
                               DIMENSION: stacks on stacks - WC Analysis -
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Name                           ┃ Desc. ┃ ± ┃ Nom. ┃ Tol.           ┃ Sens. (a) ┃ Rel. Bounds     ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 8  │ stacks on stacks - WC Analysis │       │ + │ 0.1  │ ± 0.383        │ 1         │ [-0.283, 0.483] │
└────┴────────────────────────────────┴───────┴───┴──────┴────────────────┴───────────┴─────────────────┘
WARNING:root:Converting Basic Dim. (5: f Bearing Sleeve +20 ± 0.026) to Statistical Dim.
WARNING:root:Assuming Normal Dist. for 10: stacks on stacks - RSS Analysis (assuming inputs with Normal Dist. & uniform SD) +0.1 ± 0.17825 @ Normal Dist. (μ=0.1, σ=0.05942)
             DIMENSION: stacks on stacks - RSS Analysis - (assuming inputs with Normal Dist. & uniform SD)
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Desc.                                            ┃ ± ┃ Nom. ┃ Tol.           ┃ Sens. (a) ┃ Abs. Bounds         ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 10 │ (assuming inputs with Normal Dist. & uniform SD) │ + │ 0.1  │ ± 0.17825      │ 1         │ [-0.07825, 0.27825] │
└────┴──────────────────────────────────────────────────┴───┴──────┴────────────────┴───────────┴─────────────────────┘
WARNING:root:Converting Basic Dim. (5: f Bearing Sleeve +20 ± 0.026) to Statistical Dim.
WARNING:root:Assuming Normal Dist. for 12: stacks on stacks - MRSS Analysis (assuming inputs with Normal Dist. & uniform SD) +0.1 ± 0.24046 @ Normal Dist. (μ=0.1, σ=0.06383)
            DIMENSION: stacks on stacks - MRSS Analysis - (assuming inputs with Normal Dist. & uniform SD)
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Desc.                                            ┃ ± ┃ Nom. ┃ Tol.           ┃ Sens. (a) ┃ Abs. Bounds         ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 12 │ (assuming inputs with Normal Dist. & uniform SD) │ + │ 0.1  │ ± 0.24046      │ 1         │ [-0.14046, 0.34046] │
└────┴──────────────────────────────────────────────────┴───┴──────┴────────────────┴───────────┴─────────────────────┘
WARNING:root:Assuming Normal Dist. for 1: b Retainer ring -1.75 + 0.06 / + 0 @ Normal Dist. (μ=1.78, σ=0.01)
WARNING:root:Assuming Normal Dist. for 2: c Bearing -23 + 0.12 / + 0 @ Normal Dist. (μ=23.06, σ=0.02)
WARNING:root:Assuming Normal Dist. for 3: d Bearing Sleeve +20 ± 0.026 @ Normal Dist. (μ=20.0, σ=0.00867)
WARNING:root:Assuming Normal Dist. for 4: e Case -200 ± 0.145 @ Normal Dist. (μ=200.0, σ=0.04833)
WARNING:root:Converting Basic Dim. (5: f Bearing Sleeve +20 ± 0.026) to Statistical Dim.
WARNING:root:Assuming Normal Dist. for 13: f Bearing Sleeve +20 ± 0.026 @ Normal Dist. (μ=20.0, σ=0.00867)
WARNING:root:Assuming Normal Dist. for 6: g Bearing -23 + 0.12 / + 0 @ Normal Dist. (μ=23.06, σ=0.02)
WARNING:root:Assuming Normal Dist. for 14: stacks on stacks - '6 Sigma' Analysis (assuming inputs with Normal Dist.) +0.1 ± 0.26433 @ Normal Dist. (μ=0.1, σ=0.05874)
          DIMENSION: stacks on stacks - '6 Sigma' Analysis - (assuming inputs with Normal Dist.)
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Desc.                               ┃ ± ┃ Nom. ┃ Tol.           ┃ Sens. (a) ┃ Abs. Bounds         ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 14 │ (assuming inputs with Normal Dist.) │ + │ 0.1  │ ± 0.26433      │ 1         │ [-0.16433, 0.36433] │
└────┴─────────────────────────────────────┴───┴──────┴────────────────┴───────────┴─────────────────────┘
                                       SPEC: stack spec
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Desc. ┃ Distribution                    ┃ Median ┃ Spec. Limits ┃ Yield Prob. ┃ Reject PPM ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│       │ Normal Dist. (μ=0.1, σ=0.05874) │ 0.425  │ [0.05, 0.8]  │ 80.2675148  │ 197324.85  │
└───────┴─────────────────────────────────┴────────┴──────────────┴─────────────┴────────────┘
```

![](./docs/newplot.png)
![](./docs/newplot2.png)

## Usage

dimstack works great as a library in a python script, in REPL, or in JupyterLab.

### and Notebook setup

```
%pip install -q dimstack
```

## Development

### Testing

```
python -m unittest
python -m unittest discover .\tests\
```

### Documenting

```
python -m mkdocs build
python -m mkdocs serve
python -m mkdocs gh-deploy
```

```
uv run mkdocs build
uv run mkdocs serve
uv run mkdocs gh-deploy
```

### Deploying

First bump version in pyproject.toml, then

```
uv build
uv publish
cp '.\\dist\\*.whl' '.\\notebooks\\pypi\\'
```

# Acknowledgements

- https://d2t1xqejof9utc.cloudfront.net/files/147765/Dimensioning%20and%20Tolerancing%20Handbook.pdf?1541238602
- http://www.newconceptzdesign.com/stackups/
- https://github.com/slightlynybbled/tol-stack
- https://www.mitcalc.com/doc/tolanalysis1d/help/en/tolanalysis1d.htm
- https://clas.iusb.edu/math-compsci/_prior-thesis/YFeng_thesis.pdf
- https://ris.utwente.nl/ws/portalfiles/portal/6632975/Salomons96computer1.pdf
- https://ris.utwente.nl/ws/files/6632926/Salomons96computer2.pdf
