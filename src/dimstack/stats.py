import math

# from statistics import mean, stdev


# "6 Sigma" equations.


def C_p(UL: float, LL: float, sigma: float) -> float:
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
    return (UL - LL) / (6 * sigma)


def C_pk(C_p: float, k: float) -> float:
    """
    Process capability index. adjusted for centering.
    Cpl = (mu - L)/3*sigma
    Cpu = (U - mu)/3*sigma
    C_pk = min(Cpl, Cpu) = (1 - k) * C_p

    Args:
        C_p (float): Process capability index.
        k (float): ratio of the amount the center of the distribution is shifted
                    from the nominal value to the standard deviation.

    Returns:
        float: Process capability index.

    >>> C_pk(1, 0)
    1
    """
    return (1 - k) * C_p


# def sigma_i(T_i: float, sigma: float) -> float:
#     return T_i / sigma


# def standard_deviation(sigma_i: float, n: float) -> float:
#     return sigma_i / n**0.5


def RSS_func(*args):
    """
    Root sum square.

    >>> RSS_func(1, 2, 3)
    3.7416573867739413
    """
    return (sum([arg**2 for arg in args])) ** 0.5


def C_f(t_rss, t_wc, n):
    return ((0.5 * (t_wc - t_rss)) / (t_rss * (n**0.5 - 1))) + 1


def norm_cdf(x, mu=0, sigma=1):
    """
    Cumulative distribution function for the normal distribution.

    >>> norm_cdf(0)
    0.5
    >>> norm_cdf(1)
    0.8413447460685428
    >>> norm_cdf(2)
    0.9772498680518209
    """
    return 0.5 * (1 + math.erf((x - mu) / (sigma * (2**0.5))))

if __name__ == "__main__":
    import doctest
    doctest.testmod()