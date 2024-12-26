# Importing the required libraries
import pandas as pd
import matplotlib.pyplot as plt
import os
import yaml
import psycopg2
import pickle

from sqlalchemy import create_engine
from urllib.parse import quote

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

# Creating a function to preprocess data
def preprocess_data():

    # Accessing the params.yaml file
    params = yaml.safe_load(open("params.yaml"))['preprocess']

    # Importing the required configurations for the database
    from config import user, psswd, database, host, port

    # URL-encoding the password to encode the "@"
    encoded_password = quote(psswd)

    # Creating databsase engine
    engine = create_engine(f'postgresql+psycopg2://{user}:{encoded_password}@{host}:{port}/{database}')

    # Defining the select query
    select_query = "SELECT * FROM train_df"

    # Executing the query
    train_data = pd.read_sql(select_query, engine)

    # Describing the data
    train_data.describe()

    # Dropping null values
    train_data = train_data.dropna()

    # Dropping the duplicate values
    train_data = train_data.drop_duplicates()

    # Retriving the columns of the data
    cols = train_data.columns

    # Creating a boxplot for id
    train_data[[cols[0]]].boxplot()

    # Creating a boxplot for Age
    train_data[[cols[1]]].boxplot()

    # Creating a boxplot for Income
    train_data[[cols[2]]].boxplot()

    # Creating a boxplot for Employee Length (employee length greater than 120 is a very big outlier that needs to be removed)
    train_data[[cols[4]]].boxplot()

    # Creating a boxplot for Credit History Length
    train_data[[cols[6]]].boxplot()

    # Creating a boxplot for Loan Amount
    train_data[[cols[9]]].boxplot()

    # Creating a boxplot for Loan Interest Rate
    train_data[[cols[10]]].boxplot()

    # Creating a boxplot for Loan Percent Income
    train_data[[cols[11]]].boxplot()

    # Removing the outliers from the data
    cleaned_train_data = train_data[train_data.person_emp_length < 70]

    # Dropping the id column as it won't contribute to the predictions
    cleaned_train_data = cleaned_train_data.drop("id", axis=1)

    # Splitting the data into features and labels
    cleaned_train_labels = cleaned_train_data["loan_status"]
    cleaned_train_data = cleaned_train_data.drop("loan_status", axis=1)

    # Retrieivng the columns of the cleaned data
    cols = cleaned_train_data.columns

    # Retrieving categorical features
    categorical_features = [col for col in cols if cleaned_train_data[col].dtype.name == 'object']

    # Retrieving numerical features
    numerical_features = [col for col in cols if cleaned_train_data[col].dtype.name != 'object']

    # Creating a column transformer
    transformer = ColumnTransformer(
        [('numerical_transformer', MinMaxScaler(feature_range=(0,1)), numerical_features),
        ('categorical_transformer', OneHotEncoder(handle_unknown='ignore'), categorical_features)]
    )

    # Preprocessing the data
    preprocessed_data = pd.DataFrame(transformer.fit_transform(cleaned_train_data))

    # Creating directories to save the preprocessed data and the transformer
    os.makedirs("data/preprocess", exist_ok=True)
    os.makedirs("transformers", exist_ok=True)

    # Saving the preprocessed data an d labels as a csv file
    preprocessed_data.to_csv(params['output_data_path'], index=False)
    cleaned_train_labels.to_csv(params['output_label_path'], index=False)

    # Saving the column transformer as a pickle file
    pickle.dump(transformer, open(params['transformer_path'], 'wb'))

    # Displaying a success message
    print("\nThe data has been successfully preprocessed!")

    # Returning nothing
    return

# Defining the code to be executed
if __name__ == '__main__':

    # Calling the function to preprocess the data
    preprocess_data()