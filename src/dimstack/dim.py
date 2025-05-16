import itertools
import logging
import textwrap
from typing import Any

from . import dist
from .display import display_df
from .tolerance import Bilateral
from .utils import POSITIVE, nround, sign, sign_symbol
from .stats import C_p, C_pk


class Basic:
    """
    A measurement is a single measurement of a part.

    Args:
        nom (float, optional): The nominal value of the measurement. Defaults to 0.
        tol (Bilateral, optional): The tolerance of the measurement. Defaults to Bilateral.symmetric(0).
        a (float, optional): The sensitivity of the measurement. Defaults to 1.
        name (str, optional): The name of the measurement. Defaults to "Dimension".
        desc (str, optional): The description of the measurement. Defaults to "Dimension".
    """

    newID = itertools.count().__next__

    def __init__(
        self,
        nom: float,
        tol: Bilateral,
        a: float = 1,
        name: str = "Dimension",
        desc: str = "Dimension",
    ):
        self.id = Basic.newID()
        self.dir = sign(nom)
        self.nominal = abs(nom)
        self.tolerance = tol
        self.a = a
        self.name = name
        self.description = desc

    def __str__(self) -> str:
        # return f"{self.id}: {self.name} {self.description} {self.nom_direction_sign}{nround(self.nominal)} {str(self.tolerance)}"
        desc_width = 30
        return (
            textwrap.shorten(
                f"{self.id}: {self.name} {self.description} ",
                width=desc_width,
                placeholder="...",
            ).ljust(desc_width)
            + f" {self.nom_direction_sign}{str(nround(self.nominal)).rjust(6)} {str(self.tolerance)}"
        )

    def _repr_html_(self):
        return display_df([self.dict], f"DIMENSION: {self.name}", dispmode="html")

    def _display_(self):
        return display_df([self.dict], f"DIMENSION: {self.name}")

    def show(self):
        return display_df([self.dict], f"DIMENSION: {self.name}")

    @property
    def dict(self) -> dict[str, Any]:
        return {
            "ID": self.id,
            "Name": self.name,
            "Desc.": (self.description),
            "±": self.nom_direction_sign,
            "Nom.": nround(self.nominal),
            "Tol.": (str(self.tolerance)).ljust(14, " "),
            "Sens. (a)": str(self.a),
            # "Rel. Bounds": f"[{nround(self.rel_lower)}, {nround(self.rel_upper)}]",
            "Abs. Bounds": f"[{nround(self.abs_lower)}, {nround(self.abs_upper)}]",
        }

    @property
    def nom_direction_sign(self) -> str:
        return sign_symbol(self.dir)

    @property
    def rel_nominal(self) -> float:
        """The nominal value of the measurement. AKA, relative nominal"""
        return self.nominal

    @property
    def rel_median(self) -> float:
        """The median value of the measurement. AKA, relative median"""
        return (self.rel_lower + self.rel_upper) / 2

    @property
    def rel_lower(self) -> float:
        """Relative lower value of the dimension"""
        return self.nominal + self.tolerance.lower

    @property
    def rel_upper(self) -> float:
        """Relative upper value of the dimension"""
        return self.nominal + self.tolerance.upper

    @property
    def abs_nominal(self) -> float:
        """The absolute nominal value of the measurement."""
        return self.dir * self.nominal

    @property
    def abs_median(self) -> float:
        """The absolute median value of the measurement."""
        return (self.abs_lower + self.abs_upper) / 2

    @property
    def abs_lower(self) -> float:
        """The minimum value of the measurement. AKA, absolute upper"""
        return self.dir * self.nominal + self.abs_lower_tol

    @property
    def abs_upper(self) -> float:
        """The maximum value of the measurement. AKA, absolute lower"""
        return self.dir * self.nominal + self.abs_upper_tol

    @property
    def abs_lower_tol(self) -> float:
        """The absolute minimum value of the tolerance."""
        if sign_symbol(self.dir) == POSITIVE:
            return self.tolerance.lower
        else:
            return -self.tolerance.upper

    @property
    def abs_upper_tol(self) -> float:
        """The absolute maximum value of the tolerance."""
        if sign_symbol(self.dir) == POSITIVE:
            return self.tolerance.upper
        else:
            return -self.tolerance.lower

    def convert_to_bilateral(self) -> "Basic":
        """Convert the dimension to a bilateral dimension by centering the nominal value."""
        median = self.rel_median
        tol = self.tolerance.T / 2

        self.nominal = median
        self.tolerance = Bilateral.symmetric(tol)
        return self

    def review(
        self,
        distribution: dist.Uniform | dist.Normal | dist.NormalScreened | None = None,
    ) -> "Reviewed":
        """Convert the dimension to a reviewed dimension."""
        return Reviewed(self, distribution)


class Stack:
    def __init__(
        self,
        name: str = "Stack",
        description: str = "",
        dims: list[Basic] = [],
    ):
        self.name = name
        self.description = description
        self.dims = dims

    def __str__(self) -> str:
        return f"{self.name}: {self.dims}"

    def _repr_html_(self):
        return display_df(self.dict, f"DIMENSION STACK: {self.name}", dispmode="html")

    def _display_(self):
        return display_df(self.dict, f"DIMENSION STACK: {self.name}")

    def show(self, expand=False):
        return display_df(self.dict, f"DIMENSION STACK: {self.name}")

    def append(self, measurement: Basic):
        """Append a measurement to the stack."""
        self.dims.append(measurement)

    @property
    def dict(self) -> list[dict[str, Any]]:
        return [dim.dict for dim in self.dims]


class Reviewed:
    """Reviewed

    Args:
        dim (Basic): The basic dimension.
        distribution (str, optional): The distribution of the measurement. Defaults to "Normal".
    """

    dim: Basic
    distribution: dist.Uniform | dist.Normal | dist.NormalScreened

    def __init__(
        self,
        dim: Basic,
        distribution: dist.Uniform | dist.Normal | dist.NormalScreened | None = None,
    ):
        self.dim = dim
        if distribution is None:
            self.assume_normal_dist(6)
        else:
            self.distribution = distribution

    def __str__(self) -> str:
        return f"{self.dim} @ {self.distribution}"

    def _repr_html_(self):
        return display_df([self.dict], f"REVIEWED DIMENSION: {self.dim.name}", dispmode="html")

    def _display_(self):
        return display_df([self.dict], f"REVIEWED DIMENSION: {self.dim.name}")

    def show(self):
        return display_df([self.dict], f"REVIEWED DIMENSION: {self.dim.name}")

    @property
    def dict(self) -> dict[str, Any]:
        return {
            # **self.dim.dict,
            "Dim.": f"{self.dim}",
            "Dist.": f"{self.distribution}",
            # "Z": nround(self.Z) if isinstance(self.distribution, dist.Normal) else "",
            "Shift (k)": nround(self.k),
            "C_p": nround(self.C_p) if isinstance(self.distribution, dist.Normal) else "",
            "C_pk": nround(self.C_pk) if isinstance(self.distribution, dist.Normal) else "",
            "μ_eff": nround(self.mean_eff),
            "σ_eff": nround(self.std_dev_eff),
            "Eff. Sigma": f"± {str(nround(self.process_sigma_eff))}σ",
            "Yield Prob.": f"{nround(self.yield_probability*100, 8)}" if self.yield_probability is not None else "",
            "Reject PPM": f"{nround(self.yield_loss_probability*1000000, 2)}"
            if self.yield_loss_probability is not None
            else "",
        }

    def assume_normal_dist(self, target_process_sigma: float):
        """Assume a normal distribution."""
        mean = self.mean_eff
        std_dev = (self.dim.abs_upper - self.dim.abs_lower) / (2 * target_process_sigma)
        self.distribution = dist.Normal(mean=mean, std_dev=std_dev)
        # logging.warning(f"Assuming Normal Dist. for {self}")
        return self

    def assume_normal_dist_shifted(self, target_process_sigma, shift) -> "Reviewed":
        """Assume a normal distribution with a shift"""
        self.assume_normal_dist(target_process_sigma)
        if isinstance(self.distribution, dist.Normal):
            # self.distribution.mean = self.distribution.mean + shift * self.distribution.std_dev
            self.distribution.mean = self.distribution.mean + shift * self.distribution.std_dev * target_process_sigma
        return self

    @property
    def C_p(self) -> float:
        """Process Capability"""
        if isinstance(self.distribution, dist.Normal):
            return C_p(self.dim.rel_upper, self.dim.rel_lower, self.distribution.std_dev)
        return 0

    @property
    def C_pk(self) -> float:
        """Process Capability Index"""
        if isinstance(self.distribution, dist.Normal):
            return C_pk(self.dim.abs_upper, self.dim.abs_lower, self.distribution.mean, self.distribution.std_dev)
        return 0

    @property
    def Z(self) -> float:
        """Z value"""
        if isinstance(self.distribution, dist.Normal):
            return (self.dim.abs_upper - self.distribution.mean) / self.distribution.std_dev
        return 0

    @property
    def mean_eff(self) -> float:
        """effective mean"""
        return (self.dim.abs_lower + self.dim.abs_upper) / 2

    @property
    def std_dev_eff(self) -> float:
        """
        effective standard deviation
        "6 std_dev" is the standard deviation of the distribution
        """
        # return abs(self.tolerance.T) / (6 * self.C_pk)
        if isinstance(self.distribution, dist.Normal):
            outer_shift = min(
                (self.dim.abs_upper - self.distribution.mean), (self.distribution.mean - self.dim.abs_lower)
            )
            return (self.dim.tolerance.T * self.distribution.std_dev) / (2 * outer_shift)
        return 0

    @property
    def process_sigma_eff(self) -> float:
        """
        calculated sigma (# of eff_std_devs away fromm USL and LSL)
        """
        if self.std_dev_eff == 0:
            return 0
        # print(self.tolerance.upper, self.std_dev_eff)
        # since we are using effective std_dev, either USL or LSL should work.
        min_tol_gap = min((self.dim.abs_upper - self.mean_eff), (self.mean_eff - self.dim.abs_lower))
        return (min_tol_gap) / self.std_dev_eff
        # return 0

    @property
    def k(self) -> float:
        """
        Shift (k) of the distribution

        C_pk = C_p * (1 - k)
        """
        if isinstance(self.distribution, dist.Normal):
            return (self.distribution.mean - self.mean_eff) / (self.dim.tolerance.T / 2)
        return 0

    @property
    def yield_loss_probability(self) -> float:
        """
        Returns the probability of a part being out of spec.
        """
        if self.distribution is None:
            return 0
        return 1 - self.yield_probability

    @property
    def yield_probability(self) -> float:
        """
        Returns the probability of a part being in spec.
        """
        if self.distribution is None:
            return 0
        UL = self.dim.abs_upper
        LL = self.dim.abs_lower
        # return 1 - normal_cdf(UL, self.mean_eff, self.std_dev_eff) + normal_cdf(LL, self.mean_eff, self.std_dev_eff)
        return float(self.distribution.cdf(UL) - self.distribution.cdf(LL))


class ReviewedStack:
    def __init__(
        self,
        name: str = "Stack",
        description: str = "",
        dims: list[Reviewed] = [],
    ):
        self.name = name
        self.description = description
        self.dims = dims

    def __str__(self) -> str:
        return f"{self.name}: {self.dims}"

    def _repr_html_(self):
        return display_df(self.dict, f"REVIEWED DIMENSION STACK: {self.name}", dispmode="html")

    def _display_(self):
        return display_df(self.dict, f"REVIEWED DIMENSION STACK: {self.name}")

    def show(self, expand=False):
        return display_df(self.dict, f"REVIEWED DIMENSION STACK: {self.name}")

    def append(self, measurement: Reviewed):
        """Append a measurement to the stack."""
        self.dims.append(measurement)

    @property
    def dict(self) -> list[dict[str, Any]]:
        return [dim.dict for dim in self.dims]

    def to_basic_stack(self) -> Stack:
        """Convert the stack to a basic stack."""
        return Stack(
            name=self.name,
            description=self.description,
            dims=[rdim.dim for rdim in self.dims],
        )


class Requirement:
    def __init__(self, name, description, distribution: dist.Uniform | dist.Normal | dist.NormalScreened, LL, UL):
        self.name = name
        self.description = description
        # self.dim = dim
        self.distribution = distribution
        self.LL = LL
        self.UL = UL

    def __str__(self) -> str:
        return f"{self.name} [{self.LL}, {self.UL}] {self.distribution}"

    def _repr_html_(self):
        return display_df(self.dict, f"REQUIREMENT: {self.name}", dispmode="html")

    def _display_(self):
        return display_df(self.dict, f"REQUIREMENT: {self.name}")

    def show(self):
        return display_df(self.dict, f"REQUIREMENT: {self.name}")

    @property
    def median(self) -> float:
        """median"""
        return (self.LL + self.UL) / 2

    @property
    def yield_loss_probability(self) -> float:
        """
        Returns the probability of a part being out of spec.
        """
        return 1 - self.yield_probability

    @property
    def yield_probability(self) -> float:
        """
        Returns the probability of a part being in spec.
        """
        return float(self.distribution.cdf(self.UL) - self.distribution.cdf(self.LL))

    @property
    def R(self) -> float:
        """Return the yield loss probability in PPM"""
        return self.yield_loss_probability * 1000000

    @property
    def dict(self) -> list[dict[str, Any]]:
        return [
            {
                "Name": textwrap.shorten(self.name, width=10, placeholder="..."),
                "Desc.": textwrap.shorten(self.description, width=10, placeholder="..."),
                "Distribution": str(self.distribution),
                "Median": nround(self.median),
                "Spec. Limits": f"[{nround(self.LL)}, {nround(self.UL)}]",
                "Yield Prob.": f"{nround(self.yield_probability*100, 8)}" if self.yield_probability is not None else "",
                "Reject PPM": f"{nround(self.R, 2)}",
            }
        ]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
