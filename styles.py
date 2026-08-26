import streamlit as st


def load_styles():

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0f1117;
        }

        .block-container {
            max-width: 900px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }

        h1 {
            text-align: center;
        }

        .stCaption {
            text-align: center;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #181b24;
            border-radius: 16px;
            border: 1px solid #292d38;
            padding: 10px;
        }

        div.stButton > button {
            border-radius: 10px;
            font-weight: 600;
            min-height: 45px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )