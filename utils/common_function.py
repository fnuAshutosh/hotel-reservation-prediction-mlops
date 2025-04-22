import os 
import pandas
from src.logger import getlogger
from src.custom_exception import CustomException
import yaml
import pandas as pd



logger  = getlogger(__name__)


def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info(f"YAML file {file_path} loaded successfully.: {config}")
            return config
    except yaml.YAMLError as e:
        logger.error(f"Error reading YAML file {file_path}: {e}")
        raise CustomException(f"Failed to read YAML file {file_path}: {e}") 

def load_data(path):
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} not found.")
        data = pandas.read_csv(path)
        logger.info(f"Data loaded successfully from {path}.")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {path}: {e}")
        raise CustomException(f"Failed to load data from {path}: {e}")
    

