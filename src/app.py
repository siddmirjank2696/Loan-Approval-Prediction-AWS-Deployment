# Importing the required libraries
import numpy as np
import pandas as pd
import yaml
import pickle
from flask import Flask, render_template, request

# Accessing the params.yaml file
params = yaml.safe_load(open("params.yaml", "rb"))['app']

# Creating an instance of the flask class
app = Flask(__name__)

# Creating a function to predict loan status
def predict_loan_status(s):

    # Defining an empty string for prediction text
    prediction_text = ""

    # Loading the transformer
    transformer = pickle.load((open(params['transformer_path'], 'rb')))

    # Loading the model
    model = pickle.load(open(params['model_path'], 'rb'))

    # Loading the sample inputs
    sample = pd.read_csv(params['sample_path'])

    # Splitting the string by a comma
    data = s.split(",")

    # Reshaping the data
    data = np.array(data).reshape(1, len(data))

    # Converting the data into a pandas dataframe
    df = pd.DataFrame(data, columns=sample.columns)

    # Transforming the data for model predictions
    test_input = transformer.transform(df)

    # Predicting the loan status
    prediction = model.predict(test_input)

    # Checking whether the prediction is 0
    if prediction[0] == 0:
        prediction_text = "The loan will not be approved"
    else:
        prediction_text = "The loan will be approved"

    # Returning the prediction text
    return prediction_text


# Creating a route for the homepage
@app.route('/')
def home():

    # Returning the homepage template
    return render_template("home_page.html")

# Creating a route for the prediction page
@app.route("/predict")
def predict():

    # Retrieivng the user inputs
    inputs = request.args.get('data')

    # Predicting the loan status
    prediction_text = predict_loan_status(inputs)

    # Returning the prediction page template
    return render_template("prediction_page.html", prediction_text=prediction_text)

# Defining the code to be executed
if __name__ == '__main__':

    # Running the application
    app.run(debug=True, host=params['host'], port=params['port'])