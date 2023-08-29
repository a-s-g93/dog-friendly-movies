import streamlit as st
from urllib.error import URLError


try:
    st.write("hello world!")

    # get list of movies to search

    # display columns [PRESENT, NOT PRESENT, UNKNOWN]
    # confidence (c)
    #   0: Not Present                      | 0   = c
    #   1: forgettable / unclear            | 0   < c <= 0.5
    #   2:                                  | 0.5 < c <= 0.9
    #   3: Some people view it as present   | 0.9 < c <= 1.1
    #   4:                                  | 1.1 < c <= 2
    #   5: It's there                       | 2   < c


# ------------------------------------
# ERRORS -----------------------------
# ------------------------------------
except URLError as e:
    st.error(
        """
        **This app requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
except Exception as e:
    st.error(
        """
        Error occurred %s
        """
        % e
    )
