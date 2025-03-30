from .utils import nround, sign_symbol


# class Bilateral.symmetric:
#     """Bilateral tolerancing is a method of specifying a tolerance that is symmetrical about the nominal value.
#     This is the most common type of tolerancing.
#     """

#     def __init__(self, tol: float):
#         self._tol = abs(tol)

#     def __repr__(self) -> str:
#         return f"Bilateral.symmetric({self._tol})"

#     def __str__(self) -> str:
#         return f"± {nround(self.T/2)}"

#     @property
#     def upper(self):
#         return self._tol

#     @property
#     def lower(self):
#         return -self._tol

#     @property
#     def T(self):
#         return 2 * self._tol


# class Bilateral.unequal:
#     """Bilateral tolerancing is a method of specifying a tolerance that is asymmetrical about the nominal value.
#     This can also be used for Unilateral tolerancing.
#     """

#     def __init__(self, upper: float, lower: float):
#         if upper < lower:
#             self.upper = lower
#             self.lower = upper
#         else:
#             self.upper = upper
#             self.lower = lower

#     def __repr__(self) -> str:
#         return f"Bilateral.unequal({self.upper}, {self.lower})"

#     def __str__(self) -> str:
#         return (
#             f"{sign_symbol(self.upper)}{nround(abs(self.upper))} / {sign_symbol(self.lower)}{nround(abs(self.lower))}"
#         )

#     @property
#     def T(self):
#         return self.upper - self.lower


# def Bilateral(upper: float, lower: float | None = None):
#     """Automatically determine the type of bilateral tolerance to use from the upper and lower inputs.

#     Args:
#         upper (float): _description_
#         lower (float, optional): _description_. Defaults to None.

#     Returns:
#         (Bilateral.symmetric | Bilateral.unequal): _description_
#     """
#     if lower is None:
#         return Bilateral.symmetric(upper)
#     else:
#         if upper == lower:
#             return Bilateral.symmetric(upper)
#         else:
#             return Bilateral.unequal(upper, lower)


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
        if self._upper == self._lower:
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
