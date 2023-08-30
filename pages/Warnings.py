import streamlit as st
from urllib.error import URLError
from communicator import Communicator

if "communicator" not in st.session_state:
    st.session_state["communicator"] = Communicator()

warning_options = st.session_state["communicator"].get_warning_titles()

try:
    st.header("Mindful Movies")
    st.subheader("Search Warnings")

    # get list of warnings to search
    selected_warnings = st.multiselect(
        "Select Warnings",
        warning_options,
        format_func=lambda x: x["title"],
        placeholder="Select Warnings...",
    )

    # set vote threshold for data display
    vote_threshold = st.slider("Select Vote Threshold", 1, 100, 5)

    id_list = [x["id"] for x in selected_warnings]

    data = st.session_state["communicator"].get_warning_data(id_list)

    for media in data:
        st.write(media["m.title"] + " - " + media["m.type"])
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
