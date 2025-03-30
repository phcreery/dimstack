import math
from typing import List

# "6 Sigma" equations.


def C_p(UL: float, LL: float, std_dev: float) -> float:
    """
    Process capability index.

    Args:
        UL (int): Upper limit.
        LL (int): Lower limit.
        sigma (int): Standard deviation.

    Returns:
        float: Process capability index.

    >>> C_p(1, 0, 1)
    0.16666666666666666
    >>> C_p(6, -6, 1)
    2.0
    """
    return (UL - LL) / (6 * std_dev)


def C_pk(UL: float, LL: float, mean: float, std_dev: float) -> float:
    """
    Process capability index. adjusted for centering.
    Cpl = (mu - L)/3*std_dev
    Cpu = (U - mu)/3*std_dev
    C_pk = min(Cpl, Cpu) = (1 - k) * C_p

    Args:
        UL (float): Upper limit.
        LL (float): Lower limit.
        std_dev (float): Standard deviation.
        mean (float): Mean.

    Returns:
        float: Process capability index.

    >>> from .utils import nround
    >>> nround(C_pk(208.036, 207.964, 208.009, 0.006))
    1.5
    """
    return min(
        (UL - mean) / (3 * std_dev),
        (mean - LL) / (3 * std_dev),
    )
    # return (1 - k) * C_p


def rss_args(*args):
    """
    Root sum square.

    >>> rss_args(1, 2, 3)
    3.7416573867739413
    """
    return (sum([arg**2 for arg in args])) ** 0.5


def rss(args: List[float]):
    """
    Root sum square.

    >>> rss([1, 2, 3])
    3.7416573867739413
    """
    val = 0
    for arg in args:
        val += arg * arg
    val = math.sqrt(val)
    return val


def C_f(t_rss, t_wc, n):
    """Correction factor used to calculate the modified RSS.

    Args:
        t_rss (_type_): _description_
        t_wc (_type_): _description_
        n (_type_): _description_

    Returns:
        _type_: _description_
    """
    return ((0.5 * (t_wc - t_rss)) / (t_rss * (n**0.5 - 1))) + 1


def normal_cdf(x, mean=0, std_dev=1):
    """
    Cumulative distribution function for the normal distribution.

    >>> normal_cdf(0)
    0.5
    >>> normal_cdf(1)
    0.8413447460685428
    >>> normal_cdf(2)
    0.9772498680518209
    """
    return 0.5 * (1 + math.erf((x - mean) / (std_dev * (2**0.5))))


def normal_dist(x, mean=0, std_dev=1):
    prob_density = (math.pi * std_dev) * math.exp(-0.5 * ((x - mean) / std_dev) ** 2)
    return prob_density


if __name__ == "__main__":
    import doctest

    doctest.testmod()
