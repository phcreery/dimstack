from typing import Any, Iterable

import pandas as pd
from rich.console import Console
from rich.table import Table

DISPLAY_MODE = "text"
FIGSIZE = (6, 3)


def mode(dispmode: str):
    """Set the display mode for the stack.

    Args:
        mode (str): "text"/"txt", "str"/"string", "html", "rich", "notebook", or "df"
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

    if dispmode == "text" or dispmode == "txt":
        if title:
            print(f"{title}")
        print(df.to_string(index=False))
        print()
    elif dispmode == "string" or dispmode == "str":
        return df.to_string(index=False)
    elif dispmode == "html":
        return df.style.hide(axis="index").set_caption(title)
    elif dispmode == "notebook":
        return df.style.hide(axis="index").set_caption(title)
    # elif dispmode == "dict":
    #     print(df.to_dict())
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
        print()
    else:
        return data
