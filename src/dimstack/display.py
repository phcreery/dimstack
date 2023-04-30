import pandas as pd


DISPLAY_MODE = "text"  # "text", "str"/"string", "plot", or "df"
FIGSIZE = (6, 3)


def mode(dispmode: str):
    """Set the display mode for the stack.

    Args:
        mode (str): "text", "str"/'string, "plot", or "df"
    """
    global DISPLAY_MODE
    DISPLAY_MODE = dispmode


def display_df(data: dict, title: str = None, dispmode=None) -> pd.DataFrame:
    """Display a dataframe.

    Args:
        df (pd.DataFrame): _description_
    """
    if dispmode is None:
        dispmode = DISPLAY_MODE

    df = pd.DataFrame(data).astype(str)

    if dispmode == "text":
        if title:
            print(f"{title}")
        print(df.to_string(index=False))
        print()
    if dispmode == "string" or dispmode == "str":
        return df.to_string(index=False)
    elif dispmode == "plot":
        return df.style.hide(axis="index").set_caption(title)
    elif dispmode == "df":
        return df
    else:
        return data
