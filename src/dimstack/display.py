from typing import Any, Iterable
from enum import Enum

import pandas as pd
from rich.console import Console
from rich.table import Table


class DisplayMode(Enum):
    """Display modes for the stack.

    Args:
        TEXT (str): Text mode
        STRING (str): String mode
        HTML (str): HTML mode
        RICH (str): Rich mode
        NOTEBOOK (str): Notebook mode
        DF (str): DataFrame mode
    """

    TEXT = "text"
    STRING = "string"
    HTML = "html"
    RICH = "rich"
    NOTEBOOK = "notebook"
    DF = "df"


DISPLAY_MODE = DisplayMode.TEXT
FIGSIZE = (6, 3)


def mode(dispmode: DisplayMode | str):
    """Set the display mode for the stack.

    Args:
        dispmode (DisplayMode | str): Display mode to set.
    """
    global DISPLAY_MODE
    DISPLAY_MODE = dispmode


def display_df(data: Iterable[dict[Any, Any]], title: str = "", dispmode=None):
    """Display a dataframe.

    Args:
        df (pd.DataFrame): _description_
    """
    if dispmode is None:
        dispmode = DISPLAY_MODE

    df = pd.DataFrame(data).astype(str)

    if dispmode == DisplayMode.TEXT:
        if title:
            print(f"{title}")
        print(df.to_string(index=False))
        print()
    elif dispmode == DisplayMode.STRING:
        return df.to_string(index=False)
    elif dispmode == DisplayMode.HTML:
        return df.style.hide(axis="index").set_caption(title).set_properties(**{"text-align": "left"})
    elif dispmode == DisplayMode.NOTEBOOK:
        return df.style.hide(axis="index").set_caption(title).set_properties(**{"text-align": "left"})
    # elif dispmode == "dict":
    #     print(df.to_dict())
    elif dispmode == DisplayMode.DF:
        return df
    elif dispmode == DisplayMode.RICH:
        console = Console()
        table = Table(title=title)
        for col in df.columns:
            table.add_column(col)
        for row in df.itertuples(index=False):
            table.add_row(*row)
        console.print(table)
        print()
    else:
        return data
