from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_model(y_true, y_pred, y_pred_proba):
    """
    Evaluate the model using accuracy, AUC-ROC, and confusion matrix.
    """
    # Calculate accuracy
    accuracy = accuracy_score(y_true, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    
    # Calculate AUC-ROC
    auc_score = roc_auc_score(y_true, y_pred_proba)
    print(f"AUC-ROC Score: {auc_score:.2f}")
    
    # Plot confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.show()

# Example usage
# y_true = [0, 1, 0, 1, 0, 1]
# y_pred = [0, 1, 0, 0, 0, 1]
# y_pred_proba = [0.1, 0.9, 0.2, 0.3, 0.1, 0.8]
# evaluate_model(y_true, y_pred, y_pred_proba)