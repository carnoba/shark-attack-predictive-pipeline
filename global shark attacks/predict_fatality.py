import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

def train_model(db_name):
    conn = sqlite3.connect(db_name)
    df = pd.read_sql('SELECT * FROM sharks', conn)
    conn.close()
    
    # Select features: Activity and Month
    # We need to filter out 'Unknown' or 0 months if they are too many, 
    # but for precision let's use what we have.
    
    data = df[['Activity', 'Month', 'is_fatal']].dropna()
    
    # Encode categorical Activity
    le = LabelEncoder()
    data['Activity_Encoded'] = le.fit_transform(data['Activity'].astype(str))
    
    X = data[['Activity_Encoded', 'Month']]
    y = data['is_fatal']
    
    # Split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Training Random Forest Classifier...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Predict
    y_pred = rf.predict(X_test)
    
    report = classification_report(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    
    print("\nModel Evaluation:")
    print(f"Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(report)
    
    # Save results to file
    with open('model_results.txt', 'w') as f:
        f.write(f"Accuracy: {acc:.4f}\n")
        f.write("\nClassification Report:\n")
        f.write(report)
    
    # Save model
    joblib.dump(rf, 'fatality_predictor.pkl')
    joblib.dump(le, 'activity_encoder.pkl')
    print("Model and encoder saved and results written to model_results.txt.")


if __name__ == "__main__":
    try:
        train_model('master_sharks.db')
    except Exception as e:
        print(f"Modeling failed: {e}")
