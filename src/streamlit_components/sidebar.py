import streamlit as st
from pathlib import Path
from PIL import Image


def show_sidebar():
    st.sidebar.title("Student Performance Prediction")
    img = Image.open(Path(__file__).parents[1] / "data/score-predictor-logo.jpg")

    st.sidebar.image(img, use_column_width=True, width=50)

    st.sidebar.header("About score-predictor")

    st.sidebar.markdown("""
    ### Overview
    Developed a comprehensive machine learning pipeline using a Kaggle dataset. The solution includes data cleaning, feature engineering, exploratory data analysis (EDA), model training, and deployment.

    ### Key Components
    1. **Data Preprocessing**: Handled missing values, created and selected features.
    2. **EDA**: Analyzed data distributions and correlations.
    3. **ML Pipelines**: Built and optimized training and prediction pipelines.
    4. **API Development**: Created a backend with FastAPI and Uvicorn.
    5. **Frontend Development**: Built an interactive frontend with Streamlit.
    6. **Deployment**: Dockerized the project, implemented CI/CD with GitHub Actions, and deployed on Hugging Face with Nginx proxy.
                        
    ### Summary
    Demonstrated expertise in building and deploying scalable ML solutions with modern tools and frameworks, ensuring efficiency and reproducibility.
    """)
