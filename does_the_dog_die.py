# This file interacts with the doesthedogdie.com API to retrieve data.

import requests
import streamlit as st


def get_media(media_id: int):
    """
    This method retrieves the media JSON data from dtdd.com
    """

    headers = {"Accept": "application/json", "X-API-KEY": st.secrets["dtdd_key"]}
    address = f"https://www.doesthedogdie.com/media/{str(media_id)}"
    data = requests.get(address, headers=headers).json()

    return data["item"], data["topicItemStats"]
