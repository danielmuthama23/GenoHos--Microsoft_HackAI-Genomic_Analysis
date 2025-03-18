from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_model(data_path):
    """
    Train a Random Forest model using Synapse Data Science.
    """
    # Load data
    df = spark.read.parquet(data_path)
    
    # Prepare features and target
    X = df.select("scaled_features").rdd.map(lambda row: row[0]).collect()
    y = df.select("Recovery_Status").rdd.map(lambda row: row[0]).collect()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")
    
    return model

# Example usage
model = train_model("abfss://genomics-lake@onelake.dfs.fabric.microsoft.com/cleaned-data/")