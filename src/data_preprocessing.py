import os 
import pandas as pd
import numpy as np 
from src.logger import getlogger
from src.custom_exception import CustomException
from config.paths_configs import *
from utils.common_function import read_yaml, load_data 
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = getlogger(__name__)

class DataPreprocessing:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config_path = config_path
        self.config = read_yaml(self.config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            logger.info(f"Directory {self.processed_dir} created.")
        
    
    def preprocess_data(self, df):
        try:
            logger.info("Starting data preprocessing...")
            logger.info(f"Initial shape of data: {df.columns}")
            # Drop unnecessary columns
            df.drop(columns=['Booking_ID'], inplace=True)
            # Drop duplicates
            df.drop_duplicates()
            
            # categorical columns 
            categorical_cols = self.config["data_processing"]["categorical_features"]
            # numerical columns
            numerical_cols = self.config["data_processing"]["numerical_features"]

            logger.info(f"Applying label encoding on categorical columns: {categorical_cols}")

            label_encoder = LabelEncoder()
            mappings = {}

            # for col in categorical_cols:
            #     df[col] = label_encoder.fit_transform(df[col])
            #     mappings.append({col: dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))})
            
            for col in categorical_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
                


            logger.info(f"Label mapping are :")

            for col,mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            logger.info(f"Applying Skeweness")
            skewness_threshold = self.config["data_processing"]["skewness_threshold"]

            skweness = df[numerical_cols].apply(lambda x: x.skew()).sort_values(ascending=False)
            
            for column in skweness[skweness>skewness_threshold].index:
                df[column] = np.log1p(df[column])
                #logger.info(f"Applied log transformation on {column}")
            
            return df
        
        except Exception as e:
            logger.error(f"Error in data preprocessing step: {e}")
            raise CustomException(f"Error while preprocessing data step:", e)
        
    
    def handle_imbalance(self,df):
        try:
            logger.info("Handling class imbalance using SMOTE...")
            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]
            
            smote = SMOTE(random_state=42)
            X_res, y_res = smote.fit_resample(X, y)
            
            balanced_df = pd.DataFrame(X_res, columns=X.columns)
            balanced_df["booking_status"] = y_res.values

            logger.info(f"Class distribution after SMOTE: {balanced_df['booking_status'].value_counts()}")
            return balanced_df
        
        except Exception as e:
            logger.error(f"Error in handling imbalance: {e}")
            raise CustomException(f"Error while handling imbalance:", e)
    
    def select_feature(self,df):
        try:
            logger.info("Selecting features based on correlation with target variable...")
            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]
            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            # feature_importances = model.feature_importances_
            # feature_importance_df = pd.DataFrame({
            #     'feature': X.columns,
            #     'importance': feature_importances
            # }).sort_values(by='importance', ascending=False)

            # number_of_features_to_select = self.config["data_processing"]["numerical_features"]

            # top_10_features = feature_importance_df['feature'].head(number_of_features_to_select).values 

            feature_importance = model.feature_importances_

            feature_importance_df = pd.DataFrame({
                        'feature':X.columns,
                        'importance':feature_importance
                            })
            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            num_features_to_select = self.config["data_processing"]["no_of_features"]

            top_10_features = top_features_importance_df["feature"].head(num_features_to_select).values


            logger.info(f"Features selected : {top_10_features}")

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Feature slection completed sucesfully")

            return top_10_df

        except Exception as e:
            logger.error(f"Error in feature selection: {e}")
            raise CustomException(f"Error while selecting features:", e)


    def save_processed_data(self,df, file_path):
        try:
            logger.info(f"Saving processed data to {file_path}...")
            df.to_csv(file_path, index=False)
            logger.info(f"Processed data saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving processed data: {e}")
            raise CustomException(f"Error while saving processed data:", e)
        


    def process(self):
        try:
            logger.info("Starting data processing pipeline...")
            # Load train and test data
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.handle_imbalance(train_df)
            test_df = self.handle_imbalance(test_df)
            
            train_df = self.select_feature(train_df)
            test_df = test_df[train_df.columns]  # Ensure test set has the same features as train set

            # Save processed data
            self.save_processed_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_processed_data(test_df, PROCESSED_TEST_DATA_PATH)
            logger.info("Data processing pipeline completed successfully.")
            

        except Exception as e:
            logger.error(f"Error in data processing pipeline: {e}")
            raise CustomException(f"Error in data processing pipeline:", e)

    


if __name__ == "__main__":
    preprocessor = DataPreprocessing(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PROCESSED_DIR,
        config_path=CONFIG_PATH
    )
    # Run the preprocessing pipeline
    preprocessor.process()