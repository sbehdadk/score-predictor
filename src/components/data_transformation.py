# EDA : Exploratory data analysis
import sys
from pathlib import Path
import pandas as pd
from pandas import DataFrame
from dataclasses import dataclass
import numpy as np
from sklearn.compose import (
    ColumnTransformer,
)  # use for pipeline (onehotending etc...)
from sklearn.impute import SimpleImputer  # handle non-value
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src.exception import CustomizedException
from src.logger import logging
from src.utils import save_to_pickle_object


@dataclass
class DataTransformerConfig:
    artifact_path: Path = Path(__file__).parent / "artifacts/"
    preprocessed_model_file_path: Path = Path.joinpath(
        artifact_path, "preprocessed_model.pkl"
    )


class DataTransformer:
    """
    This class is responsible for transforming raw data into a preprocessed state.
    """

    def __init__(self, train_data_path, test_data_path):
        self.data_transformer_config = DataTransformerConfig()
        logging.info("data transformer initialized...")
        self.train_data_path = train_data_path
        self.test_data_path = test_data_path
        self.target_col = "math_score"

    @staticmethod
    def get_numerical_cols(data_frame: DataFrame):
        return list(
            filter(
                lambda x: data_frame[x].dtype != "O" and x != "math_score",
                data_frame.columns,
            )
        )

    @staticmethod
    def get_categorical_cols(data_frame: DataFrame):
        return list(filter(lambda x: data_frame[x].dtype == "O", data_frame.columns))

    def get_feature_data_frame(self, data_frame: DataFrame):
        return data_frame.drop(columns=[self.target_col], axis=1)

    def get_target_data_frame(self, data_frame: DataFrame):
        return data_frame[self.target_col]

    def get_data_transformer(self):
        """
        This function returns the types of features in the dataset.

        Raises:
            - `CustomizedException`: _description_

        Returns:
            - `_type_`: _description_
        """
        train_df = pd.read_csv(
            self.train_data_path,
        )

        numerical_cols = self.get_numerical_cols(train_df)
        categorical_cols = self.get_categorical_cols(train_df)
        try:
            numerical_pipeline = Pipeline(
                steps=[
                    (
                        "imputer",
                        SimpleImputer(strategy="median"),
                    ),  # handling missing values
                    ("scaler", StandardScaler()),
                ]
            )
            categorical_pipeline = Pipeline(
                steps=[
                    (
                        "imputer",
                        SimpleImputer(strategy="most_frequent"),
                    ),  # handling missing values
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )

            logging.info(
                "standard scaling for numerical & encoding the categorical columns successfully done."
            )
            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", numerical_pipeline, numerical_cols),
                    (
                        "categorical_pipeline",
                        categorical_pipeline,
                        categorical_cols,
                    ),
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomizedException(e, sys)

    def initialize_data_transformer(self, train_path, test_path):
        """
        This function initializes the data transformer.

        Args:
            train_path (Path): _description_
            test_path (Path): _description_

        Raises:
            - `CustomizedException`: _description_
        """
        try:
            preprocessor = self.get_data_transformer()
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            input_train_data_frame = self.get_feature_data_frame(train_df)
            target_train_data_frame = self.get_target_data_frame(train_df)

            input_test_data_frame = self.get_feature_data_frame(test_df)
            target_test_data_frame = self.get_target_data_frame(test_df)

            logging.info("data transformation started...")
            train_data_array = preprocessor.fit_transform(input_train_data_frame)
            test_data_array = preprocessor.transform(input_test_data_frame)

            train_array = np.c_[train_data_array, np.array(target_train_data_frame)]
            test_array = np.c_[test_data_array, np.array(target_test_data_frame)]

            logging.info("data transformation completed successfully...")
            save_to_pickle_object(
                file_path=self.data_transformer_config.preprocessed_model_file_path,
                object=preprocessor,
            )
            return (
                train_array,
                test_array,
                self.data_transformer_config.preprocessed_model_file_path,
            )
        except Exception as e:
            raise CustomizedException(e, sys)
