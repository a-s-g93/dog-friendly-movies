import streamlit as st
from urllib.error import URLError
from communicator import Communicator
from data_prep import get_bin

if "communicator" not in st.session_state:
    st.session_state["communicator"] = Communicator()

warning_options = st.session_state["communicator"].get_warning_titles()
confidence_options = [
    # (0, "No Data"),
    (1, "Absent"),
    (2, "Not Likely"),
    (3, "Debatable"),
    (4, "Likely"),
    (5, "Present"),
]

try:
    st.header("Mindful Movies")
    st.subheader("Search Warnings")

    with st.form("warning_form"):
        # get list of warnings to search
        selected_warnings = st.multiselect(
            "Select Warnings",
            warning_options,
            format_func=lambda x: x["title"],
            placeholder="Select Warnings...",
        )

        # get confidence level
        conf_start, conf_stop = st.select_slider(
            "Select Confidence Level",
            confidence_options,
            value=[(4, "Likely"), (5, "Present")],
            format_func=lambda x: x[1],
        )

        # set vote threshold for data display
        vote_threshold = st.slider("Select Vote Threshold", 1, 100, 5)

        submit = st.form_submit_button("Search")

    if submit:
        id_list = [x["id"] for x in selected_warnings]

        # get confidence range
        bin_start = get_bin(conf_start[0])[0]
        bin_stop = get_bin(conf_stop[0])[1]

        data = st.session_state["communicator"].get_warning_data(
            id_list, bin_start, bin_stop, vote_threshold
        )

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
