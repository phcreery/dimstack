## PLANNED

TODO: .py

- [ ] rename tolerance to tol
- [ ] simplify tolerance classes to single Tol.Bilateral (like vlangs implementation)
- [ ] simplify from_basic_dim like the vlangs
- [ ] fix slight error in stack calculations in McGraw Hill Tests

## 0.3.0 Planned

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

## 0.2.0 Released

## 0.1.0

Initial Release
