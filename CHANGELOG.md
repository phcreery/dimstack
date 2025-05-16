## PLANNED

- [ ] Monte-Carlo simulation
- [ ] Tolerance Optimization [Simple Arithmetic, Fig 9-9, 11-7 in McGraw Hill,](https://www.mitcalc.com/en/ui/ui_tanalysis1.htm)
- [ ] Dimension.from_distribution() (nice to have for monte carlo)
- [ ] Add more distributions like Triangular
- [ ] Stack combined Yield (not for stackup analysis, but combined yield)
- [ ] Multi-dimensional tolerancing
- [ ] add tests for dimension sensitivity (a)

## 0.8.0 5/15/2025

- [x] Remove `target_process_sigma`
- [x] Rename Skew to Shift
- [x] Make reviewing dimension with assumption more ergonomic and consistent
- [x] Clean up logs about assuming distributions
- [x] Better display mode setting API with enum

## 0.7.1

- [x] fix symmetric tolerance "±" text display
- [x] improve plotting labels

## 0.7.0

- [x] more consistent API
- [x] simplify tolerance classes to single Tol.Bilateral (like Rust/v-lang implementation)

## 0.6.0

- [x] Fix negative distribution
- [x] Separate Dimension and StatisticalDim/Data. (AKA, merge StatisticalDim and Reviewed)
  - Basic Dimension
  - Reviewed Dimension (Reviewed just points at dimension and Distribution/Data)
  - Distribution
  - Requirement (For distribution or distribution data)
  - [x] WC, RSS, MRSS takes all Basic Dimensions
  - [x] SixSigma, MonteCarlo takes all Reviewed Dimensions
  - [x] Spec renamed to Requirement
  - [x] Plots work with new dims

## 0.5.1 11/15/2024

- [x] move ruff to dev dependency

## 0.5.0 11/12/2024

- [x] Move WC, RSS, MRSS calculations to separate locations
- [x] is Statistical "@ ± {self.target_process_sigma}σ & k={self.k}" needed?
- [x] fix StackPlot.add_dimension() not returning self
- [x] automatic or user specified plot dist data xbins (currently size=0.1)

## 0.4.0 11/11/2024

- [x] Fix negative statistical data
- [x] Show Abs. Bounds instead of Rel. Bounds
- [x] uv managed project

## 0.3.3

- [x] DivisionByZero regression fix in SixSigma analysis

## 0.3.2

- [x] fix abs_upper and abs_lower for negative nominal dimensions and add tests
- [x] rename `process_sigma` to `target_process_sigma`
- [x] deprecate Z_min/Z_max (abs_upper/abs_lower)

## 0.3.1 Released 9/30/2023

- [x] Fix plotting regression

## 0.3.0 Released 9/30/2023

- [x] remove self.items in MRSS(), they should just be items
- [x] reorder mean and stdev in C_pk()
- [x] rename upper_rel to rel_upper
- [x] rename "k" to "Skew (k)", "a" to "Sens. (a)", ...
- [x] rename stack.items to stack.dims
- [x] organize analysis calculations with dim.dir() first (in analysis and other locations)
- [x] rename title to name
- [x] give stack a description
- [x] make C_p and C_pk only work on normal distribution with +/-6sigma (or explicitly state they are "6 sigma" values)
- [x] add abs_upper and abs_lower (same as Z_min and Z_max)
- [x] remove distribution from Basic Dimension
- [x] restructure the way distributions are handled
- [x] rename rss_func to rss and make it receive array instead of arbitrary length parameters
- [x] WC: is tol.dir needed on t_wc computation? No
- [x] remove mean, stdev from Statistical Dimension
- [x] make k calculated from nominal and distribution mean
- [x] fix slight error in stack calculations in McGraw Hill Tests
- [x] rename tolerance to tol
- [x] Support to positive bilateral tolerances. Ex. 2 + 0.2 / + 0.1

## 0.2.0 Released 6/23/2023

## 0.1.0 Released 5/23/2023

Initial Release
