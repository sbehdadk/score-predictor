import streamlit as st
from PIL import Image
from pathlib import Path
from src.streamlit_components.sidebar import show_sidebar
from src.streamlit_components.dashboard import show_dashboard


def main():
    st.header(
        "🚀 Score predictor🚀 ",
    )
    show_sidebar()

    # Tabs for detailed sections
    tabs = st.tabs(
        [
            "Dashboard",
            "Data Preprocessing",
            "EDA",
            "ML Pipelines",
            "API & Frontend",
            "Deployment",
        ]
    )
    with tabs[0]:
        st.header("Prediction Dashboard")
        show_dashboard()

    with tabs[1]:
        st.header("Data Preprocessing")
        img_path = Path(__file__).parents[1] / "src/data/"
        st.markdown("""
        **Data Cleaning**:
        - Identified and handled missing values to ensure dataset completeness.
        - Removed outliers and anomalies to enhance data quality.
        - Ensured data consistency and integrity across all features.
        """)

        st.image(
            [
                Image.open(img_path / "head_of_dataframe.png"),
                Image.open(img_path / "df_describe.png"),
            ],
            caption=[
                "Head of dataframe",
                "Dataframe describe",
            ],
            width=700,
        )
        st.markdown("""**Feature Engineering**:
        - Created new features from existing data to capture additional patterns.
        - Selected important features using model-based methods for better performance.
        - Generated additional features that provided significant predictive power.
        """)

        st.image(
            [
                Image.open(img_path / "add_new_features.png"),
                Image.open(img_path / "preproccessed_dataframe.png"),
            ],
            caption=[
                "Feature engineering",
                "preproccessed dataframe",
            ],
            width=700,
        )
    with tabs[2]:
        st.header("Exploratory Data Analysis (EDA)")
        st.markdown("""
        Conducted thorough EDA to uncover insights, visualize distributions, and identify correlations within the dataset.
        - Visualized data distributions to understand feature characteristics.
        - Identified and analyzed correlations between different features.
        - Used various plotting techniques (e.g., histograms, scatter plots) to gain insights.
        """)

        st.image(
            [
                Image.open(img_path / "plot_1.png"),
                Image.open(img_path / "plot_2.png"),
                Image.open(img_path / "plot_3.png"),
                Image.open(img_path / "plot_4.png"),
            ],
            caption=[
                "Data distribution",
                "Data distribution",
                "Data distribution",
                "Data distribution",
            ],
            width=1200,
        )

    with tabs[3]:
        st.header("Machine Learning Pipelines")
        st.markdown("""
        Developed robust training and prediction pipelines using `scikit-learn`.
        - Built scalable and reusable pipelines for data preprocessing and model training.
        - Implemented model selection and hyperparameter tuning to identify the best-performing models.
        - Combined predictions from multiple models (ensemble learning) to improve accuracy and reliability.
        """)

    with tabs[4]:
        st.header("API & Frontend")
        st.markdown("""
        **API Development**:
        - Utilized **FastAPI** to create a backend for handling API calls.
        - Deployed the backend using **Uvicorn**, ensuring high-performance asynchronous capabilities.

        **Frontend Development**:
        - Built an interactive frontend using **Streamlit**, enabling users to interact with the model predictions and insights seamlessly.
        - Designed user-friendly interfaces to input data and view prediction results.
        """)

    with tabs[5]:
        st.header("Deployment and Version Control")
        st.markdown("""
        **Deployment**:
        - Containerized the application using **Docker** for consistent and reproducible environments.
        - Implemented reverse proxy with **Nginx** for secure and efficient web traffic management.
        - Deployed the application on **Hugging Face** for easy access and scalability.

        **Version Control**:
        - Leveraged **GitHub** for version control and collaboration.
        - Implemented **GitHub Actions** for continuous integration and deployment (CI/CD) workflows.
        - Ensured automated testing, building, and deployment processes for maintaining code quality and deployment efficiency.
        """)


if __name__ == "__main__":
    main()
