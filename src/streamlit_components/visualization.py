import streamlit as st
import pandas as pd


def show_visualization():
    st.title("Data Visualization")

    st.subheader("Visualize your data using various charts and graphs.")

    st.write("Please upload your data file to visualize it.")

    uploaded_file = st.file_uploader("Upload your data file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        st.write("Data preview:")
        st.dataframe(data.head())

        st.subheader("Bar chart")
        st.bar_chart(data["column_name"])

        st.subheader("Line chart")
        st.line_chart(data["column_name"])

        st.subheader("Pie chart")
        st.pie_chart(data["column_name"])

        st.subheader("Scatter plot")
        st.scatter_chart(data)
