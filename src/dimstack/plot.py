import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
import itertools
from .eval import Stack


def plot_stack(stack: Stack):
    colors = px.colors.qualitative.Plotly
    col_pal_iterator = itertools.cycle(colors)

    # fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]], x_title="Distance (mm)")

    prev_pos = 0
    for item in stack.items:
        color = next(col_pal_iterator)

        new_pos = prev_pos + item.nominal * item.dir
        ll = min(new_pos + item.tolerance.upper * item.dir, new_pos - item.tolerance.lower * item.dir)
        ul = max(new_pos + item.tolerance.upper * item.dir, new_pos - item.tolerance.lower * item.dir)

        fig.add_trace(
            go.Scatter(
                x=[prev_pos, new_pos],
                y=[item.name, item.name],
                mode="lines+markers+text",
                line=dict(color=color, width=2),
                marker=dict(size=[0, 10]),
                name=item.name,
                text=["", repr(item)],
                textposition="bottom center",
                legendgroup=f"{item.name}",
            )
        )

        fig.add_trace(
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
        fig.add_trace(
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
        fig.add_trace(
            go.Scatter(
                line=dict(color=color, width=1),
                name=f"{item.name} Distribution",
                x=xrange * item.dir + prev_pos,
                y=item.get_dist().pdf(xrange) * 0.001 * 100,
                legendgroup=f"{item.name}",
            ),
            secondary_y=True,
        )

        prev_pos = new_pos

    fig.update_yaxes(title_text="Dimension", secondary_y=False)
    fig.update_yaxes(title_text="Probability Density", secondary_y=True)
    fig.update_layout(go.Layout(title=f"Dimension chart of: {stack.title}"))
    fig.show()
