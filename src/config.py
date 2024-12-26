# Importing the required libraries
import os
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

# Retrieving the database, user and password for the database
database = os.getenv('POSTGRES_DATABASE')
user = os.getenv('POSTGRES_USER')
psswd = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')