from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt

def perform_pca(data_path, n_components=2):
    """
    Perform PCA on the dataset and visualize the results.
    """
    # Load data
    df = pd.read_csv(data_path)
    
    # Separate features and target
    X = df.drop(columns=["Recovery_Status"])
    y = df["Recovery_Status"]
    
    # Perform PCA
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)
    
    # Visualize PCA results
    plt.figure(figsize=(8, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap="viridis")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA of Genomic Data")
    plt.colorbar(label="Recovery Status")
    plt.show()
    
    return X_pca

# Example usage
perform_pca("data_ingestion/sample_data/genomic_data.csv")