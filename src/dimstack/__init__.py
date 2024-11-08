# from . import eval
from . import dim, display, dist, plot, stats, tolerance, utils
from . import tolerance as tol
from .dim import Basic, Spec, Stack, Statistical
from .dist import Normal, Uniform  # , Triangular, LogNormal, Weibull, Exponential, Gamma, Beta, Gumbel, Frechet

__all__ = ["dim", "stats", "display", "tolerance", "utils", "dist", "plot"]

# __version__ = "0.1.0"
