from .utils import nround, sign_symbol
import numpy as np


class Bilateral:
    """
    Bilateral tolerancing is a method of specifying a tolerance that is symmetrical about the nominal value.
    This is the most common type of tolerancing.
    """

    def __init__(self, upper: float, lower: float):
        if upper < lower:
            self._upper = lower
            self._lower = upper
        else:
            self._upper = upper
            self._lower = lower

    def __str__(self) -> str:
        if np.abs(self._upper + self._lower) < np.finfo(float).eps:
            return f"± {nround(self._upper)}"
        else:
            return f"{sign_symbol(self._upper)}{nround(abs(self._upper))} / {sign_symbol(self._lower)}{nround(abs(self._lower))}"

    @classmethod
    def symmetric(cls, tol: float):
        return cls(tol, -tol)

    @classmethod
    def asymmetric(cls, upper: float, lower: float):
        """
        Create a bilateral tolerance with different upper and lower bounds
        """
        return cls(upper, lower)

    @classmethod
    def unequal(cls, upper: float, lower: float):
        """
        Create a bilateral tolerance with different upper and lower bounds
        alias for `asymmetric`
        """
        return cls.asymmetric(upper, lower)

    @property
    def upper(self):
        return self._upper

    @property
    def lower(self):
        return self._lower

    @property
    def T(self):
        return self._upper - self._lower


if __name__ == "__main__":
    import doctest

    doctest.testmod()
