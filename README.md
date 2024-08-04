---
title: score-predictor
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
python_version: 3.9
app_file: app/main.py
app_port: 7860
fullWidth: true
header: default
short_description: predicts the student scores.
tags:
  - machine-learning
  - fastapi
  - streamlit
  - docker
thumbnail: https://example.com/thumbnail.png
pinned: true
---

# score-predictor

This project combines FastAPI and Streamlit to create a machine learning application that is deployed on Hugging Face Spaces. The application includes an API for making predictions and a web interface for interacting with the model.

## Project Structure

```plaintext
my-ml-app/
├── app/
│   ├── main.py
│   ├── requirements.txt
│   ├── templates/
│   │   ├── index.html
│   │   ├── home.html
├── streamlit_app.py
├── Dockerfile
