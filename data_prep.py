# This file formats retrieved data to be displayed to users.

import pandas as pd
import numpy as np
import streamlit as st


def format_data(data, vote_threshold):
    """
    This method takes a list of dictionaries and creates
    a dataframe for visualization.
    """

    df = pd.DataFrame.from_dict(data)

    bins = [-1, 0, 0.5, 0.9, 1.1, 2, np.inf]
    labels = [0, 1, 2, 3, 4, 5]
    df["buckets"] = pd.cut(df["confidence"], bins, labels=labels)
    df = df[df["voteCount"] >= vote_threshold]

    return df.sort_values(["buckets", "title"], ascending=[False, True])


def get_bin(label):
    """
    This method returns the bin of the given confidence label.
    """

    if label == 0:
        return (-1, 0)
    elif label == 1:
        return (0, 0.5)
    elif label == 2:
        return (0.5, 0.9)
    elif label == 3:
        return (0.9, 1.1)
    elif label == 4:
        return (1.1, 2)
    elif label == 5:
        return (2, np.inf)
    else:
        return (None, None)
