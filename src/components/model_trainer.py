import sys
from pathlib import Path
from dataclasses import dataclass
import numpy as np
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    AdaBoostRegressor,
    GradientBoostingRegressor,
)
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from xgboost import XGBRegressor

from app.exception import CustomizedException
from app.logger import logging
from app.utils import save_to_pickle_object, evaluate_models


@dataclass
class ModelConfig:
    artifact_path: Path = Path(__file__).parent / "artifacts/"
    model_file_path: Path = artifact_path / "model.pkl"


class Model:
    def __init__(self) -> None:
        self.model_config = ModelConfig()

    def initial_trainer(
        self, train_array: np, test_array: np, preprocessor_path: Path = None
    ):
        try:
            logging.info("importing train & test arrays...")
            X_train, y_train, X_test, y_test = (
                train_array[
                    :, :-1
                ],  # alternatively np.split(train_array, [train_array.shape[1] - 1], axis=1)
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            params = {
                "K-Neighbors Regressor": {
                    "n_neighbors": [5, 7, 9, 11, 13, 15],
                    "weights": ["uniform", "distance"],
                    "metric": ["minkowski", "euclidean", "manhattan"],
                },
                "Decision Tree": {
                    "criterion": [
                        "squared_error",
                        "friedman_mse",
                        "absolute_error",
                        "poisson",
                    ],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest": {
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'max_features':['sqrt','log2',None],
                    "n_estimators": [8, 16, 32, 64, 128, 256]
                },
                "Gradient Boosting": {
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    "learning_rate": [0.1, 0.01, 0.05, 0.001],
                    "subsample": [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    "learning_rate": [0.1, 0.01, 0.05, 0.001],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "AdaBoost Regressor": {
                    "learning_rate": [0.1, 0.01, 0.5, 0.001],
                    # 'loss':['linear','square','exponential'],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
            }

            model_report: dict = evaluate_models(
                X_train=X_train,
                X_test=X_test,
                y_train=y_train,
                y_test=y_test,
                models=models,
                params=params,
            )

            best_model_instance = max(model_report, key=model_report.get)
            best_model_report = model_report[best_model_instance]

            best_model_name = next(
                name
                for name, instance in models.items()
                if instance == best_model_instance
            )

            best_model = models[best_model_name]
            if best_model_report < 0.6:
                raise CustomizedException("No best model found")

            logging.info("best model found")

            save_to_pickle_object(
                file_path=self.model_config.model_file_path,
                object=best_model,
            )

            predicted_best_model_result = best_model.predict(X_test)
            r2_score_value = r2_score(y_test, predicted_best_model_result)

            return r2_score_value
        except Exception as e:
            raise CustomizedException(e, sys)


if __name__ == "__main__":
    pass
