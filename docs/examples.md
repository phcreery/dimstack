## Interactive Jupyter Notebook

[Example Notebook](example.html)

## Motor Assembly textbook example, Chapter 9 through 11, Dimensioning and Tolerancing Handbook, McGraw Hill

```python
import dimstack as ds

ds.display.mode("text")

m1 = ds.StatisticalDimension(
    nom=208,
    tol=ds.tol.SymmetricBilateral(0.036),
    process_sigma=6,
    k=0.25,
    name="a",
    desc="Shaft",
)
m2 = ds.StatisticalDimension(
    nom=-1.75,
    tol=ds.tol.UnequalBilateral(0, 0.06),
    process_sigma=3,
    name="b",
    desc="Retainer ring",
)
m3 = ds.StatisticalDimension(nom=-23, tol=ds.tol.UnequalBilateral(0, 0.12), process_sigma=3, name="c", desc="Bearing")
m4 = ds.StatisticalDimension(
    nom=20,
    tol=ds.tol.SymmetricBilateral(0.026),
    process_sigma=3,
    name="d",
    desc="Bearing Sleeve",
)
m5 = ds.StatisticalDimension(nom=-200, tol=ds.tol.SymmetricBilateral(0.145), process_sigma=3, name="e", desc="Case")
m6 = ds.BasicDimension(
    nom=20,
    tol=ds.tol.SymmetricBilateral(0.026),
    # process_sigma=3,
    name="f",
    desc="Bearing Sleeve",
)
m7 = ds.StatisticalDimension(nom=-23, tol=ds.tol.UnequalBilateral(0, 0.12), process_sigma=3, name="g", desc="Bearing")
items = [m1, m2, m3, m4, m5, m6, m7]

stack = ds.Stack(title="stacks on stacks", items=items)

stack.show()
stack.Closed.show()
stack.WC.show()
stack.RSS.show()
stack.MRSS.show()
stack.SixSigma(at=4.5).show()

spec = ds.Spec("stack spec", "", dim=stack.SixSigma(at=4.5), LL=0.05, UL=0.8)
spec.show()
```

Returns:

```
Stack: stacks on stacks
ID Name    Description dir  Nom.           Tol. Sen.    Relative Bounds   Dist. Process Sigma    k C_p C_pk       μ       σ μ_eff   σ_eff Yield Probability Reject PPM
 0    a          Shaft   + 208.0 ± 0.036           1 [207.964, 208.036]  Normal          ± 6σ 0.25 2.0  1.5 208.009   0.006 208.0   0.008       99.99932047        6.8
 1    b  Retainer ring   -  1.75 + 0 / - 0.06      1       [1.69, 1.75]  Normal          ± 3σ    0 1.0  1.0    1.72    0.01  1.72    0.01       99.73002039     2699.8
 2    c        Bearing   -  23.0 + 0 / - 0.12      1        [22.88, 23]  Normal          ± 3σ    0 1.0  1.0   22.94    0.02 22.94    0.02       99.73002039     2699.8
 3    d Bearing Sleeve   +  20.0 ± 0.026           1   [19.974, 20.026]  Normal          ± 3σ    0 1.0  1.0    20.0 0.00867  20.0 0.00867       99.73002039     2699.8
 4    e           Case   - 200.0 ± 0.145           1 [199.855, 200.145]  Normal          ± 3σ    0 1.0  1.0   200.0 0.04833 200.0 0.04833       99.73002039     2699.8
 5    f Bearing Sleeve   +  20.0 ± 0.026           1   [19.974, 20.026] Uniform
 6    g        Bearing   -  23.0 + 0 / - 0.12      1        [22.88, 23]  Normal          ± 3σ    0 1.0  1.0   22.94    0.02 22.94    0.02       99.73002039     2699.8

Dimension: stacks on stacks - Closed Analysis
ID             Name     Description dir Nom.              Tol. Sen. Relative Bounds Distribution
 7 stacks on stacks Closed Analysis   + 0.25 + 0.533 / - 0.233    1  [0.017, 0.783]      Uniform

Dimension: stacks on stacks - WC Analysis
ID             Name Description dir Nom.           Tol. Sen. Relative Bounds Distribution
 8 stacks on stacks WC Analysis   +  0.4 ± 0.383           1  [0.017, 0.783]      Uniform

WARNING:root:Converting BasicDimension (5: f Bearing Sleeve +20 ± 0.026) to StatisticalDimension
Dimension: stacks on stacks - RSS Analysis (assuming inputs with Normal Distribution & ± 3σ)
ID             Name                                                    Description dir Nom.           Tol. Sen.    Relative Bounds Distribution Process Sigma k C_p C_pk   μ       σ μ_eff   σ_eff Yield Probability Reject PPM
10 stacks on stacks RSS Analysis (assuming inputs with Normal Distribution & ± 3σ)   +  0.4 ± 0.17825         1 [0.22175, 0.57825]       Normal          ± 3σ 0 1.0  1.0 0.4 0.05942   0.4 0.05942       99.73002039     2699.8

WARNING:root:Converting BasicDimension (5: f Bearing Sleeve +20 ± 0.026) to StatisticalDimension
Dimension: stacks on stacks - MRSS Analysis (assuming inputs with Normal Distribution & ± 3σ)
ID             Name                                                     Description dir Nom.           Tol. Sen.    Relative Bounds Distribution Process Sigma k     C_p    C_pk   μ       σ μ_eff   σ_eff Yield Probability Reject PPM
12 stacks on stacks MRSS Analysis (assuming inputs with Normal Distribution & ± 3σ)   +  0.4 ± 0.24046         1 [0.15954, 0.64046]       Normal    ± 3.76693σ 0 1.25564 1.25564 0.4 0.06383   0.4 0.06383       99.98347307     165.27

WARNING:root:Converting BasicDimension (5: f Bearing Sleeve +20 ± 0.026) to StatisticalDimension
Dimension: stacks on stacks - '6 Sigma' Analysis (assuming inputs with Normal Distribution)
ID             Name                                                   Description dir Nom.           Tol. Sen.    Relative Bounds Distribution Process Sigma k C_p C_pk   μ       σ μ_eff   σ_eff Yield Probability Reject PPM
14 stacks on stacks '6 Sigma' Analysis (assuming inputs with Normal Distribution)   +  0.4 ± 0.26433         1 [0.13567, 0.66433]       Normal        ± 4.5σ 0 1.5  1.5 0.4 0.05874   0.4 0.05874       99.99932047        6.8

WARNING:root:Converting BasicDimension (5: f Bearing Sleeve +20 ± 0.026) to StatisticalDimension
Spec: stack spec
      Name Description                                                                                                        Dimension Spec. Limits Median       k     C_p    C_pk Yield Probability Reject PPM
stack spec             16: stacks on stacks '6 Sigma' Analysis (assuming inputs with Normal Distribution) +0.4 ± 0.26433 @ ± 4.5σ & k=0  [0.05, 0.8]  0.425 0.06667 2.12804 1.98617               100          0

```

## MIT Calc Demonstration Analysis

[https://www.mitcalc.com/en/ui/ui_tanalysis1.htm](https://www.mitcalc.com/en/ui/ui_tanalysis1.htm)

```python
import dimstack

# this test is a copy of MITCalc User Interface diagram

m1 = dimstack.eval.StatisticalDimension(
    nom=208,
    tol=dimstack.tolerance.SymmetricBilateral(0.036),
    process_sigma=6,
    k=0.25,
    name="a",
    desc="Shaft",
)
m2 = dimstack.eval.StatisticalDimension(
    nom=-1.75,
    tol=dimstack.tolerance.UnequalBilateral(0, 0.06),
    process_sigma=3,
    name="b",
    desc="Retainer ring",
)
m3 = dimstack.eval.StatisticalDimension(nom=-23, tol=dimstack.tolerance.UnequalBilateral(0, 0.12), process_sigma=3, name="c", desc="Bearing")
m4 = dimstack.eval.StatisticalDimension(
    nom=20,
    tol=dimstack.tolerance.SymmetricBilateral(0.026),
    process_sigma=3,
    name="d",
    desc="Bearing Sleeve",
)
m5 = dimstack.eval.StatisticalDimension(nom=-200, tol=dimstack.tolerance.SymmetricBilateral(0.145), process_sigma=3, name="e", desc="Case")
m6 = dimstack.eval.StatisticalDimension(
    nom=20,
    tol=dimstack.tolerance.SymmetricBilateral(0.026),
    process_sigma=3,
    name="f",
    desc="Bearing Sleeve",
)
m7 = dimstack.eval.StatisticalDimension(nom=-23, tol=dimstack.tolerance.UnequalBilateral(0, 0.12), process_sigma=3, name="g", desc="Bearing")
items = [m1, m2, m3, m4, m5, m6, m7]

stack = dimstack.eval.Stack(title="stacks on stacks", items=items)

stack.show()
stack.Closed.show()
stack.WC.show()
stack.RSS.show()
stack.MRSS.show()
stack.SixSigma(at=4.5).show()
```

Returns:

```
Stack: stacks on stacks
ID Name                     Description dir  Nom.             Tol. Sen. Relative Bounds Distribution Process Sigma k C_p C_pk μ σ μ_eff σ_eff Yield Probability Reject PPM
 0    A             Screw thread length   - 0.375   + 0 / - 0.031     1  [0.344, 0.375]      Uniform
 1    B                   Washer Length   + 0.032   ± 0.002           1   [0.03, 0.034]      Uniform
 2    C Inner bearing cap turned length   +  0.06   ± 0.003           1  [0.057, 0.063]      Uniform
 3    D                  Bearing length   + 0.438   + 0 / - 0.015     1  [0.423, 0.438]      Uniform
 4    E            Spacer turned length   +  0.12   ± 0.005           1  [0.115, 0.125]      Uniform
 5    F                    Rotor length   +   1.5 + 0.01 / - 0.004    1   [1.496, 1.51]      Uniform
 4    G            Spacer turned length   +  0.12   ± 0.005           1  [0.115, 0.125]      Uniform
 3    H                  Bearing length   + 0.438   + 0 / - 0.015     1  [0.423, 0.438]      Uniform
 6    I           Pulley casting length   +  0.45   ± 0.007           1  [0.443, 0.457]      Uniform
 7    J             Shaft turned length   - 3.019   + 0.012 / - 0     1  [3.019, 3.031]      Uniform
 8    K               Tapped hole depth   +   0.3   ± 0.03            1    [0.27, 0.33]      Uniform

Dimension: stacks on stacks - Closed Analysis -
ID                               Name Description dir  Nom.              Tol. Sen. Relative Bounds Distribution
 9 stacks on stacks - Closed Analysis               + 0.064 + 0.093 / - 0.098    1 [-0.034, 0.157]      Uniform

Dimension: stacks on stacks - WC Analysis -
ID                           Name Description dir   Nom.           Tol. Sen. Relative Bounds Distribution
10 stacks on stacks - WC Analysis               + 0.0615 ± 0.0915          1  [-0.03, 0.153]      Uniform

WARNING:root:Converting BasicDimension (0: A Screw thread length -0.375 + 0 / - 0.031) to StatisticalDimension
WARNING:root:Converting BasicDimension (1: B Washer Length +0.032 ± 0.002) to StatisticalDimension
WARNING:root:Converting BasicDimension (2: C Inner bearing cap turned length +0.06 ± 0.003) to StatisticalDimension
WARNING:root:Converting BasicDimension (3: D Bearing length +0.438 + 0 / - 0.015) to StatisticalDimension
WARNING:root:Converting BasicDimension (4: E Spacer turned length +0.12 ± 0.005) to StatisticalDimension
WARNING:root:Converting BasicDimension (5: F Rotor length +1.5 + 0.01 / - 0.004) to StatisticalDimension
WARNING:root:Converting BasicDimension (4: G Spacer turned length +0.12 ± 0.005) to StatisticalDimension
WARNING:root:Converting BasicDimension (3: H Bearing length +0.438 + 0 / - 0.015) to StatisticalDimension
WARNING:root:Converting BasicDimension (6: I Pulley casting length +0.45 ± 0.007) to StatisticalDimension
WARNING:root:Converting BasicDimension (7: J Shaft turned length -3.019 + 0.012 / - 0) to StatisticalDimension
WARNING:root:Converting BasicDimension (8: K Tapped hole depth +0.3 ± 0.03) to StatisticalDimension
Dimension: stacks on stacks - RSS Analysis - (assuming inputs with Normal Distribution & ± 3σ)
ID                            Name                                       Description dir   Nom.           Tol. Sen.    Relative Bounds Distribution Process Sigma k C_p C_pk      μ       σ  μ_eff   σ_eff Yield Probability Reject PPM
22 stacks on stacks - RSS Analysis (assuming inputs with Normal Distribution & ± 3σ)   + 0.0615 ± 0.03755         1 [0.02395, 0.09905]       Normal          ± 3σ 0 1.0  1.0 0.0615 0.01252 0.0615 0.01252       99.73002039     2699.8

WARNING:root:Converting BasicDimension (0: A Screw thread length -0.375 + 0 / - 0.031) to StatisticalDimension
WARNING:root:Converting BasicDimension (1: B Washer Length +0.032 ± 0.002) to StatisticalDimension
WARNING:root:Converting BasicDimension (2: C Inner bearing cap turned length +0.06 ± 0.003) to StatisticalDimension
WARNING:root:Converting BasicDimension (3: D Bearing length +0.438 + 0 / - 0.015) to StatisticalDimension
WARNING:root:Converting BasicDimension (4: E Spacer turned length +0.12 ± 0.005) to StatisticalDimension
WARNING:root:Converting BasicDimension (5: F Rotor length +1.5 + 0.01 / - 0.004) to StatisticalDimension
WARNING:root:Converting BasicDimension (4: G Spacer turned length +0.12 ± 0.005) to StatisticalDimension
WARNING:root:Converting BasicDimension (3: H Bearing length +0.438 + 0 / - 0.015) to StatisticalDimension
WARNING:root:Converting BasicDimension (6: I Pulley casting length +0.45 ± 0.007) to StatisticalDimension
WARNING:root:Converting BasicDimension (7: J Shaft turned length -3.019 + 0.012 / - 0) to StatisticalDimension
WARNING:root:Converting BasicDimension (8: K Tapped hole depth +0.3 ± 0.03) to StatisticalDimension
Dimension: stacks on stacks - MRSS Analysis - (assuming inputs with Normal Distribution & ± 3σ)
ID                             Name                                       Description dir   Nom.           Tol. Sen.    Relative Bounds Distribution Process Sigma k     C_p    C_pk      μ       σ  μ_eff   σ_eff Yield Probability Reject PPM
34 stacks on stacks - MRSS Analysis (assuming inputs with Normal Distribution & ± 3σ)   + 0.0615 ± 0.04919         1 [0.01231, 0.11069]       Normal    ± 3.22567σ 0 1.07522 1.07522 0.0615 0.01525 0.0615 0.01525       99.87432157    1256.78

WARNING:root:Converting BasicDimension (0: A Screw thread length -0.375 + 0 / - 0.031) to StatisticalDimension
WARNING:root:Converting BasicDimension (1: B Washer Length +0.032 ± 0.002) to StatisticalDimension
WARNING:root:Converting BasicDimension (2: C Inner bearing cap turned length +0.06 ± 0.003) to StatisticalDimension
WARNING:root:Converting BasicDimension (3: D Bearing length +0.438 + 0 / - 0.015) to StatisticalDimension
WARNING:root:Converting BasicDimension (4: E Spacer turned length +0.12 ± 0.005) to StatisticalDimension
WARNING:root:Converting BasicDimension (5: F Rotor length +1.5 + 0.01 / - 0.004) to StatisticalDimension
WARNING:root:Converting BasicDimension (4: G Spacer turned length +0.12 ± 0.005) to StatisticalDimension
WARNING:root:Converting BasicDimension (3: H Bearing length +0.438 + 0 / - 0.015) to StatisticalDimension
WARNING:root:Converting BasicDimension (6: I Pulley casting length +0.45 ± 0.007) to StatisticalDimension
WARNING:root:Converting BasicDimension (7: J Shaft turned length -3.019 + 0.012 / - 0) to StatisticalDimension
WARNING:root:Converting BasicDimension (8: K Tapped hole depth +0.3 ± 0.03) to StatisticalDimension
Dimension: stacks on stacks - '6 Sigma' Analysis - (assuming inputs with Normal Distribution)
ID                                  Name                                Description dir   Nom.           Tol. Sen.    Relative Bounds Distribution Process Sigma k C_p C_pk      μ       σ  μ_eff   σ_eff Yield Probability Reject PPM
46 stacks on stacks - '6 Sigma' Analysis (assuming inputs with Normal Distribution)   + 0.0615 ± 0.05617         1 [0.00533, 0.11767]       Normal        ± 4.5σ 0 1.5  1.5 0.0615 0.01248 0.0615 0.01248       99.99932047        6.8
```