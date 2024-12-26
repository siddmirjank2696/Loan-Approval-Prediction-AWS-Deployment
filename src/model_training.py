# Importing the required libraries
import pandas as pd
import yaml
import pickle
import os

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier

import mlflow
from mlflow.models import infer_signature

import warnings

# Filtering out warnings
warnings.filterwarnings("ignore")


# Creating a function to train the data
def train_data():
    
    # Accessing the params.yaml file
    params = yaml.safe_load(open('params.yaml'))['train']

    # Importing the data and labels
    X = pd.read_csv(params['input_data_path']).values
    y = pd.read_csv(params['input_label_path']).values.ravel()

    # Splitting the data into train and test
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Setting mlflow configuration with dagshub
    os.environ['MLFLOW_TRACKING_URI']="https://dagshub.com/siddmirjank2696/Diabetes-Detection-MLflow.mlflow"
    os.environ['MLFLOW_TRACKING_USERNAME']="siddmirjank2696"
    os.environ["MLFLOW_TRACKING_PASSWORD"]="ed2891a2b1abb4d15f5d9a6a45f8bb11829b6bed"

    # Setting the mlflow tracking uri
    mlflow.set_tracking_uri("https://dagshub.com/siddmirjank2696/Loan-Approval-Prediction-AWS-Deployment.mlflow")

    # Setting the experiment name
    mlflow.set_experiment("XgBoost Tracking")

    # Starting an mlflow run
    with mlflow.start_run():

        # Creating an xgboost object
        xgb = XGBClassifier()

        # Fititng the data to the model
        xgb.fit(X_train, y_train)

        # Performing predictions on the validation data
        y_pred = xgb.predict(X_val)

        # Calculating the accuracy
        accuracy = accuracy_score(y_val, y_pred)

        # Logging the accuracy
        mlflow.log_metric("accuracy", accuracy)

        # Inferring the model signature
        signature = infer_signature(X_train, y_train)

        # Defining the model information
        model_info = mlflow.xgboost.log_model(
            xgb_model = xgb,
            artifact_path = "models/xgboost-model",
            signature = signature
        )

    # Loading the test data
    person_test_data = pd.read_csv(params['person_data_path'])
    loan_test_data = pd.read_csv(params['loan_data_path'])

    # Merging the test data to form one csv file
    predictions = pd.merge(person_test_data, loan_test_data, how="inner", on="id")

    # Dropping id from the test data because it does not contribute to the prediction
    test_data = predictions.drop("id", axis=1)

    # Loading the transformer
    transformer = pickle.load(open(params['transformer_path'], 'rb'))

    # Transforming the test data into the same format as the train data
    X_test = transformer.transform(test_data)

    # Predicting the loan status on the test data
    y_test = xgb.predict(X_test)

    # Adding the predictions to the csv file
    predictions["loan_status"] = y_test

    # Creating a directory to save the predictions and the model
    os.makedirs("data/predictions", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    # Saving the predictions as a csv file
    predictions.to_csv(params['output_path'], index=False)

    # Saving the model as a pickle file
    pickle.dump(xgb, open(params['model_path'], 'wb'))

    # Displaying the success message
    print("\nThe model and predictions were saved successfully!\n")

    # Returning nothing
    return

# Defining the code to be executed
if __name__ == '__main__':

    # Calling the function to train the model
    train_data()