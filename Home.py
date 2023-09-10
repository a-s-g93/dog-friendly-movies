import streamlit as st
from urllib.error import URLError

try:
    st.header("Mindful Movies")

    with open("ui/sidebar.md", "r") as sidebar_file:
        sidebar_content = sidebar_file.read()

    st.sidebar.markdown(sidebar_content)

    st.markdown(sidebar_content)

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
