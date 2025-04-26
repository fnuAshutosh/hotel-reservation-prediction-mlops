import os 
import sys
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import getlogger
from src.custom_exception import CustomException
from config.paths_configs import *
from ..utils.common_function import read_yaml


logger = getlogger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = config["bucket_name"]
        self.file_name = config["bucket_file_name"]
        self.train_test_ratio = config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data Ingestion initialized with {self.bucket_name} and {self.file_name}")


    def download_csv_from_gcp(self):
        """
        Download the CSV file from GCP bucket and save it to the local directory.
        """
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"File {self.file_name} downloaded from GCP bucket {self.bucket_name} to {RAW_FILE_PATH}.")
        except Exception as e:
            logger.error(f"Error downloading file from GCP: {e}")
            raise CustomException("Failed to download file from GCP", e)
        

    def split_data(self):
        try:
            logger.info("Splitting data into train and test sets.")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size=1-self.train_test_ratio, random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"Train and test data saved to {TRAIN_FILE_PATH} and {TEST_FILE_PATH}.")
        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            raise CustomException("Failed to split data", e)


    def run(self):
        """
        Run the data ingestion pipeline.
        """
        try:
            logger.info("Starting data ingestion process.")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data ingestion completed successfully.")
        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")

        finally:
            logger.info("Data ingestion process finished.")



if __name__ == "__main__":
    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()