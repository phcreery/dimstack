import itertools
import logging
from typing import List, Union, Dict, Any

from .display import display_df
from .stats import C_p, C_pk, RSS
from .tolerance import SymmetricBilateral, UnequalBilateral, Bilateral
from .utils import nround, sign
from . import dist

POSITIVE = "+"
NEGATIVE = "-"


class Basic:
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
        self.id = Basic.newID()
        self.dir = sign(nom) * sign(a)
        self.nominal = abs(nom)
        self.tolerance = tol
        self.a = abs(a)
        self.name = name
        self.description = desc

    def __repr__(self) -> str:
        return f"Basic({self.nominal}, {repr(self.tolerance)}, {self.a}, {self.name}, {self.description})"

    def __str__(self) -> str:
        return f"{self.id}: {self.name} {self.description} {self.nom_direction_sign}{nround(self.nominal)} {str(self.tolerance)}"

    def _repr_html_(self) -> str:
        return display_df(self.dict, f"Dimension: {self.name} - {self.description}", dispmode="plot")._repr_html_()

    def show(self):
        return display_df(self.dict, f"Dimension: {self.name} - {self.description}")

    @property
    def dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "ID": self.id,
                "Name": self.name,
                "Description": (self.description),
                "dir": self.nom_direction_sign,
                "Nom.": nround(self.nominal),
                "Tol.": (str(self.tolerance)).ljust(14, " "),
                "Sens. (a)": str(self.a),
                "Relative Bounds": f"[{nround(self.rel_lower)}, {nround(self.rel_upper)}]",
            }
        ]

    @property
    def nom_direction_sign(self):
        if self.dir >= 0:
            return POSITIVE
        else:
            return NEGATIVE

    @property
    def tolerance_absolute(self):
        if self.nom_direction_sign == POSITIVE:
            return self.tolerance
        elif self.nom_direction_sign == NEGATIVE:
            return Bilateral(self.tolerance.lower, self.tolerance.upper)

    @property
    def median(self):
        return (self.rel_lower + self.rel_upper) / 2

    @property
    def abs_lower(self):
        """The minimum value of the measurement. AKA, absolute upper"""
        return self.dir * (self.nominal - self.tolerance.lower)

    @property
    def abs_upper(self):
        """The maximum value of the measurement. AKA, absolute lower"""
        return self.dir * (self.nominal + self.tolerance.upper)

    @property
    def Z_min(self):
        """The minimum value of the measurement. AKA, absolute upper"""
        return self.abs_lower

    @property
    def Z_max(self):
        """The maximum value of the measurement. AKA, absolute lower"""
        return self.abs_upper

    @property
    def rel_lower(self):
        return self.nominal - self.tolerance.lower

    @property
    def rel_upper(self):
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
        stat: "Statistical",
    ):
        if type(stat) is Basic:
            return stat

        logging.warning(f"Converting Statistical ({stat}) to Basic")
        return cls(
            nom=stat.nominal * stat.dir,
            tol=stat.tolerance,
            a=stat.a,
            name=stat.name,
            desc=stat.description,
        )


class Statistical(Basic):
    """Statistical

    Args:
        process_sigma (float, optional): The standard deviation of the process represented as ±σ. Defaults to ±3σ.
        k (float, optional): The ratio of the amount the center of the distribution is shifted from the mean represented as a multiple of the process
                            standard deviation. Defaults to 0σ.
        distribution (str, optional): The distribution of the measurement. Defaults to "Normal".
    """

    def __init__(
        self,
        process_sigma: float = 3,
        distribution: Union[dist.Uniform, dist.Normal, dist.NormalScreened, None] = None,
        *args,
        **kwargs,
    ):
        # super().__init__(*args, **kwargs)
        super(Statistical, self).__init__(*args, **kwargs)
        self.distribution = distribution
        self.process_sigma = process_sigma

    def __repr__(self) -> str:
        return f"Statistical({self.nominal}, {repr(self.tolerance)}, {self.a}, {self.name}, {self.description}, {self.process_sigma}, {self.k}, {self.distribution})"  # noqa: E501

    def __str__(self) -> str:
        return f"{self.id}: {self.name} {self.description} {self.nom_direction_sign}{nround(self.nominal)} {str(self.tolerance)} @ ± {self.process_sigma}σ & k={self.k}"

    def _repr_html_(self) -> str:
        return display_df(self.dict, f"Dimension: {self.name} - {self.description}", dispmode="plot")._repr_html_()

    def show(self):
        return display_df(self.dict, f"Dimension: {self.name} - {self.description}")

    @classmethod
    def from_basic_dimension(
        cls,
        basic: Union[Basic, "Statistical"],
        process_sigma: float = 3,
        distribution: Union[dist.Uniform, dist.Normal, dist.NormalScreened, None] = None,
    ):
        if type(basic) is Statistical:
            return basic

        logging.warning(f"Converting Basic ({basic}) to Statistical dimension")
        return cls(
            nom=basic.nominal * basic.dir,
            tol=basic.tolerance,
            a=basic.a,
            name=basic.name,
            desc=basic.description,
            process_sigma=process_sigma,
            distribution=distribution,
        )

    # TODO: move to distribution function
    # @classmethod
    # def from_data(cls, data, sigma=3, name="data", desc="data"):
    #     """Create a Statistical dimension from data

    #     Args:
    #         data (np.ndarray or similar): The data to create the dimension from
    #     """
    #     distribution = dist.Normal.fit(data)

    #     return cls(
    #         nom=distribution.mean,
    #         tol=SymmetricBilateral(distribution.stdev * sigma),
    #         a=1,
    #         name=name,
    #         desc=f"{desc} (from data)",
    #         process_sigma=sigma,
    #         k=0,
    #         distribution=None,
    #         data=data,
    #     )

    # Assume a normal distribution.
    def assume_normal_dist(self):
        mean = self.mean_eff
        stdev = (self.rel_upper - self.rel_lower) / (2 * self.process_sigma)
        distribution = dist.Normal(mean=mean, stdev=stdev)
        self.distribution = distribution
        return self

    # Assume a normal distribution with a skew
    def assume_normal_dist_skewed(self, skew):
        self.assume_normal_dist()
        if isinstance(self.distribution, dist.Normal):  # which it will be
            self.distribution.mean = self.distribution.mean + skew * (self.distribution.stdev * self.process_sigma)
        return self

    @property
    def dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "ID": self.id,
                "Name": self.name,
                "Description": (self.description),
                "dir": self.nom_direction_sign,
                "Nom.": nround(self.nominal),
                "Tol.": (str(self.tolerance)).ljust(14, " "),
                "Sens. (a)": nround(self.a),
                "Relative Bounds": f"[{nround(self.rel_lower)}, {nround(self.rel_upper)}]",
                "Distribution": f"{self.distribution}",
                "Process Sigma": f"± {str(nround(self.process_sigma))}σ",
                "Skew (k)": nround(self.k),
                "C_p": nround(self.C_p) if isinstance(self.distribution, dist.Normal) else "",
                "C_pk": nround(self.C_pk) if isinstance(self.distribution, dist.Normal) else "",
                # "μ": nround(self.mean),
                # "σ": nround(self.stdev),
                "μ_eff": nround(self.mean_eff),
                "σ_eff": nround(self.stdev_eff),
                "Yield Probability": f"{nround(self.yield_probability*100, 8)}" if self.yield_probability is not None else "",
                "Reject PPM": f"{nround(self.yield_loss_probability*1000000, 2)}" if self.yield_loss_probability is not None else "",
            }
        ]

    # @property
    # def mean(self):
    #     mean_shift = self.k * self.process_sigma * self.stdev
    #     return self.median + mean_shift

    # @property
    # def stdev(self):
    #     return abs(self.tolerance.T / 2) / self.process_sigma

    # @property
    # def variance(self):
    #     return self.stdev ** 2

    @property
    def C_p(self):
        if isinstance(self.distribution, dist.Normal):
            return C_p(self.rel_upper, self.rel_lower, self.distribution.stdev)
        return 0

    @property
    def C_pk(self):
        if isinstance(self.distribution, dist.Normal):
            return C_pk(self.rel_upper, self.rel_lower, self.distribution.mean, self.distribution.stdev)
        return 0

    @property
    def mean_eff(self):
        """effective mean"""
        return (self.rel_lower + self.rel_upper) / 2

    @property
    def stdev_eff(self):
        """
        effective standard deviation
        "6 stdev" is the standard deviation of the distribution
        """
        # return abs(self.tolerance.T) / (6 * self.C_pk)
        if isinstance(self.distribution, dist.Normal):
            outer_shift = min((self.rel_upper - self.distribution.mean), (self.distribution.mean - self.rel_lower))
            return (self.tolerance.T * self.distribution.stdev) / (2 * outer_shift)
        return 0

    @property
    def k(self):
        if isinstance(self.distribution, dist.Normal):
            ideal_process_stdev = (self.tolerance.T / 2) / self.process_sigma
            skew_in_stdevs = (self.distribution.mean - self.mean_eff) / ideal_process_stdev
            return skew_in_stdevs / self.process_sigma
        return 0

    @property
    def yield_loss_probability(self):
        """
        Returns the probability of a part being out of spec.
        """
        if self.distribution is None:
            return 0
        return 1 - self.yield_probability

    @property
    def yield_probability(self):
        if self.distribution is None:
            return 0
        UL = self.rel_upper
        LL = self.rel_lower
        # return 1 - normal_cdf(UL, self.mean_eff, self.stdev_eff) + normal_cdf(LL, self.mean_eff, self.stdev_eff)
        return self.distribution.cdf(UL) - self.distribution.cdf(LL)


class Stack:
    def __init__(
        self,
        name: str = "Stack",
        description: str = "",
        dims: List[Union[Basic, Statistical]] = [],
    ):
        self.name = name
        self.description = description
        self.dims = dims

    def __repr__(self) -> str:
        return f"Stack({self.name}, {self.description}, [{', '.join([repr(dim) for dim in self.dims])}])"

    def __str__(self) -> str:
        return f"{self.name}: {self.dims}"

    def _repr_html_(self) -> str:
        return display_df(self.dict, f"Stack: {self.name}", dispmode="plot")._repr_html_()

    def show(self):
        return display_df(self.dict, f"Stack: {self.name}")

    def append(self, measurement: Union[Basic, Statistical]):
        self.dims.append(measurement)

    @property
    def Closed(self) -> Basic:
        nominal = sum([dim.dir * dim.nominal * dim.a for dim in self.dims])
        tolerance = Bilateral(
            sum(filter(None, [dim.tolerance_absolute.upper for dim in self.dims])),
            sum(filter(None, [dim.tolerance_absolute.lower for dim in self.dims])),
        )
        return Basic(
            nominal,
            tolerance,
            name=f"{self.name} - Closed Analysis",
            desc="",
        )

    @property
    def WC(self) -> Basic:
        """
        This is a simple WC calculation. This results in a Bilateral dimension with a tolerance that is the sum of the component tolerances.
        It states that in any combination of tolerances, you can be sure the result will be within the this resulting tolerance.
        """
        mean = sum([dim.dir * dim.median * dim.a for dim in self.dims])
        t_wc = sum([abs((dim.tolerance.T / 2) * dim.a) for dim in self.dims])
        tolerance = Bilateral(t_wc)
        return Basic(
            nom=mean,
            tol=tolerance,
            name=f"{self.name} - WC Analysis",
            desc="",
        )

    @property
    def RSS(self) -> Statistical:
        """
        This is a simple RSS calculation. This is uses the RSS calculation method in the Dimensioning and Tolerancing Handbook, McGraw Hill.
        It is really only useful for a Bilateral stack of same process-stdev dims. The RSS result has the same uncertainty as the measurements.
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

        See:
         - Dimensioning and Tolerancing Handbook, McGraw Hill
         - http://files.engineering.com/getfile.aspx?folder=69759f43-e81a-4801-9090-a0c95402bfc0&file=RSS_explanation.GIF
        """
        dims: List[Statistical] = [Statistical.from_basic_dimension(dim) for dim in self.dims]
        d_g = sum([dim.dir * dim.median * dim.a for dim in dims])
        t_rss = RSS([dim.dir * (dim.tolerance.T / 2) * dim.a for dim in dims])
        tolerance = Bilateral(t_rss)
        return Statistical(
            nom=d_g,
            tol=tolerance,
            name=f"{self.name} - RSS Analysis",
            desc="(assuming inputs with Normal Distribution & ± 3σ)",
        )

    @property
    def MRSS(self) -> Statistical:
        """Basically RSS with a coefficient modifier to make the tolerance tighter.

        Returns:
            Statistical: _description_
        """
        dims: List[Statistical] = [Statistical.from_basic_dimension(dim) for dim in self.dims]
        d_g = sum([dim.dir * dim.median * dim.a for dim in dims])
        t_wc = sum([abs(dim.dir * (dim.tolerance.T / 2) * dim.a) for dim in dims])
        t_rss = RSS([dim.dir * dim.a * (dim.tolerance.T / 2) for dim in dims])
        n = len(self.dims)
        C_f = (0.5 * (t_wc - t_rss)) / (t_rss * (n**0.5 - 1)) + 1
        t_mrss = C_f * t_rss
        tolerance = Bilateral(t_mrss)
        stdev = t_wc / 6
        sigma = t_mrss / stdev
        return Statistical(
            nom=d_g,
            tol=tolerance,
            name=f"{self.name} - MRSS Analysis",
            desc="(assuming inputs with Normal Distribution & ± 3σ)",
            process_sigma=sigma,
        )

    def SixSigma(self, at: float = 3) -> Statistical:
        dims: List[Statistical] = [Statistical.from_basic_dimension(dim) for dim in self.dims]
        mean = sum([dim.dir * dim.median for dim in dims])
        stdev = RSS([dim.stdev_eff for dim in dims])
        tolerance = Bilateral(stdev * at)
        dim = Statistical(
            nom=mean,
            tol=tolerance,
            process_sigma=at,
            name=f"{self.name} - '6 Sigma' Analysis",
            desc="(assuming inputs with Normal Distribution)",
        )
        dim.assume_normal_dist()
        return dim

    @property
    def dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "ID": dim.id,
                "Name": dim.name,
                "Description": (dim.description),
                "dir": dim.nom_direction_sign,
                "Nom.": nround(dim.nominal),
                "Tol.": (str(dim.tolerance)).ljust(14, " "),
                "Sens. (a)": f"{nround(dim.a)}",
                "Relative Bounds": f"[{nround(dim.rel_lower)}, {nround(dim.rel_upper)}]",
                "Distribution": f"{dim.distribution}" if hasattr(dim, "distribution") else "",
                "Process Sigma": f"± {str(nround(dim.process_sigma))}σ" if hasattr(dim, "process_sigma") else "",
                "Skew (k)": nround(dim.k) if hasattr(dim, "k") else "",
                "C_p": nround(dim.C_p) if (hasattr(dim, "C_p") and isinstance(dim.distribution, dist.Normal)) else "",
                "C_pk": nround(dim.C_pk) if (hasattr(dim, "C_pk") and isinstance(dim.distribution, dist.Normal)) else "",
                "μ": nround(dim.mean) if hasattr(dim, "mean") else "",
                "σ": nround(dim.stdev) if hasattr(dim, "stdev") else "",
                "μ_eff": nround(dim.mean_eff) if hasattr(dim, "mean_eff") else "",
                "σ_eff": nround(dim.stdev_eff) if hasattr(dim, "stdev_eff") else "",
                "Yield Probability": f"{nround(dim.yield_probability*100, 8)}" if hasattr(dim, "yield_probability") else "",
                "Reject PPM": f"{nround(dim.yield_loss_probability*1000000, 2)}" if hasattr(dim, "yield_loss_probability") else "",
            }
            for dim in self.dims
        ]


class Spec:
    def __init__(self, name, description, dim: Union[Statistical, Basic], LL, UL):
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

    # @property
    # def k(self):
    #     """k"""
    #     return abs((self.dim.mean - self.median) / ((self.UL - self.LL) / 2))

    # @property
    # def C_p(self):
    #     return C_p(self.UL, self.LL, self.dim.stdev)

    # @property
    # def C_pk(self):
    #     # return C_pk(self.C_p, self.k)
    #     return min(
    #         (self.UL - self.dim.mean) / (3 * self.dim.stdev),
    #         (self.dim.mean - self.LL) / (3 * self.dim.stdev),
    #     )

    @property
    def yield_loss_probability(self):
        """
        Returns the probability of a part being out of spec.
        """
        if not isinstance(self.dim, Statistical) or self.dim.distribution is None:
            return 0
        return 1 - self.yield_probability

    @property
    def yield_probability(self):
        if not isinstance(self.dim, Statistical) or self.dim.distribution is None:
            return 0
        return self.dim.distribution.cdf(self.UL) - self.dim.distribution.cdf(self.LL)

    @property
    def R(self):
        """Return the yield loss probability in PPM"""
        return self.yield_loss_probability * 1000000

    @property
    def dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "Name": self.name,
                "Description": self.description,
                "Dimension": f"{self.dim}",
                "Median": nround(self.median),
                "Spec. Limits": f"[{nround(self.LL)}, {nround(self.UL)}]",
                "Yield Probability": f"{nround(self.yield_probability*100, 8)}" if self.yield_probability is not None else "",
                "Reject PPM": f"{nround(self.R, 2)}",
            }
        ]


if __name__ == "__main__":
    import doctest

    doctest.testmod()