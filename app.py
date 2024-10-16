import streamlit as st
from modules import sentiment_analysis
from modules import pdf_compare

def main():

    st.sidebar.title("Navigation")
    choice = st.sidebar.radio('Select a page:', list(PAGES.keys()))

    if choice in PAGES:
        PAGES[choice].main()

PAGES = {
    "PDF Compare": pdf_compare
}

if __name__ == "__main__":
    main()