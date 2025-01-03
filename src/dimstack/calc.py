from .dim import Basic, Stack, Reviewed, ReviewedStack
from .stats import rss
from .tolerance import Bilateral
from .dist import Normal


def Closed(self: Stack | ReviewedStack) -> Basic:
    if isinstance(self, Stack):
        dims = self.dims
    elif isinstance(self, ReviewedStack):
        dims = [rdim.dim for rdim in self.dims]

    nominal = sum([dim.dir * dim.nominal * dim.a for dim in dims])

    if nominal < 0:
        # tolerance = Bilateral(
        #     nominal - sum(dim.abs_lower for dim in dims),
        #     nominal - sum(dim.abs_upper for dim in dims),
        # )

        tolerance = Bilateral(
            -sum(dim.abs_lower_tol for dim in dims),
            -sum(dim.abs_upper_tol for dim in dims),
        )
    else:
        # tolerance = Bilateral(
        #     sum(dim.abs_upper for dim in dims) - nominal,
        #     sum(dim.abs_lower for dim in dims) - nominal,
        # )

        tolerance = Bilateral(
            sum(dim.abs_upper_tol for dim in dims),
            sum(dim.abs_lower_tol for dim in dims),
        )

    return Basic(
        nominal,
        tolerance,
        name=f"{self.name} - Closed Analysis",
        desc="",
    )


def WC(self: Stack | ReviewedStack) -> Basic:
    """
    This is a simple WC calculation. This results in a Bilateral dimension with a tolerance that is the sum of the component tolerances.
    It states that in any combination of tolerances, you can be sure the result will be within the this resulting tolerance.
    """

    if isinstance(self, Stack):
        dims = self.dims
    elif isinstance(self, ReviewedStack):
        dims = [rdim.dim for rdim in self.dims]

    mean = sum([dim.dir * dim.median * dim.a for dim in dims])
    t_wc = sum([abs((dim.tolerance.T / 2) * dim.a) for dim in dims])
    tolerance = Bilateral(t_wc)
    return Basic(
        nom=mean,
        tol=tolerance,
        name=f"{self.name} - WC Analysis",
        desc="",
    )


def RSS(self: Stack | ReviewedStack) -> Basic:
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
    if isinstance(self, Stack):
        dims = self.dims
    elif isinstance(self, ReviewedStack):
        dims = [rdim.dim for rdim in self.dims]

    d_g = sum([dim.dir * dim.median * dim.a for dim in dims])
    t_rss = rss([dim.dir * (dim.tolerance.T / 2) * dim.a for dim in dims])
    tolerance = Bilateral(t_rss)
    return Basic(
        nom=d_g,
        tol=tolerance,
        name=f"{self.name} - RSS Analysis",
        desc="(assuming inputs with Normal Dist. & uniform SD)",
    )


def MRSS(self: Stack | ReviewedStack) -> Basic:
    """Basically RSS with a coefficient modifier to make the tolerance tighter.

    Returns:
        Statistical: _description_
    """
    if isinstance(self, Stack):
        dims = self.dims
    elif isinstance(self, ReviewedStack):
        dims = [rdim.dim for rdim in self.dims]

    d_g = sum([dim.dir * dim.median * dim.a for dim in dims])
    t_wc = sum([abs(dim.dir * (dim.tolerance.T / 2) * dim.a) for dim in dims])
    t_rss = rss([dim.dir * dim.a * (dim.tolerance.T / 2) for dim in dims])
    n = len(self.dims)
    C_f = (0.5 * (t_wc - t_rss)) / (t_rss * (n**0.5 - 1)) + 1
    t_mrss = C_f * t_rss
    tolerance = Bilateral(t_mrss)
    return Basic(
        nom=d_g,
        tol=tolerance,
        name=f"{self.name} - MRSS Analysis",
        desc="(assuming inputs with Normal Dist. & uniform SD)",
    )


def SixSigma(self: ReviewedStack, at: float = 3) -> Reviewed:
    # mean = sum([rdim.mean_eff for rdim in self.dims])
    mean = sum([rdim.dim.dir * rdim.dim.median for rdim in self.dims])
    stdev = rss([dim.stdev_eff for dim in self.dims])
    tolerance = Bilateral(stdev * at)
    dist = Normal(mean, stdev)
    dim = Reviewed(
        Basic(
            nom=mean,
            tol=tolerance,
            name=f"{self.name} - '6 Sigma' Analysis",
            desc="(assuming inputs with Normal Dist.)",
        ),
        target_process_sigma=at,
        distribution=dist,
    )
    return dim
