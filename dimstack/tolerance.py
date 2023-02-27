from typing import List, Union
import numpy as np
import itertools
import pandas as pd

POSITIVE = "+"
NEGATIVE = "-"
DECIMALS = 5
DIST_NORMAL = "Normal"  # Normal distribution.
DIST_SCREENED = "Screened"  # Normal distribution which has been screened. e.g. Go-NoGo or Pass-Fail fixture.
DIST_NOTCHED = "Notched"  # This is a common distribution when parts are being sorted and the leftover parts are used
DIST_NORMAL_LT = "Normal LT"  # Normal distribution which has been screened in order to remove lengths above a limit.
DIST_NORMAL_GT = "Normal GT"  # Normal distribution which has been screened in order to remove lengths below a limit.


def C_p(sigma: int, UL: int, LL: int) -> float:
    return (UL - LL) / (6 * sigma)


def C_pk(C_p: float, k: float) -> float:
    return (1 - k) * C_p


def sigma_i(T_i: int, sigma: int) -> float:
    return T_i / sigma


def standard_deviation(sigma_i: float, n: int) -> float:
    return sigma_i / n**0.5


def RSS(*args):
    return (sum([arg**2 for arg in args])) ** 0.5


def round(x, n=DECIMALS):
    return np.around(x, decimals=n)


def C_f(t_rss, t_wc, n):
    return ((0.5 * (t_wc - t_rss)) / (t_rss * (n**0.5 - 1))) + 1


class Bilateral:
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


class Unilateral:
    def __init__(self, upper: float, lower: float):
        self.upper = upper
        self.lower = lower

    def __repr__(self) -> str:
        return f"+{round(self.upper)}/-{round(self.lower)}"

    @property
    def tol(self):
        return (self.upper - self.lower) / 2

    @property
    def T(self):
        return self.upper - self.lower


class Measurement:
    newID = itertools.count().__next__

    def __init__(
        self,
        nom: int = 0,
        tol: Union[Unilateral, Bilateral] = Bilateral(0),
        process_sigma: int = 6,
        k: int = 0,
        distribution: str = "Normal",
        name: str = "Measurement",
        desc: str = "Measurement",
    ):
        self.id = Measurement.newID()
        self.nominal = nom
        self.tolerance = tol
        self.process_sigma = process_sigma
        self.k = k
        self.distribution = distribution
        self.name = name
        self.description = desc

    def __repr__(self) -> str:
        return f"{self.id}: {self.direction}{round(self.distance)} {repr(self.tolerance)} {self.sigma}σ {self.name} {self.description}"

    @property
    def distance(self):
        return np.abs(self.nominal)

    @property
    def direction(self):
        if self.nominal >= 0:
            return POSITIVE
        else:
            return NEGATIVE

    @property
    def j(self):
        """The variable name j represents the direction. j is either -1 or 1.

        Returns:
            int: direction multiplier
        """
        if self.direction == POSITIVE:
            return 1
        elif self.direction == NEGATIVE:
            return -1

    @property
    def T(self):
        return self.tolerance.T

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
        return self.j * (self.distance - self.tolerance.lower)

    @property
    def max_rel(self):
        return self.j * (self.distance + self.tolerance.upper)

    @property
    def min_abs(self):
        # return self.distance - self.T / 2
        return self.distance - self.tolerance.lower

    @property
    def max_abs(self):
        # return self.distance + self.T / 2
        return self.distance + self.tolerance.upper

    @property
    def sigma(self):
        return abs(self.T / 2) / self.process_sigma

    @property
    def C_p(self):
        return C_p(self.sigma, self.max_abs, self.min_abs)

    @property
    def C_pk(self):
        return C_pk(self.C_p, self.k)

    @property
    def mu_eff(self):
        return (self.max_abs + self.min_abs) / 2

    @property
    def sigma_eff(self):
        return abs(self.T) / (6 * self.C_pk)


class Stack:
    def __init__(self, title: str = "Stack", items: List[Measurement] = []):
        self.title = title
        self.items = items

    def __repr__(self) -> str:
        return f"{self.title}"

    def append(self, measurement: Measurement):
        self.items.append(measurement)

    @property
    def nom_stack(self):
        return [item.nominal for item in self.items]

    @property
    def tol_stack_upper(self):
        return [item.upper_abs for item in self.items]

    @property
    def tol_stack_lower(self):
        return [item.lower_abs for item in self.items]

    @property
    def d_g(self):
        return sum(self.nom_stack)

    @property
    def t_wc_upper(self):
        return sum(self.tol_stack_upper)

    @property
    def t_wc_lower(self):
        return sum(self.tol_stack_lower)

    @property
    def t_rss_upper(self):
        return RSS(*self.tol_stack_upper)

    @property
    def t_rss_lower(self):
        return RSS(*self.tol_stack_lower)

    @property
    def t_mrss_lower(self):
        return (
            C_f(self.t_rss_lower, self.t_wc_lower, len(self.items)) * self.t_rss_lower
        )

    @property
    def t_mrss_upper(self):
        return (
            C_f(self.t_rss_upper, self.t_wc_upper, len(self.items)) * self.t_rss_upper
        )

    def df(self):
        # members = [attr for attr in dir(obj()) if not callable(getattr(obj(),attr)) and not attr.startswith("__")]
        return pd.DataFrame(
            [
                {
                    "id": item.id,
                    "dir": item.direction,
                    "nominal": np.abs(round(item.nominal)),
                    "tolerance": (repr(item.tolerance)).ljust(len("tolerance"), " "),
                    "process_sigma": str(item.process_sigma) + "σ",
                    "σ": round(item.sigma),
                    "min_rel": round(item.min_rel),
                    "max_rel": round(item.max_rel),
                    "min_abs": round(item.min_abs),
                    "max_abs": round(item.max_abs),
                    "C_p": round(item.C_p),
                    "k": item.k,
                    "C_pk": round(item.C_pk),
                    "μ_eff": round(item.mu_eff),
                    "σ_eff": round(item.sigma_eff),
                    "name": item.name,
                    "description": (item.description),
                }
                for item in self.items
            ]
        )

    def df_text(self):
        return self.df().to_string(index=False)

    def results_text_RSS_simple(self):
        # Dimensioning and Tolerancing Handbook, McGraw Hill
        # http://files.engineering.com/getfile.aspx?folder=69759f43-e81a-4801-9090-a0c95402bfc0&file=RSS_explanation.GIF
        """This is a simple RSS calculation. This is uses the RSS calculation method in the Dimensioning and Tolerancing Handbook, McGraw Hill.
        It is really only useful for a Bilateral stack of same process-sigma items. The RSS result has the same uncertainty as the measurements.
        """
        s = "--[RSS simple]---------------------------------------\n"
        s += f"{round(self.d_g)} +{round(self.t_wc_upper)}/-{round(self.t_wc_lower)} [{round(self.d_g-self.t_wc_lower)} {round(self.d_g+self.t_wc_upper)}] Worst Case \n"
        s += f"{round(self.d_g)} +{round(self.t_mrss_upper)}/-{round(self.t_mrss_lower)} [{round(self.d_g-self.t_mrss_lower)} {round(self.d_g+self.t_mrss_upper)}] Modified RSS \n"
        s += f"{round(self.d_g)} +{round(self.t_rss_upper)}/-{round(self.t_rss_lower)} [{round(self.d_g-self.t_rss_lower)} {round(self.d_g+self.t_rss_upper)}] RSS "
        return s

    def results_text_RSS(self):
        # https://www.mitcalc.com/doc/tolanalysis1d/help/en/tolanalysis1d.htm
        # mu = sum([item.nominal for item in self.items])
        # sigma = RSS(*[sigma_i(item.T, item.process_sigma * 2) for item in self.items])
        mu = sum([item.mu_eff * item.j for item in self.items])
        sigma = RSS(*[item.sigma_eff * item.j for item in self.items])
        s = "--[RSS]---------------------------------------\n"
        s += f"μ = {round(mu)}\n"
        s += f"σ = {round(sigma)}\n"
        s += f"{round(mu)} ± {round(sigma*6)} [{round(mu-sigma*6)} {round(mu+sigma*6)}] 6σ \n"
        # s += f"{round(mu)} ± {round(sigma*5)} [{round(mu-sigma*5)} {round(mu+sigma*5)}] 5sigma"
        s += f"{round(mu)} ± {round(sigma*4.5)} [{round(mu-sigma*4.5)} {round(mu+sigma*4.5)}] 4.5σ \n"
        s += f"{round(mu)} ± {round(sigma*4)} [{round(mu-sigma*4)} {round(mu+sigma*4)}] 4σ \n"
        s += f"{round(mu)} ± {round(sigma*3)} [{round(mu-sigma*3)} {round(mu+sigma*3)}] 3σ \n"
        s += f"{round(mu)} ± {round(sigma*2)} [{round(mu-sigma)} {round(mu+sigma*2)}] 2σ \n"
        return s

    # def results_text_six_sigma(self):
    #     # https://www.mitcalc.com/doc/tolanalysis1d/help/en/tolanalysis1d.htm
    #     s = "----------------------------------------\n"
    #     # s += f"{}\n"
