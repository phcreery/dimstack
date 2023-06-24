# from . import eval
from . import dim
from . import stats
from . import display
from . import tolerance
from . import utils
from . import dist
from . import plot

from .dim import Statistical, Basic, Stack, Spec
from .dist import Normal, Uniform  # , Triangular, LogNormal, Weibull, Exponential, Gamma, Beta, Gumbel, Frechet
from . import tolerance as tol

__all__ = ["dim", "stats", "display", "tolerance", "utils", "dist", "plot"]

__version__ = "0.1.0"
