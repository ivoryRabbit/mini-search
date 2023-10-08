import pandas as pd
import streamlit as st
from requests import Session

from config.client import backend_url


def search_movies(session: Session = Session()):
    st.title("Search Movies")

    if "relevant_movies" not in st.session_state:
        st.session_state["relevant_movies"] = None

    def request_search():
        url = f"{backend_url}/search/movies"
        params = {"query": st.session_state["query"], "size": 10}

        response = session.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
        else:
            data = None

        st.session_state["relevant_movies"] = data

    with st.form(key="form"):
        st.text_input("👇 Enter your keyword", placeholder="Title", key="query")

        st.form_submit_button(
            label="Search",
            use_container_width=True,
            on_click=request_search,
        )

    result = st.session_state["relevant_movies"]

    if result is None or len(result) == 0:
        st.stop()
        return

    fields = ["id", "title", "genres", "year", "view", "rating"]

    st.subheader("[Relevant Movies]")

    st.data_editor(
        pd.DataFrame(result)[fields],
        column_config={
            "id": st.column_config.Column(
                "Movie ID",
                help="ID of movie",
                width="small",
                required=True,
            ),
            "title": st.column_config.Column(
                "Title",
                help="Title of movie",
                width="medium",
            ),
            "genres": st.column_config.Column(
                "Genres",
                help="Genres of movie",
                width="large",
            ),
            "year": st.column_config.TextColumn(
                "Release",
                help="Movie release year",
                max_chars=4,
                validate=r"^\d{4}$",
            ),
            "view": st.column_config.ProgressColumn(
                "View Count",
                help="Count of total view",
                width="medium",
                format="%f",
                min_value=0,
                max_value=result[0]["view"],
            ),
            "rating": st.column_config.ProgressColumn(
                "Avg Rating",
                help="Average of rating",
                width="medium",
                format="%.2f",
                min_value=0.0,
                max_value=5.0,
            ),
        },
        disabled=fields,
        hide_index=True,
        width=1200,
        key="search"
    )
