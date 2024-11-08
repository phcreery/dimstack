from decimal import ROUND_HALF_UP, Decimal

DECIMALS = 5
POSITIVE = "+"
NEGATIVE = "-"


def nround(number, ndigits=DECIMALS):
    """
    Always round off
    >>> nround(4.114, 2)
    4.11
    >>> nround(4.115, 2)
    4.12
    >>> nround(4.116, 2)
    4.12
    >>> nround(-0.03401, 3)
    -0.034
    """
    # return round(number, ndigits)

    # https://stackoverflow.com/questions/43851273/how-to-round-float-0-5-up-to-1-0-while-still-rounding-0-45-to-0-0-as-the-usual
    exp = Decimal("1.{}".format(ndigits * "0")) if ndigits else Decimal("1")
    return type(number)(Decimal(number).quantize(exp, ROUND_HALF_UP))


def sign(x):
    """Return the sign of x, i.e. -1, 0 or 1.

    >>> sign(0)
    0
    >>> sign(10)
    1
    >>> sign(-10)
    -1
    """
    x = float(x)
    return (x > 0) - (x < 0)


def sign_symbol(x):
    """Return the sign of x, i.e. + or -.

    >>> sign_symbol(0)
    '+'
    >>> sign_symbol(10)
    '+'
    >>> sign_symbol(-10)
    '-'

    Args:
        x (float)

    Returns:
        string: "+", "-"
    """
    if x >= 0:
        return POSITIVE
    else:
        return NEGATIVE


if __name__ == "__main__":
    import doctest

    doctest.testmod()
