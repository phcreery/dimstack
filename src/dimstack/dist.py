import numpy as np
from scipy.stats import norm, uniform


DIST_UNIFORM = "Uniform"  # Uniform distribution.
DIST_NORMAL = "Normal"  # Normal distribution.
DIST_SCREENED = "Screened"  # Normal distribution which has been screened. e.g. Go-NoGo or Pass-Fail fixture.
# DIST_NOTCHED = "Notched"  # This is a common distribution when parts are being sorted and the leftover parts are used.
# DIST_NORMAL_LT = "Normal LT"  # Normal distribution which has been screened in order to remove lengths above a limit.
# DIST_NORMAL_GT = "Normal GT"  # Normal distribution which has been screened in order to remove lengths below a limit.


class Uniform:
    def __init__(self, lower: float, upper: float):
        self.lower = lower
        self.upper = upper

    def __repr__(self) -> str:
        return f"UniformDistribution({self.lower}, {self.upper})"

    def sample(self, n: int):
        # return np.random.uniform(self.lower, self.upper, n)
        return uniform.rvs(loc=self.lower, scale=self.upper - self.lower, size=n)

    def pdf(self, x: float):
        return uniform.pdf(x, loc=self.lower, scale=self.upper - self.lower)

    def cdf(self, x: float):
        return uniform.cdf(x, loc=self.lower, scale=self.upper - self.lower)


class Normal:
    def __init__(self, mean: float, stdev: float):
        self.mean = mean
        self.stdev = stdev

    def __repr__(self) -> str:
        return f"NormalDistribution({self.mean}, {self.stdev})"

    def sample(self, n: int):
        # return np.random.normal(self.mean, self.stdev, n)
        return norm.rvs(loc=self.mean, scale=self.stdev, size=n)

    def pdf(self, x: float):
        return norm.pdf(x, loc=self.mean, scale=self.stdev)

    def cdf(self, x: float):
        return norm.cdf(x, loc=self.mean, scale=self.stdev)


class NormalScreened:
    def __init__(self, mean: float, stdev: float, lower: float, upper: float):
        self.mean = mean
        self.stdev = stdev
        self.lower = lower
        self.upper = upper

    def __repr__(self) -> str:
        return f"NormalDistribution({self.mean}, {self.stdev})"

    def sample(self, n: int):
        numbers = norm.rvs(loc=self.mean, scale=self.stdev, size=n)
        # filter out numbers that are not between lower and upper
        screenednumbers = np.extract((numbers >= self.lower) & (numbers <= self.upper), numbers)
        return screenednumbers

    def pdf(self, x: float):
        if x < self.lower:
            return 0
        elif x > self.upper:
            return 0
        return norm.pdf(x, loc=self.mean, scale=self.stdev)

    def cdf(self, x: float):
        if x < self.lower:
            return 0
        elif x > self.upper:
            return 0
        return norm.cdf(x, loc=self.mean, scale=self.stdev)