# This file formats retrieved data to be displayed to users.

import pandas as pd
import numpy as np
import streamlit as st


def format_data(data):
    """
    This method takes a list of dictionaries and creates
    a dataframe for visualization.
    """

    df = pd.DataFrame.from_dict(data)

    print(df)
