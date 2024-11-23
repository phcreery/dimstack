import itertools
from typing import Union

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .dim import Basic, BasicStack, Reviewed, ReviewedStack
from .dist import Normal, NormalScreened, Uniform


class StackPlot:
    """Plot a stack of dimensions. This is a wrapper around Plotly."""

    start_pos = 0
    color = None

    def __init__(self, title="Stack Plot", x_title="Distance"):
        colors = px.colors.qualitative.Antique
        self.col_pal_iterator = itertools.cycle(colors)

        fig = make_subplots(specs=[[{"secondary_y": True}]], x_title=x_title)
        self.fig = fig
        self.fig.update_yaxes(title_text="Dimension", secondary_y=False)
        self.fig.update_yaxes(title_text="Probability Density", secondary_y=True)
        self.fig.update_layout(go.Layout(title=title))

    def show(self):
        """
        Show the plot. This works in both Jupyter notebooks and in a Python script.
        """
        return self.fig.show()

    def add_dimension(self, item: Basic, title: str | None = None, start_pos: float | None = None, color=None):
        """Add a dimension to the plot.

        Args:
            item (Union[Basic, Reviewed]): _description_
            start_pos (int, optional): _description_. Defaults to None.
        """
        if start_pos is None:
            start_pos = self.start_pos

        prev_pos = start_pos
        if color is None:
            color = self.color

        if title is None:
            title = str(item)

        new_pos = prev_pos + item.nominal * item.dir
        ll = new_pos + item.abs_lower_tol
        ul = new_pos + item.abs_upper_tol

        self.fig.add_trace(
            go.Scatter(
                x=[prev_pos, new_pos],
                y=[item.name, item.name],
                mode="lines+markers+text",
                line=dict(color=color, width=2),
                marker=dict(size=[0, 10]),
                name=f"{item.name} Dimension",
                text=["", f"{title}"],
                textposition="bottom center",
                legendgroup=f"{item.name}",
            )
        )

        self.fig.add_trace(
            go.Scatter(
                x=[new_pos, ll],
                y=[item.name, item.name],
                mode="lines+markers+text",
                line=dict(color="black"),
                marker=dict(size=[0, 10], symbol="line-ns", line_width=2, line_color="black"),
                name=f"{item.name} Upper Tol",
                opacity=0.5,
                legendgroup=f"{item.name}",
            )
        )
        self.fig.add_trace(
            go.Scatter(
                x=[new_pos, ul],
                y=[item.name, item.name],
                mode="lines+markers+text",
                line=dict(color="black"),
                marker=dict(size=[0, 10], symbol="line-ns", line_width=2, line_color="black"),
                name=f"{item.name} Lower Tol",
                opacity=0.5,
                legendgroup=f"{item.name}",
            )
        )

        self.start_pos = new_pos
        return self

    def add_distribution(
        self,
        distribution: Normal | Uniform | NormalScreened,
        name: str,
        start: float,
        stop: float,
        xbins_size=0.1,
        start_pos: float | None = None,
        color=None,
    ):
        """Add a distribution to the plot.

        Args:
            distribution (Union[Normal, Uniform, NormalScreened]): _description_
            name (str): _description_
            xrange (_type_): _description_

        Returns:
            _type_: _description_
        """
        if start_pos is None:
            start_pos = self.start_pos
        if color is None:
            color = self.color

        xrange = np.arange(start, stop, 0.001)
        self.fig.add_trace(
            go.Scatter(
                line=dict(color=color, width=1),
                name=f"{name} Distribution",
                x=xrange + start_pos,
                y=distribution.pdf(xrange),
                legendgroup=f"{name}",
            ),
            secondary_y=True,
        )

        if hasattr(distribution, "data") and distribution.data is not None:
            self.fig.add_histogram(
                x=distribution.data + start_pos,
                histnorm="probability",
                xbins=dict(size=xbins_size),
                name=f"{name} Data",
                marker_color=color,
                opacity=0.5,
                legendgroup=f"{name}",
            )

        return self

    def add_stack(self, stack: BasicStack):
        """Add a stack of dimensions to the plot.

        Args:
            stack (Stack): _description_

        Returns:
            _type_: _description_
        """ """"""
        for item in stack.dims:
            self.add_dimension(item)
            self.color = next(self.col_pal_iterator)

        return self

    def add_reviewed_stack(self, stack: ReviewedStack):
        """Add a stack of reviewed dimensions to the plot.

        Args:
            stack (Stack): _description_

        Returns:
            _type_: _description_
        """ """"""
        for item in stack.dims:
            this_start_pos = self.start_pos
            xbins_size = item.dim.tolerance.T / 10
            self.add_dimension(item.dim, title=str(item))
            self.add_distribution(
                item.distribution,
                item.dim.name,
                item.dim.dir * item.dim.nominal + item.dim.abs_lower_tol,
                item.dim.dir * item.dim.nominal + item.dim.abs_upper_tol,
                # item.dim.dir * item.dim.nominal + item.dim.tolerance.lower,
                # item.dim.dir * item.dim.nominal + item.dim.tolerance.upper,
                xbins_size=xbins_size,
                start_pos=this_start_pos,
            )
            self.color = next(self.col_pal_iterator)

        return self

    def add(self, item: Basic | Reviewed | BasicStack | ReviewedStack):
        """Add a dimension or stack to the plot.

        Args:
            item (Union[Basic, Reviewed, BasicStack, ReviewedStack]): _description_

        Raises:
            TypeError: If the item is not a Basic, Reviewed, BasicStack, or ReviewedStack

        Returns:
            StackPlot: self
        """
        self.color = next(self.col_pal_iterator)

        if isinstance(item, Basic):
            self.add_dimension(item)
        elif isinstance(item, Reviewed):
            this_start_pos = self.start_pos
            xbins_size = item.dim.tolerance.T / 10
            self.add_dimension(item.dim, title=str(item))
            self.add_distribution(
                item.distribution,
                item.dim.name,
                item.dim.nominal + item.dim.abs_lower_tol,
                item.dim.nominal + item.dim.abs_upper_tol,
                # item.dim.dir * item.dim.nominal + item.dim.tolerance.lower,
                # item.dim.dir * item.dim.nominal + item.dim.tolerance.upper,
                xbins_size=xbins_size,
                start_pos=this_start_pos,
            )
        elif isinstance(item, BasicStack):
            self.add_stack(item)
        elif isinstance(item, ReviewedStack):
            self.add_reviewed_stack(item)
        else:
            raise TypeError(f"Cannot add {type(item)} to StackPlot")

        return self
