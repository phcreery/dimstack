from typing import Union
import itertools

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

from .eval import Stack, BasicDimension, StatisticalDimension


class StackPlot:
    def __init__(self):
        colors = px.colors.qualitative.Plotly
        self.col_pal_iterator = itertools.cycle(colors)

        # fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]], x_title="Distance (mm)")
        self.fig = fig
        self.fig.update_yaxes(title_text="Dimension", secondary_y=False)
        self.fig.update_yaxes(title_text="Probability Density", secondary_y=True)
        self.fig.update_layout(go.Layout(title="Dimension chart"))

    def show(self):
        return self.fig.show()

    def add_dimension(self, item: Union[BasicDimension, StatisticalDimension], start_pos=0):
        prev_pos = start_pos
        color = next(self.col_pal_iterator)

        new_pos = prev_pos + item.nominal * item.dir
        ll = min(new_pos + item.tolerance.upper * item.dir, new_pos - item.tolerance.lower * item.dir)
        ul = max(new_pos + item.tolerance.upper * item.dir, new_pos - item.tolerance.lower * item.dir)

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

        ul = max(item.nominal + item.tolerance.upper, item.nominal - item.tolerance.lower)
        ll = min(item.nominal + item.tolerance.upper, item.nominal - item.tolerance.lower)
        xrange = np.arange(ll, ul, 0.001)
        # plot the default distribution
        self.fig.add_trace(
            go.Scatter(
                line=dict(color=color, width=1),
                name=f"{item.name} Distribution",
                x=xrange * item.dir + prev_pos,
                y=item.get_dist().pdf(xrange),
                legendgroup=f"{item.name}",
            ),
            secondary_y=True,
        )
        # plot any alternate distributions
        for dist in item.get_alt_dists():
            self.fig.add_trace(
                go.Scatter(
                    line=dict(color=color, width=1),
                    name=f"{item.name} Distribution",
                    x=xrange * item.dir + prev_pos,
                    y=dist.pdf(xrange),
                    legendgroup=f"{item.name}",
                    opacity=0.5,
                ),
                secondary_y=True,
            )

        if hasattr(item, "data") and item.data is not None:
            self.fig.add_histogram(
                x=item.data,
                histnorm="probability",
                xbins=dict(size=0.1),
                name=f"{item.name} Data",
                legendgroup=f"{item.name}",
                marker_color=color,
                opacity=0.5,
            )

    def add_stack(self, stack: Stack):
        prev_pos = 0
        for item in stack.items:
            new_pos = prev_pos + item.nominal * item.dir
            self.add_dimension(item, start_pos=prev_pos)
            prev_pos = new_pos

        return self

    def add(self, item):
        if isinstance(item, Stack):
            self.add_stack(item)
        elif isinstance(item, (BasicDimension, StatisticalDimension)):
            self.add_dimension(item)
        else:
            raise TypeError(f"Cannot add {type(item)} to StackPlot")

        return self
