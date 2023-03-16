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
Stack: stacks on stacks
ID Name                     Description dir  Nom.             Tol. Sen. Relative Bounds Process Sigma k C_p C_pk      μ σ μ_eff σ_eff Yield Probability Reject PPM
 0    A             Screw thread length   - 0.375   + 0 / - 0.031     1  [0.344, 0.375]                          0.3595
 1    B                   Washer Length   + 0.032   ± 0.002           1   [0.03, 0.034]                           0.032
 2    C Inner bearing cap turned length   +  0.06   ± 0.003           1  [0.057, 0.063]                            0.06
 3    D                  Bearing length   + 0.438   + 0 / - 0.015     1  [0.423, 0.438]                          0.4305
 4    E            Spacer turned length   +  0.12   ± 0.005           1  [0.115, 0.125]                            0.12
 5    F                    Rotor length   +   1.5 + 0.01 / - 0.004    1   [1.496, 1.51]                           1.503
 4    G            Spacer turned length   +  0.12   ± 0.005           1  [0.115, 0.125]                            0.12
 3    H                  Bearing length   + 0.438   + 0 / - 0.015     1  [0.423, 0.438]                          0.4305
 6    I           Pulley casting length   +  0.45   ± 0.007           1  [0.443, 0.457]                            0.45
 7    J             Shaft turned length   - 3.019   + 0.012 / - 0     1  [3.019, 3.031]                           3.025
 8    K               Tapped hole depth   +   0.3   ± 0.03            1    [0.27, 0.33]                             0.3

Dimension: Closed - stacks on stacks
ID   Name      Description dir  Nom.              Tol. Sen. Relative Bounds      μ
 9 Closed stacks on stacks   + 0.064 + 0.093 / - 0.098    1 [-0.034, 0.157] 0.0615

Dimension: WC - stacks on stacks
ID Name      Description dir   Nom.           Tol. Sen. Relative Bounds      μ
10   WC stacks on stacks   + 0.0615 ± 0.0915          1  [-0.03, 0.153] 0.0615

Dimension: RSS - stacks on stacks
ID Name      Description dir   Nom.           Tol. Sen.    Relative Bounds Process Sigma k C_p C_pk      μ       σ  μ_eff   σ_eff Yield Probability Reject PPM
22  RSS stacks on stacks   + 0.0615 ± 0.03755         1 [0.02395, 0.09905]          ± 3σ 0 1.0  1.0 0.0615 0.01252 0.0615 0.01252       99.73002039     2699.8

Dimension: MRSS - stacks on stacks
ID Name      Description dir   Nom.           Tol. Sen.    Relative Bounds Process Sigma k C_p C_pk      μ      σ  μ_eff  σ_eff Yield Probability Reject PPM
34 MRSS stacks on stacks   + 0.0615 ± 0.04919         1 [0.01231, 0.11069]          ± 3σ 0 1.0  1.0 0.0615 0.0164 0.0615 0.0164       99.73002039     2699.8

Dimension: '6 Sigma' - stacks on stacks
ID      Name      Description dir   Nom.           Tol. Sen.    Relative Bounds Process Sigma k C_p C_pk      μ       σ  μ_eff   σ_eff Yield Probability Reject PPM
46 '6 Sigma' stacks on stacks   + 0.0615 ± 0.05617         1 [0.00533, 0.11767]        ± 4.5σ 0 1.5  1.5 0.0615 0.01248 0.0615 0.01248       99.99932047        6.8

Spec: stack spec
      Name Description                                                      Dimension Spec. Limits Spec. Process Sigma       k      C_p    C_pk     μ Yield Probability Reject PPM
stack spec             58: '6 Sigma' stacks on stacks +0.0615 ± 0.05617 @ ±4.5σ & k=0  [0.05, 0.8]              ± 4.5σ 9.70662 10.01371 0.30709 0.425       82.15429019   178457.1
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
- https://www.mitcalc.com/doc/tolanalysis1d/help/en/tolanalysis1d.htm
