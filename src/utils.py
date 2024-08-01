import pickle

import sys
import numpy as np
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV
from src.exception import CustomizedException
from src.logger import logging


def save_to_pickle_object(file_path: Path, object: ColumnTransformer):
    try:
        file_path.parent.mkdir(exist_ok=True)
        with open(file_path, "wb") as file_object:
            pickle.dump(object, file_object)
        logging.info(f"Pickle object saved to {file_path}")
    except Exception as e:
        raise CustomizedException(e, sys)


def load_object(file_path: Path):
    try:
        with open(file_path, "rb") as file_object:
            logging.info("Loading object")
            return pickle.load(file_object)

    except Exception as e:
        raise CustomizedException(e, sys)


def evaluate_models(
    X_train: np, X_test: np, y_train: np, y_test: np, models: list, params: dict
) -> dict:
    try:
        report = {}
        for key, model in models.items():
            param = params[key]
            grid_search = GridSearchCV(model, param, cv=3)
            grid_search.fit(X_train, y_train)

            model.set_params(**grid_search.best_params_)

            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model] = test_model_score
        return report

    except Exception as e:
        raise CustomizedException(e, sys)
