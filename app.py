import streamlit as st
from urllib.error import URLError
from communicator import Communicator

# display columns [PRESENT, NOT PRESENT, UNKNOWN]
# confidence (c)
#   0: Not Present                      | 0   = c
#   1: forgettable / unclear            | 0   < c <= 0.5
#   2:                                  | 0.5 < c <= 0.9
#   3: Some people view it as present   | 0.9 < c <= 1.1
#   4:                                  | 1.1 < c <= 2
#   5: It's there                       | 2   < c

if "communicator" not in st.session_state:
    st.session_state["communicator"] = Communicator()

media_options = st.session_state["communicator"].get_media_titles()

try:
    st.header("Mindful Movies")

    # get list of movies to search
    selected_media = st.selectbox(
        "Select Media",
        media_options,
        format_func=lambda x: x["title"],
        placeholder="Select Media...",
    )

    if st.button("Submit"):
        st.write("Retrieving info for " + selected_media["title"] + "...")
        data = st.session_state["communicator"].get_media_data(selected_media["id"])

        st.header(data["m.title"])
        st.subheader(data["m.releaseYear"])
        st.write(data["m.overview"])


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
# except Exception as e:
#     st.error(
#         """
#         Error occurred %s
#         """
#         % e
#     )
