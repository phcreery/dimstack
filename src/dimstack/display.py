import pandas as pd

# from IPython.display import display

# import matplotlib.pyplot as plt


DISPLAY_MODE = "plot"  # "text" or "plot" or "df"
FIGSIZE = (6, 3)


def display_mode(mode: str):
    """Set the display mode for the stack.

    Args:
        mode (str): "text" or "plot"
    """
    global DISPLAY_MODE
    DISPLAY_MODE = mode


def display_df(data: dict, title: str = None):
    """Display a dataframe.

    Args:
        df (pd.DataFrame): _description_
    """

    df = pd.DataFrame(data).astype(str)

    if DISPLAY_MODE == "text":
        if title:
            print(f"{title}")
        print(df.to_string(index=False))
        print()
    # elif DISPLAY_MODE == "plot":
    #     return display(df.style.hide(axis="index").set_caption(title))
    elif DISPLAY_MODE == "df":
        return df
