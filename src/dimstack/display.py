from typing import Any, Dict, Iterable

import pandas as pd
from rich.console import Console
from rich.table import Table

DISPLAY_MODE = "text"
FIGSIZE = (6, 3)


def mode(dispmode: str):
    """Set the display mode for the stack.

    Args:
        mode (str): "text"/"txt", "str"/"string", "plot", "rich", or "df"
    """
    global DISPLAY_MODE
    DISPLAY_MODE = dispmode


def display_df(data: Iterable[Dict[Any, Any]], title: str = "", dispmode=None):
    """Display a dataframe.

    Args:
        df (pd.DataFrame): _description_
    """
    if dispmode is None:
        dispmode = DISPLAY_MODE

    df = pd.DataFrame(data).astype(str)

    if dispmode == "text" or dispmode == "txt":
        if title:
            print(f"{title}")
        print(df.to_string(index=False))
        print()
    elif dispmode == "string" or dispmode == "str":
        return df.to_string(index=False)
    elif dispmode == "plot":
        return df.style.hide(axis="index").set_caption(title)
    elif dispmode == "df":
        return df
    elif dispmode == "rich":
        console = Console()
        table = Table(title=title)
        for col in df.columns:
            table.add_column(col)
        for row in df.itertuples(index=False):
            table.add_row(*row)
        console.print(table)
    else:
        return data
