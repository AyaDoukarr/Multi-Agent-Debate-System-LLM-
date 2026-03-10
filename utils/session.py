import streamlit as st


def init_session_state():
    if "debat_genere" not in st.session_state:
        st.session_state.debat_genere = None

    if "history" not in st.session_state:
        st.session_state.history = []