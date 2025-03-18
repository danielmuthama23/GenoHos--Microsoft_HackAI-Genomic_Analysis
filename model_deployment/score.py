import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def init():
    """
    Load the trained model.
    """
    global model
    model = joblib.load("model.pkl")

def run(raw_data):
    """
    Process incoming requests and return predictions.
    """
    # Parse input data
    data = json.loads(raw_data)["data"]
    input_df = pd.DataFrame(data)
    
    # Make predictions
    predictions = model.predict(input_df)
    
    # Return predictions as JSON
    return json.dumps({"predictions": predictions.tolist()})

# Example usage (for testing locally)
if __name__ == "__main__":
    init()
    test_data = json.dumps({"data": [[0.1, 0.2, 0.3, 0.4, 0.5]]})
    print(run(test_data))