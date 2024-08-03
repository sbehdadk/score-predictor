import streamlit as st
from src.streamlit.home import show_home
from src.streamlit.dashboard import show_dashboard
from src.streamlit.visualization import show_visualization


def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Dashboard", "Visualization"])
    if selection == "Home":
        show_home()
    elif selection == "Dashboard":
        show_dashboard()
    elif selection == "Visualization":
        show_visualization()


if __name__ == "__main__":
    main()
