from typing import Union
import itertools

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

from .dim import Stack, Basic, Statistical


class StackPlot:
    """Plot a stack of dimensions. This is a wrapper around Plotly."""

    def __init__(self, title="Stack Plot", x_title="Distance"):
        colors = px.colors.qualitative.Plotly
        self.col_pal_iterator = itertools.cycle(colors)

        # fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]], x_title=x_title)
        self.fig = fig
        self.fig.update_yaxes(title_text="Dimension", secondary_y=False)
        self.fig.update_yaxes(title_text="Probability Density", secondary_y=True)
        self.fig.update_layout(go.Layout(title=title))

    def show(self):
        """Show the plot. This works in both Jupyter notebooks and in a Python script."""
        return self.fig.show()

    def add_dimension(self, item: Union[Basic, Statistical], start_pos: float = 0):
        """Add a dimension to the plot.

        Args:
            item (Union[Basic, Statistical]): _description_
            start_pos (int, optional): _description_. Defaults to 0.
        """
        prev_pos = start_pos
        color = next(self.col_pal_iterator)

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
                name=item.name,
                text=["", str(item)],
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

        # plot the default distribution
        xrange = np.arange(item.nominal + item.abs_lower_tol, item.nominal + item.abs_upper_tol, 0.001)
        if hasattr(item, "distribution") and item.distribution is not None:
            self.fig.add_trace(
                go.Scatter(
                    line=dict(color=color, width=1),
                    name=f"{item.name} Distribution",
                    x=xrange + prev_pos,
                    y=item.distribution.pdf(xrange),
                    legendgroup=f"{item.name}",
                ),
                secondary_y=True,
            )
            # plot any alternate distributions
            # for dist in item.get_alt_dists():
            #     self.fig.add_trace(
            #         go.Scatter(
            #             line=dict(color=color, width=1),
            #             name=f"{item.name} Distribution",
            #             x=xrange * item.dir + prev_pos,
            #             y=dist.pdf(xrange),
            #             legendgroup=f"{item.name}",
            #             opacity=0.5,
            #         ),
            #         secondary_y=True,
            #     )

            if hasattr(item.distribution, "data") and item.distribution.data is not None:
                self.fig.add_histogram(
                    x=item.distribution.data,
                    histnorm="probability",
                    xbins=dict(size=0.1),
                    name=f"{item.name} Data",
                    legendgroup=f"{item.name}",
                    marker_color=color,
                    opacity=0.5,
                )

    def add_stack(self, stack: Stack):
        """Add a stack of dimensions to the plot.

        Args:
            stack (Stack): _description_

        Returns:
            _type_: _description_
        """ """"""
        prev_pos = 0
        for item in stack.dims:
            new_pos = prev_pos + item.nominal * item.dir
            self.add_dimension(item, start_pos=prev_pos)
            prev_pos = new_pos

        self.fig.update_layout(go.Layout(title=stack.name))

        return self

    def add(self, item: Union[Stack, Basic, Statistical]):
        """Add a dimension or stack to the plot.

        Args:
            item (Stack, Basic, Statistical): _description_

        Raises:
            TypeError: If the item is not a Stack, Basic, or Statistical.

        Returns:
            StackPlot: self
        """
        if isinstance(item, Stack):
            self.add_stack(item)
        elif isinstance(item, (Basic, Statistical)):
            self.add_dimension(item)
        else:
            raise TypeError(f"Cannot add {type(item)} to StackPlot")

        return self
