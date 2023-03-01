from typing import List, Union
import numpy as np
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

POSITIVE = "+"
NEGATIVE = "-"
DECIMALS = 5
DIST_NORMAL = "Normal"  # Normal distribution.
DIST_SCREENED = "Screened"  # Normal distribution which has been screened. e.g. Go-NoGo or Pass-Fail fixture.
DIST_NOTCHED = "Notched"  # This is a common distribution when parts are being sorted and the leftover parts are used
DIST_NORMAL_LT = "Normal LT"  # Normal distribution which has been screened in order to remove lengths above a limit.
DIST_NORMAL_GT = "Normal GT"  # Normal distribution which has been screened in order to remove lengths below a limit.

DISPLAY_MODE = "plot"  # "text" or "plot"
FIGSIZE = (6, 3)


def display_mode(mode: str):
    """Set the display mode for the stack.

    Args:
        mode (str): "text" or "plot"
    """
    global DISPLAY_MODE
    DISPLAY_MODE = mode


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


def C_p(UL: float, LL: float, sigma: float) -> float:
    """Process capability index.

    Args:
        UL (int): _description_
        LL (int): _description_
        sigma (int): _description_

    Returns:
        float: _description_
    """
    return (UL - LL) / (6 * sigma)


def C_pk(C_p: float, k: float) -> float:
    """Process capability index. adjusted for centering.
    Cpl = (mu - L)/3*sigma
    Cpu = (U - mu)/3*sigma
    C_pk = min(Cpl, Cpu) = (1 - k) * C_p

    Args:
        C_p (float): Process capability index.
        k (float): ratio of the amount the center of the distribution is shifted from the nominal value to the standard deviation.

    Returns:
        float: Process capability index.
    """
    return (1 - k) * C_p


# def sigma_i(T_i: float, sigma: float) -> float:
#     return T_i / sigma


# def standard_deviation(sigma_i: float, n: float) -> float:
#     return sigma_i / n**0.5


def RSS(*args):
    return (sum([arg ** 2 for arg in args])) ** 0.5


def C_f(t_rss, t_wc, n):
    return ((0.5 * (t_wc - t_rss)) / (t_rss * (n ** 0.5 - 1))) + 1


class SymmetricBilateral:
    """Bilateral tolerancing is a method of specifying a tolerance that is symmetrical about the nominal value.
    This is the most common type of tolerancing.
    """

    def __init__(self, tol: float):
        self.tol = tol

    def __repr__(self) -> str:
        return f"± {round(self.tol)}"

    @property
    def lower(self):
        return self.tol

    @property
    def upper(self):
        return self.tol

    @property
    def T(self):
        return 2 * self.tol


class UnequalBilateral:
    """Bilateral tolerancing is a method of specifying a tolerance that is asymmetrical about the nominal value.
    This can also be used for Unilateral tolerancing.
    """

    def __init__(self, upper: float, lower: float):
        self.upper = upper
        self.lower = lower

    def __repr__(self) -> str:
        return f"+ {round(self.upper)} / - {round(self.lower)}"

    @property
    def tol(self):
        return (self.upper - self.lower) / 2

    @property
    def T(self):
        return self.upper - self.lower


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
        nom: float = 0,
        tol: Union[SymmetricBilateral, UnequalBilateral] = SymmetricBilateral(0),
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
        return f"{self.id}: {self.direction}{round(self.nominal)} {repr(self.tolerance)} {self.sigma}σ {self.name} {self.description}"

    @property
    def direction(self):
        if self.a >= 0:
            return POSITIVE
        else:
            return NEGATIVE

    @property
    def upper_abs(self):
        if self.direction == POSITIVE:
            return self.tolerance.upper
        elif self.direction == NEGATIVE:
            return self.tolerance.lower

    @property
    def lower_abs(self):
        if self.direction == POSITIVE:
            return self.tolerance.lower
        elif self.direction == NEGATIVE:
            return self.tolerance.upper

    @property
    def min_rel(self):
        return self.a * (self.nominal - self.tolerance.lower)

    @property
    def max_rel(self):
        return self.a * (self.nominal + self.tolerance.upper)

    @property
    def min_abs(self):
        return self.nominal - self.tolerance.lower

    @property
    def max_abs(self):
        return self.nominal + self.tolerance.upper

    @property
    def sigma(self):
        return abs(self.tolerance.T / 2) / self.process_sigma

    @property
    def C_p(self):
        return C_p(self.max_abs, self.min_abs, self.sigma)

    @property
    def C_pk(self):
        return C_pk(self.C_p, self.k)

    @property
    def mu_eff(self):
        """effective mean"""
        return (self.max_abs + self.min_abs) / 2

    @property
    def sigma_eff(self):
        """effective standard deviation"""
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
    def nominal(self):
        return sum([item.nominal * item.a for item in self.items])

    @property
    def mu(self):
        return sum([item.mu_eff * item.a for item in self.items])

    @property
    def sigma(self):
        return RSS(*[item.sigma_eff * item.a for item in self.items])

    @property
    def tol_stack_upper(self):
        return [item.upper_abs for item in self.items]

    @property
    def tol_stack_lower(self):
        return [item.lower_abs for item in self.items]

    @property
    def t_wc_upper(self) -> float:
        return sum(filter(None, self.tol_stack_upper))

    @property
    def t_wc_lower(self) -> float:
        return sum(filter(None, self.tol_stack_lower))

    def df(self):
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
                    "process_sigma": "±" + str(item.process_sigma) + "σ",
                    "sensitivity": str(item.a),
                    "σ": round(item.sigma),
                    # "min_rel": round(item.min_rel),
                    # "max_rel": round(item.max_rel),
                    "min_abs": round(item.min_abs),
                    "max_abs": round(item.max_abs),
                    "C_p": round(item.C_p),
                    "k": item.k,
                    "C_pk": round(item.C_pk),
                    "μ_eff": round(item.mu_eff),
                    "σ_eff": round(item.sigma_eff),
                }
                for item in self.items
            ]
        )
        return df

    def show(self):
        if DISPLAY_MODE == "text":
            print(f"{self.title}")
            print(self.df().to_string(index=False))
        elif DISPLAY_MODE == "plot":
            return display(self.df())

    def show_results_text_WC(self):
        """This is a simple Worst-Case calculation"""
        s = "--[Worst Case]--------------------------------\n"
        s += f"{round(self.nominal)} +{round(self.t_wc_upper)}/-{round(self.t_wc_lower)} [{round(self.nominal-self.t_wc_lower)} {round(self.nominal+self.t_wc_upper)}] Worst Case"
        print(s)

    def show_results_text_RSS_simple(self):
        """This is a simple RSS calculation. This is uses the RSS calculation method in the Dimensioning and Tolerancing Handbook, McGraw Hill.
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
        """
        # Dimensioning and Tolerancing Handbook, McGraw Hill
        # http://files.engineering.com/getfile.aspx?folder=69759f43-e81a-4801-9090-a0c95402bfc0&file=RSS_explanation.GIF

        # check if all items are the same process_sigma
        # if len(set([item.process_sigma for item in self.items])) > 1:
        #     raise ValueError(
        #         "For simple RSS analysis, all items must have the same process_sigma"
        #     )

        # Convert all dimensions to mean dimensions with an equal bilateral tolerance
        d_g = self.mu
        t_wc = []
        t_rss = []
        for item in self.items:
            a = item.a
            t = item.tolerance.tol
            t_wc.append(abs(a * t))
            t_rss.append((a ** 2) * (t ** 2))

        t_wc = sum(t_wc)
        t_rss = RSS(*t_rss)
        n = len(self.items)
        C_f = (0.5 * (t_wc - t_rss)) / (t_rss * (np.sqrt(n) - 1)) + 1
        t_mrss = C_f * t_rss

        s = "--[RSS assuming uniform process variation]----\n"
        s += f"{round(d_g)} ± {round(t_wc)} [{round(d_g-t_wc)} {round(d_g+t_wc)}] Worst Case \n"
        s += f"{round(d_g)} ± {round(t_mrss)} [{round(d_g-t_mrss)} {round(d_g+t_mrss)}] Modified RSS \n"
        s += (
            f"{round(d_g)} ± {round(t_rss)} [{round(d_g-t_rss)} {round(d_g+t_rss)}] RSS"
        )
        print(s)

    def show_results_text_RSS(self):
        # https://www.mitcalc.com/doc/tolanalysis1d/help/en/tolanalysis1d.htm
        # sigma = RSS(*[item.sigma_eff * item.a for item in self.items])
        sigma = self.sigma
        s = "--['6 Sigma']---------------------------------\n"
        s += f"μ = {round(self.mu)}\n"
        s += f"σ = {round(sigma)}\n"
        for i in [6, 5, 4.5, 4, 3]:
            s += f"{round(self.mu)} ± {round(sigma*i)} [{round(self.mu-sigma*i)} {round(self.mu+sigma*i)}] ±{i}σ \n"
        print(s)

    # def show_results_text_six_sigma(self):
    #     # https://www.mitcalc.com/doc/tolanalysis1d/help/en/tolanalysis1d.htm
    #     s = "----------------------------------------\n"
    #     # s += f"{}\n"

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
