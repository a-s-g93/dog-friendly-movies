import streamlit as st
from urllib.error import URLError

try:
    st.header("Mindful Movies")


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
