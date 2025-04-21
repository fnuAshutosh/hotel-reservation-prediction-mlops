from src.logger import getlogger
from src.custom_exception import CustomException

import sys

logger = getlogger(__name__)

def divide(a, b):
    try:
        return a / b
    except Exception as e:
        logger.error("Division by zero error")
        raise CustomException("Division by zero error", sys) from e
    

if __name__ == "__main__":
    try:
        logger.info("Starting the division operation")
        divide(5, 0)
    except CustomException as e:
        logger.error(str(e))  # This will log the error message with traceback information