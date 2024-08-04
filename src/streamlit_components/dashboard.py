import streamlit as st
import requests

api_url = "http://localhost:39132/api/prediction"


def get_prediction(data):
    response = requests.post(api_url, json=data)
    return response.json()


def show_dashboard():
    st.title("Student Performance Prediction Dashboard")

    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    .main {
        background-color: #f5f5f5;
        font-family: 'Roboto', sans-serif;
    }
    .title {
        color: #4CAF50;
    }
    .widget-label {
        font-size: 16px;
        font-weight: bold;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        gender = st.sidebar.selectbox("Gender", ["male", "female"])
        race_ethnicity = st.sidebar.selectbox(
            "Race",
            ["group A", "group B", "group C", "group D", "group E"],
        )
        parental_level_of_education = st.sidebar.selectbox(
            "Parental Level of Education",
            [
                "associate's degree",
                "bachelor's degree",
                "high school",
                "master's degree",
                "some college",
                "some high school",
            ],
        )

    with col2:
        lunch = st.sidebar.selectbox("Lunch", ["free/reduced", "standard"])
        test_preparation_course = st.sidebar.selectbox(
            "Test Preparation Course",
            ["completed", "none"],
        )
        writing_score = st.number_input(
            "Writing Score",
            min_value=0,
            max_value=100,
        )
        reading_score = st.number_input(
            "Reading Score",
            min_value=0,
            max_value=100,
        )

    if st.button("Predict"):
        response = get_prediction(
            data={
                "gender": gender,
                "race_ethnicity": race_ethnicity,
                "parental_level_of_education": parental_level_of_education,
                "lunch": lunch,
                "test_preparation_course": test_preparation_course,
                "writing_score": writing_score,
                "reading_score": reading_score,
            },
        )

        result = response.get("results")
        st.success(f"Predicted Score: {result}")


if __name__ == "__main__":
    show_dashboard()
