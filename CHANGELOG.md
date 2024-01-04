## PLANNED

- [ ] simplify tolerance classes to single Tol.Bilateral (like vlangs implementation)
- [ ] simplify from_basic_dim like the vlangs
- [ ] add Distribution.from_process_capability_index(C_p, C_pk, k) ??
- [ ] depricate Z_min/Z_max (abs_upper/abs_lower)
- [ ] add rel_upper/rel_lower properties
- [ ] abs_upper/abs_lower to display table
- [ ] fix abs_upper and abs_lower for negative nominal dimensions and add tests
- [ ] rename `process_sigma` to `target_process_sigma`


## 0.3.1 Released 9/30/23

- [x] Fix plotting regression

## 0.3.0 Released 9/30/23

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
