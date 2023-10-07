import streamlit as st
from streamlit_option_menu import option_menu

from page.home import home
# from page.home import search_movies

st.set_page_config(page_title="Mini-Search", page_icon="🤖", layout="wide")

page_names_to_funcs = {
    "Home": home,
    # "Search Movies": search_movies,
}

with st.sidebar:
    page_name = option_menu(
        menu_title="Select a Demo",
        options=list(page_names_to_funcs.keys()),
        # Remark https://icons.getbootstrap.com/ for icons
        icons=["house", "hand-thumbs-up", "person", "people"],
        menu_icon="app-indicator",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

page_names_to_funcs[page_name]()
