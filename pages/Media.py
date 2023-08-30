import streamlit as st
from urllib.error import URLError
from communicator import Communicator
import data_prep

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
    st.subheader("Search Media")

    # get list of movies to search
    selected_media = st.selectbox(
        "Select Media",
        media_options,
        format_func=lambda x: x["title"],
        placeholder="Select Media...",
    )

    # set vote threshold for data display
    vote_threshold = st.slider("Select Vote Threshold", 1, 100, 5)

    # if st.button("Submit"):
    # st.write("Retrieving info for " + selected_media["title"] + "...")
    data = st.session_state["communicator"].get_media_data(selected_media["id"])

    st.header(data["m.title"])
    st.subheader(data["m.releaseYear"])
    st.write(data["m.overview"])

    formatted_data = data_prep.format_data(data["trigger"], vote_threshold)

    st.divider()
    st.subheader("Present")

    count5 = len(formatted_data[formatted_data["buckets"] == 5])
    count4 = len(formatted_data[formatted_data["buckets"] == 4])
    count3 = len(formatted_data[formatted_data["buckets"] == 3])
    count2 = len(formatted_data[formatted_data["buckets"] == 2])
    count1 = len(formatted_data[formatted_data["buckets"] == 1])
    count0 = len(formatted_data[formatted_data["buckets"] == 0])

    col15, col25, col35 = st.columns(3)
    for idx, row in (
        formatted_data[formatted_data["buckets"] == 5].reset_index().iterrows()
    ):
        # print(row)
        # st.subheader(row["title"])
        # st.write("votes: ", int(row["voteCount"]), " y/n ratio: ", row["confidence"])
        # if row["description"] is not None:
        #     st.write(row["description"])
        if idx < count5 / 3.0:
            col15.markdown(f":red[{row['title']}]", help=row["description"])
        elif idx > count5 / 3.0 * 2.0:
            col35.markdown(f":red[{row['title']}]", help=row["description"])
        else:
            col25.markdown(f":red[{row['title']}]", help=row["description"])

    col14, col24, col34 = st.columns(3)
    for idx, row in (
        formatted_data[formatted_data["buckets"] == 4].reset_index().iterrows()
    ):
        if idx < count4 / 3.0:
            col14.markdown(f":orange[{row['title']}]", help=row["description"])
        elif idx > count4 / 3.0 * 2.0:
            col34.markdown(f":orange[{row['title']}]", help=row["description"])
        else:
            col24.markdown(f":orange[{row['title']}]", help=row["description"])

    st.divider()
    st.subheader("Debatably Present")
    print(count3)
    col13, col23, col33 = st.columns(3)
    for idx, row in (
        formatted_data[formatted_data["buckets"] == 3].reset_index().iterrows()
    ):
        if idx < count3 / 3.0:
            col13.markdown(f":violet[{row['title']}]", help=row["description"])
        elif idx > count3 / 3.0 * 2.0:
            col33.markdown(f":violet[{row['title']}]", help=row["description"])
        else:
            col23.markdown(f":violet[{row['title']}]", help=row["description"])

    st.divider()
    st.subheader("Missable / Not Present")

    col12, col22, col32 = st.columns(3)
    for idx, row in (
        formatted_data[formatted_data["buckets"] == 2].reset_index().iterrows()
    ):
        if idx < count2 / 3.0:
            col12.markdown(f":blue[{row['title']}]", help=row["description"])
        elif idx > count2 / 3.0 * 2.0:
            col32.markdown(f":blue[{row['title']}]", help=row["description"])
        else:
            col22.markdown(f":blue[{row['title']}]", help=row["description"])

    col11, col21, col31 = st.columns(3)
    for idx, row in (
        formatted_data[formatted_data["buckets"] == 1].reset_index().iterrows()
    ):
        if idx < count1 / 3.0:
            col11.markdown(f":green[{row['title']}]", help=row["description"])
        elif idx > count1 / 3.0 * 2.0:
            col31.markdown(f":green[{row['title']}]", help=row["description"])
        else:
            col21.markdown(f":green[{row['title']}]", help=row["description"])

    st.divider()
    st.subheader("Not Found")

    col10, col20, col30 = st.columns(3)
    for idx, row in (
        formatted_data[formatted_data["buckets"] == 0].reset_index().iterrows()
    ):
        if idx < count0 / 3.0:
            col10.markdown(f":gray[{row['title']}]", help=row["description"])
        elif idx > count0 / 3.0 * 2.0:
            col30.markdown(f":gray[{row['title']}]", help=row["description"])
        else:
            col20.markdown(f":gray[{row['title']}]", help=row["description"])

    # st.dataframe(formatted_data)
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
