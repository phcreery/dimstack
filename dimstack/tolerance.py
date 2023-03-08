from typing import List, Union
import math
import numpy as np
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

POSITIVE = "+"
NEGATIVE = "-"
DECIMALS = 4
DIST_NORMAL = "Normal"  # Normal distribution.
DIST_SCREENED = "Screened"  # Normal distribution which has been screened. e.g. Go-NoGo or Pass-Fail fixture.
DIST_NOTCHED = "Notched"  # This is a common distribution when parts are being sorted and the leftover parts are used
DIST_NORMAL_LT = "Normal LT"  # Normal distribution which has been screened in order to remove lengths above a limit.
DIST_NORMAL_GT = "Normal GT"  # Normal distribution which has been screened in order to remove lengths below a limit.

DISPLAY_MODE = "plot"  # "text" or "plot" or "df"
FIGSIZE = (6, 3)


def display_mode(mode: str):
    """Set the display mode for the stack.

    Args:
        mode (str): "text" or "plot"
    """
    global DISPLAY_MODE
    DISPLAY_MODE = mode


def display_df(df: pd.DataFrame, title: str = None):
    """Display a dataframe.

    Args:
        df (pd.DataFrame): _description_
    """
    if DISPLAY_MODE == "text":
        print(f"{title}")
        print(df.to_string(index=False))
        print()
    elif DISPLAY_MODE == "plot":
        return display(df.style.hide(axis="index").set_caption(title))
    elif DISPLAY_MODE == "df":
        return df


def round(x, n=DECIMALS):
    return np.around(x, decimals=n)


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
        k (float): ratio of the amount the center of the distribution is shifted from the nominal value to the standard deviation.

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
    return (sum([arg ** 2 for arg in args])) ** 0.5


def C_f(t_rss, t_wc, n):
    return ((0.5 * (t_wc - t_rss)) / (t_rss * (n ** 0.5 - 1))) + 1


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
    return 0.5 * (1 + math.erf((x - mu) / (sigma * (2 ** 0.5))))


class Closed:
    def __init__(self, stack: "Stack"):
        self.stack = stack

    @property
    def nominal(self):
        return sum([item.nominal * item.a for item in self.stack.items])

    @property
    def tolerance(self) -> Union["SymmetricBilateral", "UnequalBilateral"]:
        return Bilateral(
            sum(
                filter(
                    None, [item.tolerance_absolute.upper for item in self.stack.items]
                )
            ),
            sum(
                filter(
                    None, [item.tolerance_absolute.lower for item in self.stack.items]
                )
            ),
        )

    def show(self):
        """This is a simple Worst-Case calculation"""
        title = f"Closed Stack - {self.stack.title}"
        df = pd.DataFrame(
            [
                {
                    "Value": round(self.nominal),
                    "Tolerance": f"{self.tolerance}",
                    "Bounds": f"[{round(self.nominal-self.tolerance.lower)} {round(self.nominal+self.tolerance.upper)}]",
                }
            ]
        ).astype(str)

        display_df(df, title)


class WC:
    def __init__(self, stack: "Stack"):
        self.stack = stack

    @property
    def mu(self):
        return self.stack.mu

    @property
    def sigma(self):
        return self.stack.sigma

    @property
    def tolerance(self) -> Union["SymmetricBilateral", "UnequalBilateral"]:
        upper = sum(
            filter(None, [item.tolerance_absolute.upper for item in self.stack.items])
        )
        lower = sum(
            filter(None, [item.tolerance_absolute.lower for item in self.stack.items])
        )
        return Bilateral((upper + lower) / 2)

    @property
    def Z_min(self):
        return self.mu - self.tolerance.lower

    @property
    def Z_max(self):
        return self.mu + self.tolerance.upper

    def show(self):
        """This is a simple Worst-Case calculation"""
        title = f"Worst Case - {self.stack.title}"
        df = pd.DataFrame(
            [
                {
                    "Value": round(self.mu),
                    "Tolerance": f"{self.tolerance}",
                    "Bounds": f"[{round(self.Z_min)} {round(self.Z_max)}]",
                }
            ]
        ).astype(str)

        display_df(df, title)


class RSS:
    """
    This is a simple RSS calculation. This is uses the RSS calculation method in the Dimensioning and Tolerancing Handbook, McGraw Hill.
    It is really only useful for a Bilateral stack of same process-sigma items. The RSS result has the same uncertainty as the measurements.
    Historically, Eq. (9.11) assumed that all of the component tolerances (t_i) represent a 3si value for their
    manufacturing processes. Thus, if all the component distributions are assumed to be normal, then the
    probability that a dimension is between ±t_i is 99.73%. If this is true, then the assembly gap distribution is
    normal and the probability that it is ±t_rss between is 99.73%.
    Although most people have assumed a value of ±3s for piecepart tolerances, the RSS equation works
    for “equal s” values. If the designer assumed that the input tolerances were ±4s values for the piecepart
    manufacturing processes, then the probability that the assembly is between ±t_rss is 99.9937 (4s).
    The 3s process limits using the RSS Model are similar to the Worst Case Model. The minimum gap is
    equal to the mean value minus the RSS variation at the gap. The maximum gap is equal to the mean value
    plus the RSS variation at the gap.

    # Dimensioning and Tolerancing Handbook, McGraw Hill
    # http://files.engineering.com/getfile.aspx?folder=69759f43-e81a-4801-9090-a0c95402bfc0&file=RSS_explanation.GIF
    """

    def __init__(self, stack: "Stack") -> None:
        self.stack = stack

        # check if all items are the same process_sigma
        # if len(set([item.process_sigma for item in self.items])) > 1:
        #     raise ValueError(
        #         "For simple RSS analysis, all items must have the same process_sigma"
        #     )

        # Convert all dimensions to mean dimensions with an equal bilateral tolerance

    @property
    def d_g(self):
        return self.stack.mu

    @property
    def mu(self):
        return self.stack.mu

    @property
    def t_wc(self):
        return sum([abs(item.a * (item.tolerance.T / 2)) for item in self.stack.items])

    @property
    def t_rss(self):
        return RSS_func(*[item.a * (item.tolerance.T / 2) for item in self.stack.items])

    @property
    def t_mrss(self):
        n = len(self.stack.items)
        C_f = (0.5 * (self.t_wc - self.t_rss)) / (self.t_rss * (np.sqrt(n) - 1)) + 1
        return C_f * self.t_rss

    # def yield_loss_probability(self, UL, LL):
    #     return 1 - norm_cdf(UL, self.mu, self.sigma) + norm_cdf(LL, self.mu, self.sigma)

    # def yield_probability(self, UL, LL):
    #     return 1 - self.yield_loss_probability(UL, LL)

    def show(self):
        title = f"RSS - {self.stack.title}"
        df = pd.DataFrame(
            [
                # {
                #     "Name": "Worst Case",
                #     "Value": round(self.d_g),
                #     "Tolerance".ljust(14, " "): f"± {str(round(self.t_wc))}".ljust(
                #         14, " "
                #     ),
                #     "Bounds".ljust(
                #         20, " "
                #     ): f"[{round(self.d_g-self.t_wc)} {round(self.d_g+self.t_wc)}]".ljust(
                #         20, " "
                #     ),
                # },
                {
                    "Name": "Modified RSS",
                    "Value": round(self.d_g),
                    "Tolerance".ljust(14, " "): f"± {str(round(self.t_mrss))}".ljust(
                        14, " "
                    ),
                    "Bounds".ljust(
                        20, " "
                    ): f"[{round(self.d_g-self.t_mrss)} {round(self.d_g+self.t_mrss)}]".ljust(
                        20, " "
                    ),
                },
                {
                    "Name": "RSS",
                    "Value": round(self.d_g),
                    "Tolerance".ljust(14, " "): f"± {str(round(self.t_rss))}".ljust(
                        14, " "
                    ),
                    "Bounds".ljust(
                        20, " "
                    ): f"[{round(self.d_g-self.t_rss)} {round(self.d_g+self.t_rss)}]".ljust(
                        20, " "
                    ),
                },
            ]
        ).astype(str)

        display_df(df, title)


class SixSigma:
    def __init__(self, stack: "Stack") -> None:
        self.stack = stack

    @property
    def mu(self):
        return self.stack.mu

    @property
    def sigma(self):
        return self.stack.sigma

    def yield_loss_probability(self, UL, LL):
        return 1 - norm_cdf(UL, self.mu, self.sigma) + norm_cdf(LL, self.mu, self.sigma)

    def yield_probability(self, UL, LL):
        return 1 - self.yield_loss_probability(UL, LL)

    def show(self):
        # https://www.mitcalc.com/doc/tolanalysis1d/help/en/tolanalysis1d.htm
        title = f"'6 sigma' - {self.stack.title}"
        df = pd.DataFrame(
            [
                {
                    "Sigma": f"± {i}σ",
                    "Mean": round(self.mu),
                    "Tolerance": f"± {round(self.sigma * i)}",
                    "Bounds": f"[{round(self.mu-self.sigma*i)} {round(self.mu+self.sigma*i)}]",
                    "Yield Probability": f"{round(self.yield_probability(self.mu+self.sigma*i, self.mu-self.sigma*i)*100, 8)}",
                    "Reject PPM": f"{round(self.yield_loss_probability(self.mu+self.sigma*i, self.mu-self.sigma*i)*1000000, 2)}",
                }
                for i in [6, 5, 4.5, 4, 3]
            ]
        ).astype(str)

        display_df(df, title)
        print(f"μ = {round(self.mu)}")
        print(f"σ = {round(self.sigma)}")


class SymmetricBilateral:
    """Bilateral tolerancing is a method of specifying a tolerance that is symmetrical about the nominal value.
    This is the most common type of tolerancing.
    """

    def __init__(self, tol: float):
        self._tol = abs(tol)

    def __repr__(self) -> str:
        return f"± {round(self.T/2)}"

    @property
    def upper(self):
        return self._tol

    @property
    def lower(self):
        return self._tol

    @property
    def T(self):
        return 2 * self._tol


class UnequalBilateral:
    """
    Bilateral tolerancing is a method of specifying a tolerance that is asymmetrical about the nominal value.
    This can also be used for Unilateral tolerancing.
    """

    def __init__(self, upper: float, lower: float):
        upper = abs(upper)
        lower = abs(lower)
        # if upper < lower:
        #     upper, lower = lower, upper
        self.upper = upper
        self.lower = lower

    def __repr__(self) -> str:
        return f"+ {round(self.upper)} / - {round(self.lower)}"

    # @property
    # def tol(self):
    #     return (self.upper - self.lower) / 2

    @property
    def T(self):
        return self.upper - self.lower


def Bilateral(upper: float, lower: float = None):
    if lower is None:
        return SymmetricBilateral(upper)
    else:
        if upper == lower:
            return SymmetricBilateral(upper)
        else:
            return UnequalBilateral(upper, lower)


class Dimension:
    """
    A measurement is a single measurement of a part.

    Args:
        nom (float, optional): The nominal value of the measurement. Defaults to 0.
        tol (Union[SymmetricBilateral, UnequalBilateral], optional): The tolerance of the measurement. Defaults to SymmetricBilateral(0).
        a (float, optional): The sensitivity of the measurement. Defaults to 1. If the nominal value is negative, the sensitivity will be multiplied by a -1 and the nominal value will be made positive.
        process_sigma (float, optional): The standard deviation of the process represented as ±σ. Defaults to ±3σ.
        k (float, optional): The ratio of the amount the center of the distribution is shifted from the mean represented as a multiple of the process standard deviation. Defaults to 0σ.
        distribution (str, optional): The distribution of the measurement. Defaults to "Normal".
        name (str, optional): The name of the measurement. Defaults to "Dimension".
        desc (str, optional): The description of the measurement. Defaults to "Dimension".
    """

    newID = itertools.count().__next__

    def __init__(
        self,
        nom: float,
        tol: Union[SymmetricBilateral, UnequalBilateral],
        a: float = 1,
        process_sigma: float = 3,
        k: float = 0,
        distribution: str = "Normal",
        name: str = "Dimension",
        desc: str = "Dimension",
    ):
        self.id = Dimension.newID()
        self.nominal = abs(nom)
        self.tolerance = tol
        self.a = a * sign(nom)  # sensitivity
        self.process_sigma = process_sigma
        self.k = k
        self.distribution = distribution
        self.name = name
        self.description = desc

    def __repr__(self) -> str:
        return f"{self.id}: {self.name} {self.description} {self.direction}{round(self.nominal)} {repr(self.tolerance)} @ ± {self.process_sigma}σ (σ={self.sigma})"

    @property
    def direction(self):
        if self.a >= 0:
            return POSITIVE
        else:
            return NEGATIVE

    @property
    def tolerance_absolute(self):
        if self.direction == POSITIVE:
            return self.tolerance
        elif self.direction == NEGATIVE:
            return Bilateral(self.tolerance.lower, self.tolerance.upper)

    @property
    def lower_rel(self):
        return self.nominal - self.tolerance.lower

    @property
    def upper_rel(self):
        return self.nominal + self.tolerance.upper

    @property
    def mu(self):
        return self.nominal

    @property
    def sigma(self):
        return abs(self.tolerance.T / 2) / self.process_sigma

    # @property
    # def variance(self):
    #     return self.sigma ** 2

    @property
    def C_p(self):
        return C_p(self.upper_rel, self.lower_rel, self.sigma)

    @property
    def C_pk(self):
        return C_pk(self.C_p, self.k)

    @property
    def mu_eff(self):
        """effective mean"""
        return (self.lower_rel + self.upper_rel) / 2

    @property
    def sigma_eff(self):
        """
        effective standard deviation
        "6 sigma" is the standard deviation of the distribution
        """
        return abs(self.tolerance.T) / (6 * self.C_pk)


class Stack:
    def __init__(self, title: str = "Stack", items: List[Dimension] = []):
        self.title = title
        self.items = items

    def __repr__(self) -> str:
        return f"{self.title}"

    def append(self, measurement: Dimension):
        self.items.append(measurement)

    @property
    def mu(self):
        return sum([item.mu_eff * item.a for item in self.items])

    @property
    def sigma(self):
        return RSS_func(*[item.sigma_eff * item.a for item in self.items])

    @property
    def Closed(self) -> Closed:
        return Closed(self)

    @property
    def WC(self) -> WC:
        return WC(self)

    @property
    def RSS(self) -> RSS:
        return RSS(self)

    @property
    def SixSigma(self) -> SixSigma:
        return SixSigma(self)

    def show(self):
        # members = [attr for attr in dir(obj()) if not callable(getattr(obj(),attr)) and not attr.startswith("__")]
        df = pd.DataFrame(
            [
                {
                    "id": item.id,
                    "name": item.name,
                    "description": (item.description),
                    "dir": item.direction,
                    "nominal": round(item.nominal),
                    "tolerance": (repr(item.tolerance)).ljust(14, " "),
                    "process_sigma": f"± {str(item.process_sigma)}σ",
                    "sensitivity": str(item.a),
                    "relative bounds": f"[{round(item.lower_rel)}, {round(item.upper_rel)}]",
                    # "absolute bounds": f"[{round(item.lower_rel)}, {round(item.max_rel)}]",
                    # "lower_rel": round(item.lower_rel),
                    # "max_rel": round(item.max_rel),
                    # "lower_rel": round(item.lower_rel),
                    # "max_rel": round(item.max_rel),
                    "σ": round(item.sigma),
                    "C_p": round(item.C_p),
                    "k": round(item.k),
                    "C_pk": round(item.C_pk),
                    "μ_eff": round(item.mu_eff),
                    "σ_eff": round(item.sigma_eff),
                }
                for item in self.items
            ]
        ).astype(str)

        display_df(df, self.title)

    def show_length_chart(self):
        fig, axs = plt.subplots(1, 1, figsize=FIGSIZE, dpi=200)
        axs.grid()
        axs.set_axisbelow(True)
        axs.axvline(0, label="DATUM", alpha=0.6)

        # determine rough plot length to size the arrow heads
        max = 0
        min = 0
        last_part_x = 0
        for item in self.items:
            last_part_x = last_part_x + item.nominal * item.a
            if last_part_x > max:
                max = last_part_x
            if last_part_x < min:
                min = last_part_x
        head_width = (max + min) * 0.001
        # head_width = 0.1

        # draw arrows
        num_of_parts = len(self.items)
        last_part_x = 0
        for i in range(num_of_parts):
            item = self.items[i]
            axs.arrow(
                x=last_part_x,
                dx=item.nominal * item.a,
                y=i,
                dy=0,
                width=head_width / 5,
                length_includes_head=True,
                head_width=head_width,
                head_length=head_width * 50,
                color=(0, 0, 0),
            )

            last_part_x = last_part_x + item.nominal * item.a
        axs.set_yticks(range(len(self.items)))
        axs.set_yticklabels([item.name for item in self.items])
        axs.invert_yaxis()
        axs.set_title("Nominal Stackup Flow Chart")
        axs.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

        fig.tight_layout()

        # return fig


if __name__ == "__main__":
    import doctest

    doctest.testmod()
