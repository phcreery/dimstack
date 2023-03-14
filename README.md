# dimstack

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

Python library for analysis of and design for statistical tolerancing.

## Example

```python
import dimstack.display
import dimstack.tolerance
import dimstack.eval

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

eval = stack.RSS
eval.show()

stack.MRSS.show()

eval = stack.SixSigma(at=4.5)
eval.show()

assy = dimstack.eval.Assembly("assy", "", dim=eval, LL=0.05, UL=0.8, process_sigma=4.5)
assy.show()

```

Returns:

```
stacks on stacks
ID Name    Description dir  Nom.           Tol. Sen.    Relative Bounds Process Sigma     μ       σ C_p    k C_pk μ_eff   σ_eff Yield Probability Reject PPM
 0    a          Shaft   + 208.0 ± 0.036           1 [207.964, 208.036]          ± 6σ 208.0   0.006 2.0 0.25  1.5 208.0   0.008        99.9999998        0.0
 1    b  Retainer ring   -  1.75 + 0 / - 0.06     -1       [1.69, 1.75]          ± 3σ  1.72    0.01 1.0    0  1.0  1.72    0.01       99.73002039     2699.8
 2    c        Bearing   -  23.0 + 0 / - 0.12     -1        [22.88, 23]          ± 3σ 22.94    0.02 1.0    0  1.0 22.94    0.02       99.73002039     2699.8
 3    d Bearing Sleeve   +  20.0 ± 0.026           1   [19.974, 20.026]          ± 3σ  20.0 0.00867 1.0    0  1.0  20.0 0.00867       99.73002039     2699.8
 4    e           Case   - 200.0 ± 0.145          -1 [199.855, 200.145]          ± 3σ 200.0 0.04833 1.0    0  1.0 200.0 0.04833       99.73002039     2699.8
 5    f Bearing Sleeve   +  20.0 ± 0.026           1   [19.974, 20.026]                20.0
 6    g        Bearing   -  23.0 + 0 / - 0.12     -1        [22.88, 23]          ± 3σ 22.94    0.02 1.0    0  1.0 22.94    0.02       99.73002039     2699.8

Closed
ID   Name      Description dir Nom.              Tol. Sen. Relative Bounds   μ
 7 Closed stacks on stacks   + 0.25 + 0.533 / - 0.233    1  [0.017, 0.783] 0.4

WC
ID Name      Description dir Nom.           Tol. Sen. Relative Bounds   μ
 8   WC stacks on stacks   +  0.4 ± 0.383           1  [0.017, 0.783] 0.4

RSS
ID Name      Description dir Nom.           Tol. Sen.    Relative Bounds Process Sigma   μ       σ C_p k C_pk μ_eff   σ_eff Yield Probability Reject PPM
10  RSS stacks on stacks   +  0.4 ± 0.17825         1 [0.22175, 0.57825]          ± 3σ 0.4 0.05942 1.0 0  1.0   0.4 0.05942       99.73002039     2699.8

MRSS
ID Name      Description dir Nom.           Tol. Sen.    Relative Bounds Process Sigma   μ       σ C_p k C_pk μ_eff   σ_eff Yield Probability Reject PPM
12 MRSS stacks on stacks   +  0.4 ± 0.24046         1 [0.15954, 0.64046]          ± 3σ 0.4 0.08015 1.0 0  1.0   0.4 0.08015       99.73002039     2699.8

'6 Sigma'
ID      Name      Description dir Nom.           Tol. Sen.    Relative Bounds Process Sigma   μ       σ C_p k C_pk μ_eff   σ_eff Yield Probability Reject PPM
14 '6 Sigma' stacks on stacks   +  0.4 ± 0.26433         1 [0.13567, 0.66433]        ± 4.5σ 0.4 0.05874 1.5 0  1.5   0.4 0.05874       99.99932047        6.8

assy
Name Description Relative Bounds Process Sigma     μ     C_p       k    C_pk Yield Probability Reject PPM
assy                 [0.05, 0.8]        ± 4.5σ 0.425 2.12804 0.14187 1.98617       99.99999987        0.0
```

## Notebooks

```
cd notebooks
jupyter lite init

jupyter lite build --contents .
jupyter lite serve
```

```
import piplite
await piplite.install('dimstack', keep_going=True)
```

OR

```
%pip install -q dimstack
```

## Dev

`C:\Users\phcre\AppData\Roaming\Python\Scripts\pdm.exe add [package]`

`C:\Users\phcre\AppData\Roaming\Python\Scripts\pdm.exe build`

```
.\.venv\Scripts\activate
```

### Testing

```
python -m unittest discover .\tests\
```

# Acknowledgements

- http://www.newconceptzdesign.com/stackups/
- https://github.com/slightlynybbled/tol-stack
-
