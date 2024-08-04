import uvicorn

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.pipeline.predict_pipeline import CustomDataSource, PredictPipeline
import streamlit
from fastapi.requests import Request
from fastapi.responses import JSONResponse

app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.middleware("http")
async def handle_hf_health_check(request: Request, call_next):
    if request.url.path == "/" and request.query_params.get("logs") == "container":
        return JSONResponse(content={"message": "Container is running"})
    return await call_next(request)


class PredictionInput(BaseModel):
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    writing_score: int
    reading_score: int


@app.get("/")
async def root(logs: str = None):
    if logs == "container":
        return {"message": "Container is running!!!"}
    return {"message": "Not in the Container"}


# Add a root endpoint
@app.get("/api/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.post("/api/prediction")
async def predict(input_data: PredictionInput):
    data = CustomDataSource(
        gender=input_data.gender,
        race_ethnicity=input_data.race_ethnicity,
        parental_level_of_education=input_data.parental_level_of_education,
        lunch=input_data.lunch,
        test_preparation_course=input_data.test_preparation_course,
        writing_score=input_data.writing_score,
        reading_score=input_data.reading_score,
    )
    predict_df = data.get_data_as_data_frame()
    predict_pipeline = PredictPipeline()
    predicted_score = predict_pipeline.predict(predict_df)
    return {"results": predicted_score[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
