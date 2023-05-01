from . import eval
from . import stats
from . import display
from . import tolerance
from . import utils
from . import dist
from . import plot

from .eval import StatisticalDimension, BasicDimension, Stack, Spec
from .dist import Normal, Uniform  # , Triangular, LogNormal, Weibull, Exponential, Gamma, Beta, Gumbel, Frechet
from . import tolerance as tol

__all__ = ["eval", "stats", "display", "tolerance", "utils", "dist", "plot"]

__version__ = "0.1.0"
