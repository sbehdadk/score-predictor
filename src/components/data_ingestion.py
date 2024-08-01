import sys
from pathlib import Path
import pandas as pd

import env

from app.logger import logging
from app.exception import CustomizedException
from app.components.data_transformation import (
    DataTransformer,
    DataTransformerConfig,
)
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from app.components.model_trainer import Model


@dataclass
class DataIngestionConfig:
    artifacts_path: Path = Path("src/components/artifacts/")
    train_data_path: Path = Path("src/components/artifacts/") / "train_data.csv"
    test_data_path: Path = Path("src/components/artifacts/") / "test_data.csv"
    raw_data_path: Path = Path("src/components/artifacts/") / "raw_data.csv"


class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_ingestion_config.artifacts_path.mkdir(
            parents=True, exist_ok=True
        )
        logging.info("data ingestion initialized...")

    def data_ingesting(self, file_name: str):
        logging.info("data ingestor starting...")
        try:
            stud_df = pd.read_csv(file_name)

            stud_df.to_csv(
                self.data_ingestion_config.raw_data_path,
                index=False,
                header=True,
            )
            logging.info("raw data saved")

            train_set, test_set = train_test_split(
                stud_df,
                test_size=0.2,
                random_state=42,
            )

            train_set.to_csv(
                self.data_ingestion_config.train_data_path,
                index=False,
                header=True,
            )

            test_set.to_csv(
                self.data_ingestion_config.test_data_path,
                index=False,
                header=True,
            )
            logging.info("data ingestion completed successfully...")
            return (
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path,
                self.data_ingestion_config.raw_data_path,
            )
        except Exception as e:
            logging.error(f"Error occurred during data ingestion: {e}")
            raise CustomizedException(e, sys)


def main():
    data_ingestion = DataIngestion()
    train_data_path, test_data_path, raw_data_path = (
        data_ingestion.data_ingesting("src/data/stud.csv")
    )

    data_transformer = DataTransformer(
        train_data_path=train_data_path, test_data_path=test_data_path
    )

    train_arr, test_arr, _ = data_transformer.initialize_data_transformer(
        train_path=train_data_path, test_path=test_data_path
    )

    model = Model()
    r2_score = model.initial_trainer(train_array=train_arr, test_array=test_arr)
    print(r2_score)


if __name__ == "__main__":
    main()
