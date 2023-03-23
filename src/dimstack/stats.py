import math

# "6 Sigma" equations.


def C_p(UL: float, LL: float, stdev: float) -> float:
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
    return (UL - LL) / (6 * stdev)


def C_pk(UL: float, LL: float, stdev: float, mean: float) -> float:
    """
    Process capability index. adjusted for centering.
    Cpl = (mu - L)/3*stdev
    Cpu = (U - mu)/3*stdev
    C_pk = min(Cpl, Cpu) = (1 - k) * C_p

    Args:
        UL (float): Upper limit.
        LL (float): Lower limit.
        stdev (float): Standard deviation.
        mean (float): Mean.

    Returns:
        float: Process capability index.

    >>> from .utils import nround
    >>> nround(C_pk(208.036, 207.964, 0.006, 208.009))
    1.5
    """
    return min(
        (UL - mean) / (3 * stdev),
        (mean - LL) / (3 * stdev),
    )
    # return (1 - k) * C_p


# def standard_deviation(stdev_i: float, n: float) -> float:
#     return stdev_i / n**0.5


def RSS_func(*args):
    """
    Root sum square.

    >>> RSS_func(1, 2, 3)
    3.7416573867739413
    """
    return (sum([arg**2 for arg in args])) ** 0.5


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


def norm_cdf(x, mu=0, stdev=1):
    """
    Cumulative distribution function for the normal distribution.

    >>> norm_cdf(0)
    0.5
    >>> norm_cdf(1)
    0.8413447460685428
    >>> norm_cdf(2)
    0.9772498680518209
    """
    return 0.5 * (1 + math.erf((x - mu) / (stdev * (2**0.5))))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
