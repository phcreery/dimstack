import itertools

from typing import List, Union

from .display import display_df
from .stats import C_p, C_pk, RSS_func, norm_cdf
from .tolerance import SymmetricBilateral, UnequalBilateral, Bilateral
from .utils import nround, sign

POSITIVE = "+"
NEGATIVE = "-"
# DIST_NORMAL = "Normal"  # Normal distribution.
# DIST_SCREENED = "Screened"  # Normal distribution which has been screened. e.g. Go-NoGo or Pass-Fail fixture.
# DIST_NOTCHED = "Notched"  # This is a common distribution when parts are being sorted and the leftover parts are used.
# DIST_NORMAL_LT = "Normal LT"  # Normal distribution which has been screened in order to remove lengths above a limit.
# DIST_NORMAL_GT = "Normal GT"  # Normal distribution which has been screened in order to remove lengths below a limit.


class BasicDimension:
    """
    A measurement is a single measurement of a part.

    Args:
        nom (float, optional): The nominal value of the measurement. Defaults to 0.
        tol (Union[SymmetricBilateral, UnequalBilateral], optional): The tolerance of the measurement. Defaults to SymmetricBilateral(0).
        a (float, optional): The sensitivity of the measurement. Defaults to 1. If the nominal value is negative, the sensitivity will be multiplied by a -1
                            and the nominal value will be made positive.
        process_sigma (float, optional): The standard deviation of the process represented as ±σ. Defaults to ±3σ.
        k (float, optional): The ratio of the amount the center of the distribution is shifted from the mean represented as a multiple of the process
                            standard deviation. Defaults to 0σ.
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
        name: str = "Dimension",
        desc: str = "Dimension",
    ):
        self.id = BasicDimension.newID()
        self.dir = sign(nom)
        self.nominal = abs(nom)
        self.tolerance = tol
        self.a = a * sign(nom)  # sensitivity
        self.name = name
        self.description = desc

    def __repr__(self) -> str:
        return f"{self.id}: {self.name} {self.description} {self.direction}{nround(self.nominal)} {repr(self.tolerance)}"

    def show(self):
        data = [
            {
                "ID": self.id,
                "Name": self.name,
                "Description": (self.description),
                "dir": self.direction,
                "Nom.": nround(self.nominal),
                "Tol.": (repr(self.tolerance)).ljust(14, " "),
                "Sen.": str(self.a),
                "Relative Bounds": f"[{nround(self.lower_rel)}, {nround(self.upper_rel)}]",
                "μ": nround(self.mean),
            }
        ]

        display_df(data, self.name)

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

    @property
    def mean(self):
        return (self.lower_rel + self.upper_rel) / 2

    def convert_to_bilateral(self):
        mean = self.mean
        tol = self.tolerance.T / 2

        self.nominal = mean
        self.tolerance = SymmetricBilateral(tol)
        return self

    @classmethod
    def from_statistical_dimension(
        cls,
        stat: "StatisticalDimension",
    ):
        if type(stat) is BasicDimension:
            return stat
        # print(f"WARNING: Converting {stat} to BasicDimension")
        return cls(
            nom=stat.nominal,
            tol=stat.tolerance,
            a=stat.a,
            name=stat.name,
            desc=stat.description,
        )


class StatisticalDimension(BasicDimension):
    def __init__(
        self,
        process_sigma: float = 3,
        k: float = 0,
        distribution: str = "Normal",
        *args,
        **kwargs,
    ):
        super(StatisticalDimension, self).__init__(*args, **kwargs)
        self.distribution = distribution
        self.process_sigma = process_sigma
        self.k = k

    def __repr__(self) -> str:
        return f"{self.id}: {self.name} {self.description} {self.direction}{nround(self.nominal)} {repr(self.tolerance)} @ ±{self.process_sigma}σ & k={self.k}"

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
        # print(f"WARNING: Converting {basic} to StatisticalDimension")
        return cls(
            nom=basic.nominal,
            tol=basic.tolerance,
            a=basic.a,
            name=basic.name,
            desc=basic.description,
            process_sigma=process_sigma,
            k=k,
            distribution=distribution,
        )

    def show(self):
        data = [
            {
                "ID": self.id,
                "Name": self.name,
                "Description": (self.description),
                "dir": self.direction,
                "Nom.": nround(self.nominal),
                "Tol.": (repr(self.tolerance)).ljust(14, " "),
                "Sen.": nround(self.a),
                "Relative Bounds": f"[{nround(self.lower_rel)}, {nround(self.upper_rel)}]",
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

        display_df(data, self.name)

    @property
    def stdev(self):
        return abs(self.tolerance.T / 2) / self.process_sigma

    # @property
    # def variance(self):
    #     return self.stdev ** 2

    @property
    def C_p(self):
        stdev = abs(self.tolerance.T / 2) / self.process_sigma
        return C_p(self.upper_rel, self.lower_rel, stdev)

    @property
    def C_pk(self):
        return C_pk(self.C_p, self.k)

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
        return 1 - norm_cdf(UL, self.mean, self.stdev) + norm_cdf(LL, self.mean, self.stdev)

    @property
    def yield_probability(self):
        return 1 - self.yield_loss_probability


class Stack:
    def __init__(
        self,
        title: str = "Stack",
        items: List[Union[BasicDimension, StatisticalDimension]] = [],
    ):
        self.title = title
        self.items = items

    def __repr__(self) -> str:
        return f"{self.title}"

    def append(self, measurement: Union[BasicDimension, StatisticalDimension]):
        self.items.append(measurement)

    @property
    def Closed(self) -> BasicDimension:
        nominal = sum([item.nominal * item.a for item in self.items])
        tolerance = Bilateral(
            sum(filter(None, [item.tolerance_absolute.upper for item in self.items])),
            sum(filter(None, [item.tolerance_absolute.lower for item in self.items])),
        )
        return BasicDimension(
            nominal,
            tolerance,
            name="Closed",
            desc=f"{self.title}",
        )

    @property
    def WC(self) -> BasicDimension:
        mean = sum([item.mean * item.a for item in self.items])
        t_wc = sum([abs(item.a * (item.tolerance.T / 2)) for item in self.items])
        tolerance = Bilateral(t_wc)
        return BasicDimension(
            nom=mean,
            tol=tolerance,
            name="WC",
            desc=f"{self.title}",
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
        d_g = sum([item.mean_eff * item.a for item in items])
        t_rss = RSS_func(*[item.a * (item.tolerance.T / 2) for item in items])
        tolerance = Bilateral(t_rss)
        return StatisticalDimension(
            nom=d_g,
            tol=tolerance,
            name="RSS",
            desc=f"{self.title}",
        )

    @property
    def MRSS(self) -> StatisticalDimension:
        items: List[StatisticalDimension] = [StatisticalDimension.from_basic_dimension(item) for item in self.items]
        d_g = sum([item.mean_eff * item.a for item in items])
        t_wc = sum([abs(item.a * (item.tolerance.T / 2)) for item in self.items])
        t_rss = RSS_func(*[item.a * (item.tolerance.T / 2) for item in items])
        n = len(self.items)
        C_f = (0.5 * (t_wc - t_rss)) / (t_rss * (n**0.5 - 1)) + 1
        t_mrss = C_f * t_rss
        tolerance = Bilateral(t_mrss)
        return StatisticalDimension(
            nom=d_g,
            tol=tolerance,
            name="MRSS",
            desc=f"{self.title}",
        )

    def SixSigma(self, at: float = 3) -> StatisticalDimension:
        items: List[StatisticalDimension] = [StatisticalDimension.from_basic_dimension(item) for item in self.items]
        mean = sum([item.mean_eff * item.dir for item in items])
        stdev = RSS_func(*[item.stdev_eff * item.dir for item in items])
        tolerance = Bilateral(stdev * at)
        return StatisticalDimension(
            nom=mean,
            tol=tolerance,
            process_sigma=at,
            name="'6 Sigma'",
            desc=f"{self.title}",
        )

    def show(self):
        data = [
            {
                "ID": item.id,
                "Name": item.name,
                "Description": (item.description),
                "dir": item.direction,
                "Nom.": nround(item.nominal),
                "Tol.": (repr(item.tolerance)).ljust(14, " "),
                "Sen.": f"{nround(item.a)}",
                "Relative Bounds": f"[{nround(item.lower_rel)}, {nround(item.upper_rel)}]",
                # "Absolute Bounds": f"[{nround(item.lower_rel)}, {nround(item.max_rel)}]",
                "Process Sigma": f"± {str(nround(item.process_sigma))}σ" if hasattr(item, "process_sigma") else "",
                "k": nround(item.k) if hasattr(item, "k") else "",
                "C_p": nround(item.C_p) if hasattr(item, "C_p") else "",
                "C_pk": nround(item.C_pk) if hasattr(item, "C_pk") else "",
                "μ": nround(item.mean),
                "σ": nround(item.stdev) if hasattr(item, "stdev") else "",
                "μ_eff": nround(item.mean_eff) if hasattr(item, "mean_eff") else "",
                "σ_eff": nround(item.stdev_eff) if hasattr(item, "stdev_eff") else "",
                "Yield Probability": f"{nround(item.yield_probability*100, 8)}" if hasattr(item, "yield_probability") else "",
                "Reject PPM": f"{nround(item.yield_loss_probability*1000000, 2)}" if hasattr(item, "yield_loss_probability") else "",
            }
            for item in self.items
        ]

        display_df(data, self.title)

    # def show_length_chart(self):
    #     fig, axs = plt.subplots(1, 1, figsize=FIGSIZE, dpi=200)
    #     axs.grid()
    #     axs.set_axisbelow(True)
    #     axs.axvline(0, label="DATUM", alpha=0.6)

    #     # determine rough plot length to size the arrow heads
    #     max = 0
    #     min = 0
    #     last_part_x = 0
    #     for item in self.items:
    #         last_part_x = last_part_x + item.nominal * item.a
    #         if last_part_x > max:
    #             max = last_part_x
    #         if last_part_x < min:
    #             min = last_part_x
    #     head_width = (max + min) * 0.001
    #     # head_width = 0.1

    #     # draw arrows
    #     num_of_parts = len(self.items)
    #     last_part_x = 0
    #     for i in range(num_of_parts):
    #         item = self.items[i]
    #         axs.arrow(
    #             x=last_part_x,
    #             dx=item.nominal * item.a,
    #             y=i,
    #             dy=0,
    #             width=head_width / 5,
    #             length_includes_head=True,
    #             head_width=head_width,
    #             head_length=head_width * 50,
    #             color=(0, 0, 0),
    #         )

    #         last_part_x = last_part_x + item.nominal * item.a
    #     axs.set_yticks(range(len(self.items)))
    #     axs.set_yticklabels([item.name for item in self.items])
    #     axs.invert_yaxis()
    #     axs.set_title("Nominal Stackup Flow Chart")
    #     axs.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    #     fig.tight_layout()

    # return fig


class Assembly:
    def __init__(self, name, description, dim: StatisticalDimension, LL, UL, process_sigma=3):
        self.name = name
        self.description = description
        self.dim = dim
        self.LL = LL
        self.UL = UL
        self.process_sigma = process_sigma

    @property
    def mean(self):
        """mean"""
        return (self.LL + self.UL) / 2

    # @property
    # def stdev(self):
    #     """standard deviation"""
    #     return (self.UL - self.LL) / self.process_sigma

    @property
    def k(self):
        """k"""
        return abs((self.dim.mean - self.mean) / (3 * self.dim.stdev))

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
        return 1 - norm_cdf(self.UL, self.dim.mean, self.dim.stdev) + norm_cdf(self.LL, self.dim.mean, self.dim.stdev)

    @property
    def yield_probability(self):
        return 1 - self.yield_loss_probability

    @property
    def R(self):
        """Return the yield loss probability in PPM"""
        return self.yield_loss_probability * 1000000

    def show(self):
        # members = [attr for attr in dir(obj()) if not callable(getattr(obj(),attr)) and not attr.startswith("__")]
        data = [
            {
                "Name": self.name,
                "Description": (self.description),
                # "dir": self.direction,
                # "Nom.": nround(self.nominal),
                # "Tol.": (repr(self.tolerance)).ljust(14, " "),
                "Relative Bounds": f"[{nround(self.LL)}, {nround(self.UL)}]",
                # "Absolute Bounds": f"[{nround(item.lower_rel)}, {nround(item.max_rel)}]",
                "Process Sigma": f"± {str(nround(self.process_sigma))}σ",
                "k": nround(self.k),
                "C_p": nround(self.C_p),
                "C_pk": nround(self.C_pk),
                "μ": nround(self.mean),
                # "σ": nround(self.stdev),
                "Yield Probability": f"{nround(self.yield_probability*100, 8)}",
                "Reject PPM": f"{nround(self.R, 2)}",
            }
        ]

        display_df(data, self.name)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
