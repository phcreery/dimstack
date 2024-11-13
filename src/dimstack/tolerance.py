from .utils import nround, sign_symbol


class SymmetricBilateral:
    """Bilateral tolerancing is a method of specifying a tolerance that is symmetrical about the nominal value.
    This is the most common type of tolerancing.
    """

    def __init__(self, tol: float):
        self._tol = abs(tol)

    def __repr__(self) -> str:
        return f"SymmetricBilateral({self._tol})"

    def __str__(self) -> str:
        return f"± {nround(self.T/2)}"

    @property
    def upper(self):
        return self._tol

    @property
    def lower(self):
        return -self._tol

    @property
    def T(self):
        return 2 * self._tol


class UnequalBilateral:
    """Bilateral tolerancing is a method of specifying a tolerance that is asymmetrical about the nominal value.
    This can also be used for Unilateral tolerancing.
    """

    def __init__(self, upper: float, lower: float):
        if upper < lower:
            self.upper = lower
            self.lower = upper
        else:
            self.upper = upper
            self.lower = lower

    def __repr__(self) -> str:
        return f"UnequalBilateral({self.upper}, {self.lower})"

    def __str__(self) -> str:
        return (
            f"{sign_symbol(self.upper)} {nround(abs(self.upper))} / {sign_symbol(self.lower)} {nround(abs(self.lower))}"
        )

    @property
    def T(self):
        return self.upper - self.lower


def Bilateral(upper: float, lower: float = None):
    """Automatically determine the type of bilateral tolerance to use from the upper and lower inputs.

    Args:
        upper (float): _description_
        lower (float, optional): _description_. Defaults to None.

    Returns:
        (SymmetricBilateral | UnequalBilateral): _description_
    """
    if lower is None:
        return SymmetricBilateral(upper)
    else:
        if upper == lower:
            return SymmetricBilateral(upper)
        else:
            return UnequalBilateral(upper, lower)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
