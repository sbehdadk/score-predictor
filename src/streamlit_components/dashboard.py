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
        # select a gender
        gender = st.selectbox("Gender", ["Select a gender...", "male", "female"])

        # select a race/ethnicity
        race_ethnicity = st.selectbox(
            "Race",
            [
                "Select a race group...",
                "group A",
                "group B",
                "group C",
                "group D",
                "group E",
            ],
            index=0,
        )
        # select a parent level of education
        parental_level_of_education = st.selectbox(
            "Parental Level of Education",
            [
                "Select a degree...",
                "associate's degree",
                "bachelor's degree",
                "high school",
                "master's degree",
                "some college",
                "some high school",
            ],
            index=0,
        )

    with col2:
        # select a lunch option
        lunch = st.selectbox(
            "Lunch", ["Select a lunch type...", "free/reduced", "standard"]
        )

        # select a test preparation course
        test_preparation_course = st.selectbox(
            "Test Preparation Course",
            ["Select a preparation course...", "completed", "none"],
            index=0,
        )

    # select a writing score
    writing_score = st.select_slider(
        "Writing Score",
        options=list(range(101)),
        value=0,
    )

    st.markdown(
        f"""
        <div style="text-align: center; font-size: 16px; color: gray;">
            🌟✨ writing score: <span style="font-weight: bold;">{writing_score}</span> ✨🌟
        </div>
        """,
        unsafe_allow_html=True,
    )

    # select a reading score
    reading_score = st.select_slider(
        "Reading Score",
        options=list(range(101)),
        value=0,
    )

    # Display the selected value with fantasy flair
    st.markdown(
        f"""
        <div style="text-align: center; font-size: 16px; color: gray;">
            🌟✨ Reading score: <span style="font-weight: bold;">{reading_score}</span> ✨🌟
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Predict"):
        if any(
            [
                gender == "Select a gender...",
                race_ethnicity == "Select a race group...",
                parental_level_of_education == "Select a degree...",
                lunch == "Select a lunch type...",
                reading_score == 0,
                writing_score == 0,
                test_preparation_course == "Select a preparation course...",
            ]
        ):
            st.warning("Please fill out all fields before making a prediction.")
            ...
        else:
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
            if result is not None:
                st.write("The predicted score is:")
                st.markdown(
                    f"""
                    <div style="
                        background-color: #d4edda;
                        border: 1px solid #c3e6cb;
                        color: #155724;
                        padding: 10px;
                        border-radius: 5px;
                        text-align: center;
                        font-size: 24px;
                        font-weight: bold;
                    ">
                        {result}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.error("There was an error with the prediction, Please try again...")


if __name__ == "__main__":
    show_dashboard()
