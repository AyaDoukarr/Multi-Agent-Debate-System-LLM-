import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
            .main-title {
                font-size: 40px;
                font-weight: 800;
                margin-bottom: 10px;
            }
            .subtitle {
                font-size: 18px;
                color: #666;
                margin-bottom: 20px;
            }
            .box {
                padding: 16px;
                border-radius: 12px;
                background-color: #f7f7f7;
                margin-bottom: 16px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )