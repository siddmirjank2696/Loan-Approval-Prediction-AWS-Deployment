# Importing the required libraries
import pandas as pd
import os
import psycopg2
import yaml

from sqlalchemy import create_engine
from urllib.parse import quote

# Creating a fuction to perform ingest data
def ingest_data():

    # Accessing the params.yaml file
    params = yaml.safe_load(open("params.yaml"))['ingest']

    # Loading the data files
    person_data = pd.read_csv(params['person_data_path'])
    loan_data = pd.read_csv(params['loan_data_path'])

    # Merging the data to form one csv file
    train_data = pd.merge(person_data, loan_data, how="inner", on="id")

    # Importing the required configurations for the database
    from config import user, psswd, database, host, port

    # URL-encoding the password to encode the "@"
    encoded_password = quote(psswd)

    # Creating databsase engine
    engine = create_engine(f'postgresql+psycopg2://{user}:{encoded_password}@{host}:{port}/{database}')

    # Creating a table name for the database
    table_name = "train_df"

    # Writing the merged dataframe to the database
    train_data.to_sql(table_name, engine, if_exists='replace', index=False)

    # Displaying to the user
    print(f"\nThe training data has been successfully loaded into the {table_name} table!\n")

    # Returning nothing
    return

# Defining the code to be executed
if __name__ == '__main__':

    # Calling the function to ingest the data
    ingest_data()