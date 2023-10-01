# dimstack

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

Python library for mechanical engineers to help with statistical tolerancing analysis and design.

https://pypi.org/project/dimstack/

## Example (MIT Calc Demonstration Analysis)

```python
import dimstack as ds

ds.display.mode("text")

k = 0.25
process_sigma = 6
stdev = 0.036 / process_sigma
m1 = ds.dim.Statistical(
    nom=208,
    tol=ds.tol.SymmetricBilateral(0.036),
    distribution=ds.dist.Normal(208 + k * process_sigma * stdev, stdev),
    process_sigma=process_sigma,
    name="a",
    desc="Shaft",
)
m2 = ds.dim.Statistical(
    nom=-1.75,
    tol=ds.tol.UnequalBilateral(0, 0.06),
    process_sigma=3,
    name="b",
    desc="Retainer ring",
)
m3 = ds.dim.Statistical(nom=-23, tol=ds.tol.UnequalBilateral(0, 0.12), process_sigma=3, name="c", desc="Bearing")
m4 = ds.dim.Statistical(
    nom=20,
    tol=ds.tol.SymmetricBilateral(0.026),
    process_sigma=3,
    name="d",
    desc="Bearing Sleeve",
)
m5 = ds.dim.Statistical(nom=-200, tol=ds.tol.SymmetricBilateral(0.145), process_sigma=3, name="e", desc="Case")
m6 = ds.dim.Basic(
    nom=20,
    tol=ds.tol.SymmetricBilateral(0.026),
    # process_sigma=3,
    name="f",
    desc="Bearing Sleeve",
)
m7 = ds.dim.Statistical(nom=-23, tol=ds.tol.UnequalBilateral(0, 0.12), process_sigma=3, name="g", desc="Bearing")
items = [m1, m2, m3, m4, m5, m6, m7]

stack = ds.Stack(name="stacks on stacks", dims=items)

stack.show()
stack.Closed.show()
stack.WC.show()
stack.RSS.show()
stack.MRSS.show()
stack.SixSigma(at=4.5).show()

spec = ds.Spec("stack spec", "", dim=stack.SixSigma(at=4.5), LL=0.05, UL=0.8)
spec.show()

ds.plot.StackPlot().add(stack).add(stack.RSS).show()
```

Returns:

```
Stack: stacks on stacks
ID Name    Description dir  Nom.           Tol. Sens. (a)    Relative Bounds                      Distribution Process Sigma Skew (k) C_p C_pk μ σ μ_eff σ_eff Yield Probability Reject PPM
 0    a          Shaft   + 208.0 ± 0.036                1 [207.964, 208.036] Normal Dist. (μ=208.009, σ=0.006)          ± 6σ     0.25 2.0  1.5     208.0 0.008       99.99966023        3.4
 1    b  Retainer ring   -  1.75 + 0.06 / + 0           1       [1.75, 1.81]                              None          ± 3σ        0               1.78     0                 0          0
 2    c        Bearing   -  23.0 + 0.12 / + 0           1        [23, 23.12]                              None          ± 3σ        0              23.06     0                 0          0
 3    d Bearing Sleeve   +  20.0 ± 0.026                1   [19.974, 20.026]                              None          ± 3σ        0               20.0     0                 0          0
 4    e           Case   - 200.0 ± 0.145                1 [199.855, 200.145]                              None          ± 3σ        0              200.0     0                 0          0
 5    f Bearing Sleeve   +  20.0 ± 0.026                1   [19.974, 20.026]
 6    g        Bearing   -  23.0 + 0.12 / + 0           1        [23, 23.12]                              None          ± 3σ        0              23.06     0                 0          0

Dimension: stacks on stacks - Closed Analysis -
ID                               Name Description dir Nom.              Tol. Sens. (a) Relative Bounds
 7 stacks on stacks - Closed Analysis               + 0.25 + 0.233 / - 0.533         1 [-0.283, 0.483]

Dimension: stacks on stacks - WC Analysis -
ID                           Name Description dir Nom.           Tol. Sens. (a) Relative Bounds
 8 stacks on stacks - WC Analysis               +  0.1 ± 0.383                1 [-0.283, 0.483]

WARNING:root:Converting Basic (5: f Bearing Sleeve +20 ± 0.026) to Statistical dimension
Dimension: stacks on stacks - RSS Analysis - (assuming inputs with Normal Distribution & ± 3σ)
ID                            Name                                       Description dir Nom.           Tol. Sens. (a)     Relative Bounds Distribution Process Sigma Skew (k) C_p C_pk μ_eff σ_eff Yield Probability Reject PPM
10 stacks on stacks - RSS Analysis (assuming inputs with Normal Distribution & ± 3σ)   +  0.1 ± 0.17825              1 [-0.07825, 0.27825]         None          ± 3σ        0            0.1     0                 0          0

WARNING:root:Converting Basic (5: f Bearing Sleeve +20 ± 0.026) to Statistical dimension
Dimension: stacks on stacks - MRSS Analysis - (assuming inputs with Normal Distribution & ± 3σ)
ID                             Name                                       Description dir Nom.           Tol. Sens. (a)     Relative Bounds Distribution Process Sigma Skew (k) C_p C_pk μ_eff σ_eff Yield Probability Reject PPM
12 stacks on stacks - MRSS Analysis (assuming inputs with Normal Distribution & ± 3σ)   +  0.1 ± 0.24046              1 [-0.14046, 0.34046]         None    ± 3.76693σ        0            0.1     0                 0          0

WARNING:root:Converting Basic (5: f Bearing Sleeve +20 ± 0.026) to Statistical dimension
Dimension: stacks on stacks - '6 Sigma' Analysis - (assuming inputs with Normal Distribution)
ID                                  Name                                Description dir Nom.           Tol. Sens. (a) Relative Bounds                  Distribution Process Sigma Skew (k) C_p C_pk μ_eff σ_eff Yield Probability Reject PPM
14 stacks on stacks - '6 Sigma' Analysis (assuming inputs with Normal Distribution)   +  0.1 ± 0.036                1  [0.064, 0.136] Normal Dist. (μ=0.1, σ=0.008)        ± 4.5σ      0.0 1.5  1.5   0.1 0.008       99.99932047        6.8

WARNING:root:Converting Basic (5: f Bearing Sleeve +20 ± 0.026) to Statistical dimension
Spec: stack spec
      Name Description                                                                                                          Dimension Median Spec. Limits Yield Probability Reject PPM
stack spec             16: stacks on stacks - '6 Sigma' Analysis (assuming inputs with Normal Distribution) +0.1 ± 0.036 @ ± 4.5σ & k=0.0  0.425  [0.05, 0.8]       99.99999998        0.0

WARNING:root:Converting Basic (5: f Bearing Sleeve +20 ± 0.026) to Statistical dimension
```

![](./docs/newplot.png)
![](./docs/newplot2.png)

## Usage

dimstack can be used in a standard python script, or as a REPL, allowing use in JupyterLab.

Demo usage in a JupyterLite Lab

- https://phcreery.github.io/dimstack/lab/index.html

Demo usage in a JuptyerLite REPL:

- https://phcreery.github.io/dimstack/repl/index.html?kernel=python&toolbar=1&code=%pip%20install%20-q%20ds%0Aimport%20dimstack%20as%20ds

Embed in your site:

```html
<iframe
  src="https://phcreery.github.io/dimstack/repl/index.html?kernel=python&toolbar=1&code=%pip%20install%20-q%20ds%0Aimport%20dimstack%20as%20ds"
  width="100%"
  height="100%"
></iframe>
```

## Development

### Testing

```
pdm run test
```

OR

```
python -m unittest discover .\tests\
```

### Documenting

```
pdm run docs
pdm run deploydocs
```

### Deploying

First bump version in pyproject.toml, then build and publish

```
pdm build
pdm publish --no-build
```

### and Notebook setup

See https://github.com/phcreery/dimstack-demo

```
%pip install -q dimstack
```

# Acknowledgements

- http://www.newconceptzdesign.com/stackups/
- https://github.com/slightlynybbled/tol-stack
- https://www.mitcalc.com/doc/tolanalysis1d/help/en/tolanalysis1d.htm
