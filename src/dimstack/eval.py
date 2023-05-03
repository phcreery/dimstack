import itertools
import logging

from typing import List, Union, Dict, Any

from .display import display_df
from .stats import C_p, C_pk, RSS_func, normal_cdf
from .tolerance import SymmetricBilateral, UnequalBilateral, Bilateral
from .utils import nround, sign
from . import dist

POSITIVE = "+"
NEGATIVE = "-"


class BasicDimension:
    """
    A measurement is a single measurement of a part.

    Args:
        nom (float, optional): The nominal value of the measurement. Defaults to 0.
        tol (Union[SymmetricBilateral, UnequalBilateral], optional): The tolerance of the measurement. Defaults to SymmetricBilateral(0).
        a (float, optional): The sensitivity of the measurement. Defaults to 1. If the nominal value is negative, the sensitivity will be multiplied by a -1
                            and the nominal value will be made positive.
        name (str, optional): The name of the measurement. Defaults to "Dimension".
        desc (str, optional): The description of the measurement. Defaults to "Dimension".
    """

    newID = itertools.count().__next__

    def __init__(
        self,
        nom: float,
        tol: Union[SymmetricBilateral, UnequalBilateral],
        a: float = 1,
        name: str = "Dimension",
        desc: str = "Dimension",
    ):
        self.id = BasicDimension.newID()
        self.dir = sign(nom) * sign(a)
        self.nominal = abs(nom)
        self.tolerance = tol
        self.a = abs(a)
        self.name = name
        self.description = desc
        self.distribution = dist.DIST_UNIFORM

    def __repr__(self) -> str:
        return f"BasicDimension({self.nominal}, {repr(self.tolerance)}, {self.a}, {self.name}, {self.description})"

    def __str__(self) -> str:
        return f"{self.id}: {self.name} {self.description} {self.direction}{nround(self.nominal)} {str(self.tolerance)}"

    def _repr_html_(self) -> str:
        return display_df(self.dict, f"Dimension: {self.name} - {self.description}", dispmode="plot")._repr_html_()

    def show(self):
        return display_df(self.dict, f"Dimension: {self.name} - {self.description}")

    @property
    def dict(self) -> Dict[str, Any]:
        return [
            {
                "ID": self.id,
                "Name": self.name,
                "Description": (self.description),
                "dir": self.direction,
                "Nom.": nround(self.nominal),
                "Tol.": (str(self.tolerance)).ljust(14, " "),
                "Sen.": str(self.a),
                "Relative Bounds": f"[{nround(self.lower_rel)}, {nround(self.upper_rel)}]",
                "Distribution": self.distribution,
            }
        ]

    @property
    def direction(self):
        if self.dir >= 0:
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
    def median(self):
        return (self.lower_rel + self.upper_rel) / 2

    @property
    def Z_min(self):
        """The minimum value of the measurement. AKA, absolute upper"""
        return self.dir * (self.nominal - self.tolerance.lower)

    @property
    def Z_max(self):
        """The maximum value of the measurement. AKA, absolute lower"""
        return self.dir * (self.nominal + self.tolerance.upper)

    @property
    def lower_rel(self):
        return self.nominal - self.tolerance.lower

    @property
    def upper_rel(self):
        return self.nominal + self.tolerance.upper

    def convert_to_bilateral(self):
        median = self.median
        tol = self.tolerance.T / 2

        self.nominal = median
        self.tolerance = SymmetricBilateral(tol)
        return self

    @classmethod
    def from_statistical_dimension(
        cls,
        stat: "StatisticalDimension",
    ):
        if type(stat) is BasicDimension:
            return stat

        logging.warning(f"Converting StatisticalDimension ({stat}) to BasicDimension")
        return cls(
            nom=stat.nominal * stat.dir,
            tol=stat.tolerance,
            a=stat.a,
            name=stat.name,
            desc=stat.description,
        )

    def get_dist(self):
        return dist.Uniform(self.lower_rel, self.upper_rel)

    def get_alt_dists(self):
        return []


class StatisticalDimension(BasicDimension):
    """StatisticalDimension

    Args:
        process_sigma (float, optional): The standard deviation of the process represented as ±σ. Defaults to ±3σ.
        k (float, optional): The ratio of the amount the center of the distribution is shifted from the mean represented as a multiple of the process
                            standard deviation. Defaults to 0σ.
        distribution (str, optional): The distribution of the measurement. Defaults to "Normal".
    """

    def __init__(
        self,
        process_sigma: float = 3,
        k: float = 0,
        distribution: str = dist.DIST_NORMAL,
        data=None,
        *args,
        **kwargs,
    ):
        # super().__init__(*args, **kwargs)
        super(StatisticalDimension, self).__init__(*args, **kwargs)
        self.distribution = distribution
        self.process_sigma = process_sigma
        self.k = k
        self.data = data

    def __repr__(self) -> str:
        return f"StatisticalDimension({self.nominal}, {repr(self.tolerance)}, {self.a}, {self.name}, {self.description}, {self.process_sigma}, {self.k}, {self.distribution})"  # noqa: E501

    def __str__(self) -> str:
        return f"{self.id}: {self.name} {self.description} {self.direction}{nround(self.nominal)} {str(self.tolerance)} @ ± {self.process_sigma}σ & k={self.k}"

    def _repr_html_(self) -> str:
        return display_df(self.dict, f"Dimension: {self.name} - {self.description}", dispmode="plot")._repr_html_()

    def show(self):
        return display_df(self.dict, f"Dimension: {self.name} - {self.description}")

    @classmethod
    def from_basic_dimension(
        cls,
        basic: Union[BasicDimension, "StatisticalDimension"],
        process_sigma: float = 3,
        k: float = 0,
        distribution: str = "Normal",
    ):
        if type(basic) is StatisticalDimension:
            return basic

        logging.warning(f"Converting BasicDimension ({basic}) to StatisticalDimension")
        return cls(
            nom=basic.nominal * basic.dir,
            tol=basic.tolerance,
            a=basic.a,
            name=basic.name,
            desc=basic.description,
            process_sigma=process_sigma,
            k=k,
            distribution=distribution,
        )

    @classmethod
    def from_data(cls, data, sigma=3, name="data", desc="data"):
        """Create a StatisticalDimension from data

        Args:
            data (np.ndarray): The data to create the dimension from
        """
        distribution = dist.Normal.fit(data)
        print(distribution, distribution.mean, distribution.stdev)
        return cls(
            nom=distribution.mean,
            tol=SymmetricBilateral(distribution.stdev * sigma),
            a=1,
            name=name,
            desc=f"{desc} (from data)",
            process_sigma=sigma,
            k=0,
            distribution=dist.DIST_NORMAL,
            data=data,
        )

    @property
    def dict(self) -> Dict[str, Any]:
        return [
            {
                "ID": self.id,
                "Name": self.name,
                "Description": (self.description),
                "dir": self.direction,
                "Nom.": nround(self.nominal),
                "Tol.": (str(self.tolerance)).ljust(14, " "),
                "Sen.": nround(self.a),
                "Relative Bounds": f"[{nround(self.lower_rel)}, {nround(self.upper_rel)}]",
                "Distribution": f"{self.distribution}",
                "Process Sigma": f"± {str(nround(self.process_sigma))}σ",
                "k": nround(self.k),
                "C_p": nround(self.C_p),
                "C_pk": nround(self.C_pk),
                "μ": nround(self.mean),
                "σ": nround(self.stdev),
                "μ_eff": nround(self.mean_eff),
                "σ_eff": nround(self.stdev_eff),
                "Yield Probability": f"{nround(self.yield_probability*100, 8)}",
                "Reject PPM": f"{nround(self.yield_loss_probability*1000000, 2)}",
            }
        ]

    @property
    def mean(self):
        mean_shift = self.k * self.process_sigma * self.stdev
        return self.median + mean_shift

    @property
    def stdev(self):
        return abs(self.tolerance.T / 2) / self.process_sigma

    # @property
    # def variance(self):
    #     return self.stdev ** 2

    @property
    def C_p(self):
        return C_p(self.upper_rel, self.lower_rel, self.stdev)

    @property
    def C_pk(self):
        return C_pk(self.upper_rel, self.lower_rel, self.stdev, self.mean)

    @property
    def mean_eff(self):
        """effective mean"""
        return (self.lower_rel + self.upper_rel) / 2

    @property
    def stdev_eff(self):
        """
        effective standard deviation
        "6 stdev" is the standard deviation of the distribution
        """
        return abs(self.tolerance.T) / (6 * self.C_pk)

    @property
    def yield_loss_probability(self):
        UL = self.upper_rel
        LL = self.lower_rel
        # return 1 - normal_cdf(UL, self.mean_eff, self.stdev_eff) + normal_cdf(LL, self.mean_eff, self.stdev_eff)
        return 1 - self.get_dist().cdf(UL) + self.get_dist().cdf(LL)

    @property
    def yield_probability(self):
        return 1 - self.yield_loss_probability

    def get_dist(self):
        if self.distribution == dist.DIST_NORMAL:
            return dist.Normal(self.mean_eff, self.stdev_eff)
            # return dist.Normal(self.mean, self.stdev)
        elif self.distribution == dist.DIST_UNIFORM:
            return dist.Uniform(self.lower_rel, self.upper_rel)

    def get_alt_dists(self):
        if self.distribution == dist.DIST_NORMAL:
            if self.k == 0:
                return []
            mean_shift = self.k * self.process_sigma * self.stdev
            return [
                dist.Normal(self.mean_eff + mean_shift, self.stdev),
                dist.Normal(self.mean_eff - mean_shift, self.stdev),
            ]
        else:
            return []


class Stack:
    def __init__(
        self,
        title: str = "Stack",
        items: List[Union[BasicDimension, StatisticalDimension]] = [],
    ):
        self.title = title
        self.items = items

    def __repr__(self) -> str:
        return f"Stack({self.title}, [{', '.join([repr(item) for item in self.items])}])"

    def __str__(self) -> str:
        return f"{self.title}: {self.items}"

    def _repr_html_(self) -> str:
        return display_df(self.dict, f"Stack: {self.title}", dispmode="plot")._repr_html_()

    def show(self):
        return display_df(self.dict, f"Stack: {self.title}")

    def append(self, measurement: Union[BasicDimension, StatisticalDimension]):
        self.items.append(measurement)

    @property
    def Closed(self) -> BasicDimension:
        nominal = sum([item.nominal * item.a * item.dir for item in self.items])
        tolerance = Bilateral(
            sum(filter(None, [item.tolerance_absolute.upper for item in self.items])),
            sum(filter(None, [item.tolerance_absolute.lower for item in self.items])),
        )
        return BasicDimension(
            nominal,
            tolerance,
            name=f"{self.title} - Closed Analysis",
            desc="",
        )

    @property
    def WC(self) -> BasicDimension:
        """
        This is a simple WC calculation. This results in a Bilateral dimension with a tolerance that is the sum of the component tolerances.
        It states that in any combination of tolerances, you can be sure the result will be within the this resulting tolerance.
        """
        mean = sum([item.median * item.a * item.dir for item in self.items])
        t_wc = sum([abs(item.a * (item.tolerance.T / 2) * item.dir) for item in self.items])
        tolerance = Bilateral(t_wc)
        return BasicDimension(
            nom=mean,
            tol=tolerance,
            name=f"{self.title} - WC Analysis",
            desc="",
        )

    @property
    def RSS(self) -> StatisticalDimension:
        """
        This is a simple RSS calculation. This is uses the RSS calculation method in the Dimensioning and Tolerancing Handbook, McGraw Hill.
        It is really only useful for a Bilateral stack of same process-stdev items. The RSS result has the same uncertainty as the measurements.
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
        items: List[StatisticalDimension] = [StatisticalDimension.from_basic_dimension(item) for item in self.items]
        d_g = sum([item.mean_eff * item.a * item.dir for item in items])
        t_rss = RSS_func(*[item.a * (item.tolerance.T / 2) * item.dir for item in items])
        tolerance = Bilateral(t_rss)
        return StatisticalDimension(
            nom=d_g,
            tol=tolerance,
            name=f"{self.title} - RSS Analysis",
            desc="(assuming inputs with Normal Distribution & ± 3σ)",
        )

    @property
    def MRSS(self) -> StatisticalDimension:
        items: List[StatisticalDimension] = [StatisticalDimension.from_basic_dimension(item) for item in self.items]
        d_g = sum([item.mean_eff * item.a * item.dir for item in items])
        t_wc = sum([abs(item.a * (item.tolerance.T / 2) * item.dir) for item in self.items])
        t_rss = RSS_func(*[item.a * (item.tolerance.T / 2) * item.dir for item in items])
        n = len(self.items)
        C_f = (0.5 * (t_wc - t_rss)) / (t_rss * (n**0.5 - 1)) + 1
        t_mrss = C_f * t_rss
        tolerance = Bilateral(t_mrss)
        stdev = t_wc / 6
        sigma = t_mrss / stdev
        return StatisticalDimension(
            nom=d_g,
            tol=tolerance,
            name=f"{self.title} - MRSS Analysis",
            desc="(assuming inputs with Normal Distribution & ± 3σ)",
            process_sigma=sigma,
        )

    def SixSigma(self, at: float = 3) -> StatisticalDimension:
        items: List[StatisticalDimension] = [StatisticalDimension.from_basic_dimension(item) for item in self.items]
        mean = sum([item.mean_eff * item.dir for item in items])
        stdev = RSS_func(*[item.stdev_eff for item in items])
        tolerance = Bilateral(stdev * at)
        return StatisticalDimension(
            nom=mean,
            tol=tolerance,
            process_sigma=at,
            name=f"{self.title} - '6 Sigma' Analysis",
            desc="(assuming inputs with Normal Distribution)",
        )

    @property
    def dict(self) -> Dict[str, Any]:
        return [
            {
                "ID": item.id,
                "Name": item.name,
                "Description": (item.description),
                "dir": item.direction,
                "Nom.": nround(item.nominal),
                "Tol.": (str(item.tolerance)).ljust(14, " "),
                "Sen.": f"{nround(item.a)}",
                "Relative Bounds": f"[{nround(item.lower_rel)}, {nround(item.upper_rel)}]",
                "Distribution": f"{item.distribution}" if hasattr(item, "distribution") else "",
                "Process Sigma": f"± {str(nround(item.process_sigma))}σ" if hasattr(item, "process_sigma") else "",
                "k": nround(item.k) if hasattr(item, "k") else "",
                "C_p": nround(item.C_p) if hasattr(item, "C_p") else "",
                "C_pk": nround(item.C_pk) if hasattr(item, "C_pk") else "",
                "μ": nround(item.mean) if hasattr(item, "mean") else "",
                "σ": nround(item.stdev) if hasattr(item, "stdev") else "",
                "μ_eff": nround(item.mean_eff) if hasattr(item, "mean_eff") else "",
                "σ_eff": nround(item.stdev_eff) if hasattr(item, "stdev_eff") else "",
                "Yield Probability": f"{nround(item.yield_probability*100, 8)}" if hasattr(item, "yield_probability") else "",
                "Reject PPM": f"{nround(item.yield_loss_probability*1000000, 2)}" if hasattr(item, "yield_loss_probability") else "",
            }
            for item in self.items
        ]


class Spec:
    def __init__(self, name, description, dim: StatisticalDimension, LL, UL):
        self.name = name
        self.description = description
        self.dim = dim
        self.LL = LL
        self.UL = UL

    def __repr__(self) -> str:
        return f"Spec({self.name}, {self.description}, {repr(self.dim)}, {self.LL}, {self.UL})"

    def __str__(self) -> str:
        return f"Spec: {self.name}"

    def _repr_html_(self) -> str:
        return display_df(self.dict, f"Spec: {self.name}", dispmode="plot")._repr_html_()

    def show(self):
        return display_df(self.dict, f"Spec: {self.name}")

    @property
    def median(self):
        """median"""
        return (self.LL + self.UL) / 2

    # @property
    # def mean(self):
    #     mean_shift = self.k * self.process_sigma * self.stdev
    #     return self.median + mean_shift

    @property
    def k(self):
        """k"""
        return abs((self.dim.mean - self.median) / ((self.UL - self.LL) / 2))

    @property
    def C_p(self):
        return C_p(self.UL, self.LL, self.dim.stdev)

    @property
    def C_pk(self):
        # return C_pk(self.C_p, self.k)
        return min(
            (self.UL - self.dim.mean) / (3 * self.dim.stdev),
            (self.dim.mean - self.LL) / (3 * self.dim.stdev),
        )

    @property
    def yield_loss_probability(self):
        if self.UL > self.dim.Z_max:
            upper = 1
        else:
            upper = normal_cdf(self.UL, self.dim.mean, self.dim.stdev)
        if self.LL < self.dim.Z_min:
            lower = 0
        else:
            lower = normal_cdf(self.LL, self.dim.mean, self.dim.stdev)
        return 1 - (upper - lower)

    @property
    def yield_probability(self):
        return 1 - self.yield_loss_probability

    @property
    def R(self):
        """Return the yield loss probability in PPM"""
        return self.yield_loss_probability * 1000000

    @property
    def dict(self) -> Dict[str, Any]:
        return [
            {
                "Name": self.name,
                "Description": self.description,
                "Dimension": f"{self.dim}",
                "Spec. Limits": f"[{nround(self.LL)}, {nround(self.UL)}]",
                "Median": nround(self.median),
                "k": nround(self.k),
                "C_p": nround(self.C_p),
                "C_pk": nround(self.C_pk),
                "Yield Probability": f"{nround(self.yield_probability*100, 8)}",
                "Reject PPM": f"{nround(self.R, 2)}",
            }
        ]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
