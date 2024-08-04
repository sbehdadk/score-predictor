import app_streamlit as st


def show_home():
    st.title("Student Performance Prediction")

    st.subheader("Welcome to our Student Performance Prediction App!")

    st.write(
        "This app uses machine learning to predict student performance based on various factors."
    )

    st.write("Please enter your data to get started.")
