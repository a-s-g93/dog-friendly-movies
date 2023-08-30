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
