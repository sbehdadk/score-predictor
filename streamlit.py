import streamlit as st
from src.streamlit_components.home import show_home
from src.streamlit_components.dashboard import show_dashboard
from src.streamlit_components.visualization import show_visualization


def main():
    st.title("Navigation")
    selection = st.radio("Go to", ["Home", "Dashboard", "Visualization"])
    if selection == "Home":
        show_home()
    elif selection == "Dashboard":
        show_dashboard()
    elif selection == "Visualization":
        show_visualization()


if __name__ == "__main__":
    main()
