from pyspark.sql import SparkSession
from pyspark.ml.feature import StandardScaler, VectorAssembler

def preprocess_data(spark, input_path, output_path):
    """
    Preprocess data using Synapse Data Engineering.
    """
    # Load data
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    
    # Clean data (e.g., remove missing values)
    df = df.na.drop()
    
    # Normalize data
    assembler = VectorAssembler(inputCols=df.columns[1:], outputCol="features")
    df = assembler.transform(df)
    
    scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
    scaler_model = scaler.fit(df)
    df = scaler_model.transform(df)
    
    # Save cleaned data
    df.write.mode("overwrite").parquet(output_path)
    print(f"Preprocessed data saved to {output_path}.")

# Example usage
spark = SparkSession.builder.appName("GenomicDataPreprocessing").getOrCreate()
preprocess_data(spark, "abfss://genomics-lake@onelake.dfs.fabric.microsoft.com/raw-data/genomic_data.csv", 
                "abfss://genomics-lake@onelake.dfs.fabric.microsoft.com/cleaned-data/")