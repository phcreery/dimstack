from typing import List

from .dim import Basic, Stack, Statistical
from .stats import rss
from .tolerance import Bilateral


def Closed(self: Stack) -> Basic:
    nominal = sum([dim.dir * dim.nominal * dim.a for dim in self.dims])
    tolerance = Bilateral(
        sum(filter(None, [dim.abs_upper_tol for dim in self.dims])),
        sum(filter(None, [dim.abs_lower_tol for dim in self.dims])),
    )
    return Basic(
        nominal,
        tolerance,
        name=f"{self.name} - Closed Analysis",
        desc="",
    )


def WC(self: Stack) -> Basic:
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


def RSS(self: Stack) -> Statistical:
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
    t_rss = rss([dim.dir * (dim.tolerance.T / 2) * dim.a for dim in dims])
    tolerance = Bilateral(t_rss)
    return Statistical(
        nom=d_g,
        tol=tolerance,
        name=f"{self.name} - RSS Analysis",
        desc="(assuming inputs with Normal Dist. & uniform SD)",
    ).assume_normal_dist()


def MRSS(self: Stack) -> Statistical:
    """Basically RSS with a coefficient modifier to make the tolerance tighter.

    Returns:
        Statistical: _description_
    """
    dims: List[Statistical] = [Statistical.from_basic_dimension(dim) for dim in self.dims]
    d_g = sum([dim.dir * dim.median * dim.a for dim in dims])
    t_wc = sum([abs(dim.dir * (dim.tolerance.T / 2) * dim.a) for dim in dims])
    t_rss = rss([dim.dir * dim.a * (dim.tolerance.T / 2) for dim in dims])
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
        desc="(assuming inputs with Normal Dist. & uniform SD)",
        target_process_sigma=sigma,
    ).assume_normal_dist()


def SixSigma(self: Stack, at: float = 3) -> Statistical:
    dims: List[Statistical] = [Statistical.from_basic_dimension(dim).assume_normal_dist() for dim in self.dims]
    mean = sum([dim.dir * dim.median for dim in dims])
    stdev = rss([dim.stdev_eff for dim in dims])
    tolerance = Bilateral(stdev * at)
    dim = Statistical(
        nom=mean,
        tol=tolerance,
        target_process_sigma=at,
        name=f"{self.name} - '6 Sigma' Analysis",
        desc="(assuming inputs with Normal Dist.)",
    )
    dim.assume_normal_dist()
    return dim
