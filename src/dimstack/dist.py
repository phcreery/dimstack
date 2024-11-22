from typing import List, Union

import numpy as np
import pandas as pd
from scipy.stats import norm, uniform

from .utils import nround

# TODO:
# DIST_NOTCHED = "Notched"  # This is a common distribution when parts are being sorted and the leftover parts are used.
# DIST_NORMAL_LT = "Normal LT"  # Normal distribution which has been screened in order to remove lengths above a limit.
# DIST_NORMAL_GT = "Normal GT"  # Normal distribution which has been screened in order to remove lengths below a limit.


class Uniform:
    """Uniform distribution.

    Args:
        lower (float): Lower limit.
        upper (float): Upper limit.
    """

    def __init__(self, lower: float, upper: float):
        self.lower = lower
        self.upper = upper

    # def __repr__(self) -> str:
    #     return f"UniformDistribution({nround(self.lower)}, {nround(self.upper)})"

    def __str__(self) -> str:
        return f"Uniform Dist. [{nround(self.lower)}, {nround(self.upper)}]"

    def sample(self, n: int):
        # return np.random.uniform(self.lower, self.upper, n)
        return uniform.rvs(loc=self.lower, scale=self.upper - self.lower, size=n)

    def pdf(self, x: float):
        return uniform.pdf(x, loc=self.lower, scale=self.upper - self.lower)

    def cdf(self, x: float):
        return uniform.cdf(x, loc=self.lower, scale=self.upper - self.lower)


class Normal:
    """Normal distribution.

    Args:
        mean (float): Mean.
        stdev (float): Standard deviation.
    """

    def __init__(self, mean: float, stdev: float):
        self.mean = mean
        self.stdev = stdev
        self.data = None

    # def __repr__(self) -> str:
    #     return f"NormalDistribution({nround(self.mean)}, {nround(self.stdev)})"

    def __str__(self) -> str:
        return f"Normal Dist. μ={nround(self.mean)}, σ={nround(self.stdev)}"

    @property
    def variance(self):
        return self.stdev**2

    def sample(self, n: int):
        # return np.random.normal(self.mean, self.stdev, n)
        return norm.rvs(loc=self.mean, scale=self.stdev, size=n)

    def pdf(self, x: float):
        return norm.pdf(x, loc=self.mean, scale=self.stdev)

    def cdf(self, x: float):
        return norm.cdf(x, loc=self.mean, scale=self.stdev)

    @classmethod
    def fit(cls, data: Union[np.ndarray, List[float], List[int], List[np.float64], pd.Series]):
        mean, stdev = norm.fit(data)
        inst = cls(mean, stdev)
        inst.data = data
        return inst


class NormalScreened:
    """Normal distribution which has been screened. e.g. Go-NoGo or Pass-Fail fixture.

    Args:
        mean (float): Mean.
        stdev (float): Standard deviation.
        lower (float): Lower limit.
        upper (float): Upper limit.
    """

    # https://en.wikipedia.org/wiki/Truncated_normal_distribution

    def __init__(self, mean: float, stdev: float, lower: float, upper: float):
        self.mean = mean
        self.stdev = stdev
        self.lower = lower
        self.upper = upper

    # def __repr__(self) -> str:
    #     return f"Normal Screened Dist. (μ={nround(self.mean)}, σ={nround(self.stdev)})"
    def __str__(self) -> str:
        return f"Normal Screened Dist. μ={nround(self.mean)}, σ={nround(self.stdev)} [{nround(self.lower)}, {nround(self.upper)}]"

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
            return 1
        return norm.cdf(x, loc=self.mean, scale=self.stdev)
