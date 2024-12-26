# Importing the required libraries
from metaflow import FlowSpec, step
from data_ingestion import ingest_data
from data_preprocessing import preprocess_data
from model_training import train_data

# Creating a class the execute the flow
class MLPipelineFlow(FlowSpec):

    # Creating the data ingestion step
    @step
    def start(self):

        # Executing the data ingestion script
        ingest_data()

        # Defining the subsequent step
        self.next(self.preprocess)

    # Creating the data preprocessing step
    @step
    def preprocess(self):

        # Executing the data preprocessing script
        preprocess_data()

        # Defining the subsequent step
        self.next(self.train_model)

    # Creating the model training step
    @step
    def train_model(self):

        # Executing the model training script
        train_data()

        # Defining the subsequent step
        self.next(self.end)

    # Creating the last step
    @step
    def end(self):

        # Displaying to the user
        print("\nThe ML Pipeline has been successfully executed!!\n")

# Defining the code to be executed
if __name__ == '__main__':

    # Running the flow
    MLPipelineFlow()