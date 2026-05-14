import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def train_and_evaluate_model():
    print("--- Starting AI Model Training ---")
    
    # 1. Load Data
    filepath = 'data/simulated_network_traffic.csv'
    if not os.path.exists(filepath):
        print(f"Error: Data file {filepath} not found. Please run dataset_generator.py first.")
        return
        
    data = pd.read_csv(filepath)
    print(f"Data Loaded Successfully. Shape: {data.shape}")
    
    # 2. Preprocessing & Feature Engineering
    X = data.drop("attack_label", axis=1)
    y = data["attack_label"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")
    
    # 3. Model Training (Random Forest)
    print("\nTraining Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Training Complete!")
    
    # 4. Evaluation
    print("\n--- Model Evaluation ---")
    y_pred = model.predict(X_test)
    
    # Calculate Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"Accuracy:  {acc * 100:.2f}%")
    print(f"Precision: {prec * 100:.2f}%")
    print(f"Recall:    {rec * 100:.2f}%")
    print(f"F1 Score:  {f1 * 100:.2f}%")
    
    # 5. Save the Model
    os.makedirs('models', exist_ok=True)
    model_path = 'models/cybersecurity_rf_model.pkl'
    joblib.dump(model, model_path)
    print(f"\nModel saved successfully to '{model_path}'")
    
    # 6. Visualization (Confusion Matrix & Feature Importance)
    print("\nGenerating Visualizations...")
    os.makedirs('images', exist_ok=True)
    
    # Confusion Matrix Plot
    plt.figure(figsize=(6,5))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Normal', 'Threat'], 
                yticklabels=['Normal', 'Threat'])
    plt.title('Threat Detection Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.savefig('images/confusion_matrix.png', bbox_inches='tight')
    print("Saved 'images/confusion_matrix.png'")
    
    # Feature Importance Plot
    plt.figure(figsize=(8,4))
    importances = model.feature_importances_
    features = X.columns
    sns.barplot(x=importances, y=features, palette='viridis', hue=features, legend=False)
    plt.title('Feature Importance for Threat Detection')
    plt.xlabel('Importance Score')
    plt.savefig('images/feature_importance.png', bbox_inches='tight')
    print("Saved 'images/feature_importance.png'")
    
    print("\n--- Process Completed Successfully ---")

if __name__ == "__main__":
    train_and_evaluate_model()
