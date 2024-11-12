import itertools
import logging
import textwrap
from typing import Any, Dict, List, Union

from . import dist
from .display import display_df
from .stats import C_p, C_pk
from .tolerance import SymmetricBilateral, UnequalBilateral
from .utils import POSITIVE, nround, sign, sign_symbol


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
        return display_df(self.dict, f"DIMENSION: {self.name} - {self.description}", dispmode="plot")._repr_html_()

    def show(self):
        return display_df(self.dict, f"DIMENSION: {self.name} - {self.description}")

    @property
    def dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "ID": self.id,
                "Name": self.name,
                "Desc.": (self.description),
                "±": self.nom_direction_sign,
                "Nom.": nround(self.nominal),
                "Tol.": (str(self.tolerance)).ljust(14, " "),
                "Sens. (a)": str(self.a),
                "Rel. Bounds": f"[{nround(self.rel_lower)}, {nround(self.rel_upper)}]",
            }
        ]

    @property
    def nom_direction_sign(self):
        return sign_symbol(self.dir)

    @property
    def median(self):
        return (self.rel_lower + self.rel_upper) / 2

    @property
    def abs_lower(self):
        """The minimum value of the measurement. AKA, absolute upper"""
        return min(self.dir * self.nominal + self.tolerance.lower, self.dir * self.nominal + self.tolerance.upper)

    @property
    def abs_upper(self):
        """The maximum value of the measurement. AKA, absolute lower"""
        return max(self.dir * self.nominal + self.tolerance.lower, self.dir * self.nominal + self.tolerance.upper)

    @property
    def abs_lower_tol(self):
        """The absolute minimum value of the tolerance."""
        if sign_symbol(self.dir) == POSITIVE:
            return self.tolerance.lower
        else:
            return -self.tolerance.upper

    @property
    def abs_upper_tol(self):
        """The absolute maximum value of the tolerance."""
        if sign_symbol(self.dir) == POSITIVE:
            return self.tolerance.upper
        else:
            return -self.tolerance.lower

    # @property
    # def Z_min(self):
    #     """The minimum value of the measurement. AKA, absolute upper"""
    #     return self.abs_lower

    # @property
    # def Z_max(self):
    #     """The maximum value of the measurement. AKA, absolute lower"""
    #     return self.abs_upper

    @property
    def rel_lower(self):
        return self.nominal + self.tolerance.lower

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

        logging.warning(f"Converting Statistical Dim. ({stat}) to Basic Dim.")
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
        target_process_sigma (float, optional): The standard deviation of the process represented as ±σ. Defaults to ±3σ.
        k (float, optional): The ratio of the amount the center of the distribution is shifted from the mean represented as a multiple of the process
                            standard deviation. Defaults to 0σ.
        distribution (str, optional): The distribution of the measurement. Defaults to "Normal".
    """

    def __init__(
        self,
        target_process_sigma: float = 3,
        distribution: Union[dist.Uniform, dist.Normal, dist.NormalScreened, None] = None,
        *args,
        **kwargs,
    ):
        # super().__init__(*args, **kwargs)
        super(Statistical, self).__init__(*args, **kwargs)
        self.distribution = distribution
        self.target_process_sigma = target_process_sigma

    def __repr__(self) -> str:
        return f"Statistical({self.nominal}, {repr(self.tolerance)}, {self.a}, {self.name}, {self.description}, {self.target_process_sigma}, {self.k}, {self.distribution})"  # noqa: E501

    def __str__(self) -> str:
        return f"{self.id}: {self.name} {self.description} {self.nom_direction_sign}{nround(self.nominal)} {str(self.tolerance)} @ ± {self.target_process_sigma}σ & k={self.k}"

    def _repr_html_(self) -> str:
        return display_df(self.dict, f"DIMENSION: {self.name} - {self.description}", dispmode="plot")._repr_html_()

    def show(self, expand=False):
        unused_keys = ["Name"]
        simple_keys = ["ID", "Desc.", "±", "Nom.", "Tol.", "Sens. (a)", "Abs. Bounds"]
        dict_copy = self.dict
        for entry in dict_copy:
            for key in unused_keys:
                entry.pop(key, None)
        if expand:
            return display_df(dict_copy, f"DIMENSION: {self.name} - {self.description}")
        else:
            new_dict = []
            for d in dict_copy:
                new_dict.append({k: d[k] for k in simple_keys})
            return display_df(new_dict, f"DIMENSION: {self.name} - {self.description}")
        # return display_df(self.dict, f"DIMENSION: {self.name} - {self.description}")

    @property
    def dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "ID": self.id,
                "Name": self.name,
                "Desc.": (self.description),
                "±": self.nom_direction_sign,
                "Nom.": nround(self.nominal),
                "Tol.": (str(self.tolerance)).ljust(14, " "),
                "Sens. (a)": nround(self.a),
                # "Rel. Bounds": f"[{nround(self.rel_lower)}, {nround(self.rel_upper)}]",
                "Abs. Bounds": f"[{nround(self.abs_lower)}, {nround(self.abs_upper)}]",
                "Target Sigma": f"± {str(nround(self.target_process_sigma))}σ",
                "Dist.": f"{self.distribution}",
                "Skew (k)": nround(self.k),
                "C_p": nround(self.C_p) if isinstance(self.distribution, dist.Normal) else "",
                "C_pk": nround(self.C_pk) if isinstance(self.distribution, dist.Normal) else "",
                "μ_eff": nround(self.mean_eff),
                "σ_eff": nround(self.stdev_eff),
                "Eff. Sigma": f"± {str(nround(self.process_sigma_eff))}σ",
                "Yield Prob.": f"{nround(self.yield_probability*100, 8)}" if self.yield_probability is not None else "",
                "Reject PPM": f"{nround(self.yield_loss_probability*1000000, 2)}" if self.yield_loss_probability is not None else "",
            }
        ]

    @classmethod
    def from_basic_dimension(
        cls,
        basic: Union[Basic, "Statistical"],
        target_process_sigma: float = 3,
        distribution: Union[dist.Uniform, dist.Normal, dist.NormalScreened, None] = None,
    ):
        if type(basic) is Statistical:
            return basic

        logging.warning(f"Converting Basic Dim. ({basic}) to Statistical Dim.")
        return cls(
            nom=basic.dir * basic.nominal,
            tol=basic.tolerance,
            a=basic.a,
            name=basic.name,
            desc=basic.description,
            target_process_sigma=target_process_sigma,
            distribution=distribution,
        )

    # Assume a normal distribution.
    def assume_normal_dist(self):
        if isinstance(self.distribution, dist.Normal):
            return self
        logging.warning(f"Assuming Normal Dist. for {self}")
        mean = self.mean_eff
        stdev = (self.rel_upper - self.rel_lower) / (2 * self.target_process_sigma)
        distribution = dist.Normal(mean=mean, stdev=stdev)
        self.distribution = distribution
        return self

    # Assume a normal distribution with a skew
    def assume_normal_dist_skewed(self, skew):
        self.assume_normal_dist()
        if isinstance(self.distribution, dist.Normal):  # which it will be
            self.distribution.mean = self.distribution.mean + skew * (self.distribution.stdev * self.target_process_sigma)
        return self

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
    def process_sigma_eff(self):
        """
        calculated sigma (# of eff_stdevs away fromm USL and LSL)
        """
        if self.stdev_eff == 0:
            return 0
        # print(self.tolerance.upper, self.stdev_eff)
        # since we are using effective stdev, either USL or LSL should work.
        min_tol_gap = min((self.rel_upper - self.mean_eff), (self.mean_eff - self.rel_lower))
        return (min_tol_gap) / self.stdev_eff
        # return 0

    @property
    def k(self):
        if isinstance(self.distribution, dist.Normal):
            ideal_process_stdev = (self.tolerance.T / 2) / self.target_process_sigma
            skew_in_stdevs = (self.distribution.mean - self.mean_eff) / ideal_process_stdev
            return skew_in_stdevs / self.target_process_sigma
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
        UL = self.abs_upper
        LL = self.abs_lower
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
        return display_df(self.dict, f"STACK: {self.name}", dispmode="plot")._repr_html_()

    def show(self, expand=False):
        simple_keys = ["ID", "Name", "Desc.", "±", "Nom.", "Tol.", "Sens. (a)", "Abs. Bounds"]
        dict_copy = self.dict
        if expand:
            return display_df(dict_copy, f"STACK: {self.name}")
        else:
            new_dict = []
            for d in dict_copy:
                new_dict.append({k: d[k] for k in simple_keys})
            return display_df(new_dict, f"STACK: {self.name}")

    def append(self, measurement: Union[Basic, Statistical]):
        self.dims.append(measurement)

    @property
    def dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "ID": dim.id,
                "Name": dim.name,
                "Desc.": (dim.description),
                "±": dim.nom_direction_sign,
                "Nom.": (str(dim.nominal)).rjust(8, " "),
                "Tol.": (str(dim.tolerance)).ljust(14, " "),
                "Sens. (a)": f"{nround(dim.a)}",
                # "Rel. Bounds": f"[{nround(dim.rel_lower)}, {nround(dim.rel_upper)}]",
                "Abs. Bounds": f"[{nround(dim.abs_lower)}, {nround(dim.abs_upper)}]",
                "Target Sigma": f"± {str(nround(dim.target_process_sigma))}σ" if hasattr(dim, "target_process_sigma") else "",
                "Dist.": f"{dim.distribution}" if hasattr(dim, "distribution") else "",
                "Skew (k)": nround(dim.k) if hasattr(dim, "k") else "",
                "C_p": nround(dim.C_p) if (hasattr(dim, "C_p") and isinstance(dim.distribution, dist.Normal)) else "",
                "C_pk": nround(dim.C_pk) if (hasattr(dim, "C_pk") and isinstance(dim.distribution, dist.Normal)) else "",
                # "μ": nround(dim.mean) if hasattr(dim, "mean") else "",
                # "σ": nround(dim.stdev) if hasattr(dim, "stdev") else "",
                "μ_eff": nround(dim.mean_eff) if hasattr(dim, "mean_eff") else "",
                "σ_eff": nround(dim.stdev_eff) if hasattr(dim, "stdev_eff") else "",
                "Eff. Sigma": f"± {str(nround(dim.process_sigma_eff))}σ" if hasattr(dim, "process_sigma_eff") else "",
                "Yield Prob.": f"{nround(dim.yield_probability*100, 8)}" if hasattr(dim, "yield_probability") else "",
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
        return f"SPEC: {self.name}"

    def _repr_html_(self) -> str:
        return display_df(self.dict, f"SPEC: {self.name}", dispmode="plot")._repr_html_()

    def show(self):
        unused_keys = ["Name"]
        # simple_keys = ["ID", "Desc.", "±", "Nom.", "Tol.", "Sens. (a)", "Rel. Bounds"]
        dict_copy = self.dict
        for entry in dict_copy:
            for key in unused_keys:
                entry.pop(key, None)
        return display_df(dict_copy, f"SPEC: {self.name}")

    @property
    def median(self):
        """median"""
        return (self.LL + self.UL) / 2

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
                "Name": textwrap.shorten(self.name, width=10, placeholder="..."),
                "Desc.": textwrap.shorten(self.description, width=10, placeholder="..."),
                "Dimension": self.dim.__str__(),
                "Median": nround(self.median),
                "Spec. Limits": f"[{nround(self.LL)}, {nround(self.UL)}]",
                "Yield Prob.": f"{nround(self.yield_probability*100, 8)}" if self.yield_probability is not None else "",
                "Reject PPM": f"{nround(self.R, 2)}",
            }
        ]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
