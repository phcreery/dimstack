DECIMALS = 5


def nround(x, n=DECIMALS):
    return round(x, n)


def sign(x):
    """Return the sign of x, i.e. -1, 0 or 1.

    >>> sign(0)
    0
    >>> sign(10)
    1
    >>> sign(-10)
    -1
    """
    return (x > 0) - (x < 0)
