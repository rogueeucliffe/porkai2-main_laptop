# main_copy.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import sensor_read

def load_dataset(file_path, feature_names):
    data = pd.read_excel(file_path)
    data.columns = feature_names + ['Freshness']
    X = data.drop(columns=['Freshness'])
    y = data['Freshness']
    return X, y

def train_model(X, y):
    model = LogisticRegression()
    model.fit(X, y)
    return model

def evaluate_model(model, X, y):
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    return accuracy

def save_model(model, file_path):
    joblib.dump(model, file_path)

def load_saved_model(file_path):
    loaded_model = joblib.load(file_path)
    return loaded_model

def predict_freshness(sensor_data, model):
    sensor_data = [sensor_data]
    prediction = model.predict(sensor_data)
    sensor_data_with_prediction = sensor_data[0] + [prediction[0]]
    return sensor_data_with_prediction

def get_sensor_data_with_prediction():
    sensor_data = sensor_read.read_sensor_values()
    loaded_model = load_saved_model('logistic_regression_model.pkl')
    prediction = predict_freshness(sensor_data, loaded_model)
    return prediction,

def main():
    feature_names = ['Ammonia', 'Methane', 'pH_level', 'Lightness_L', 'Temperature']
    X, y = load_dataset("your_dataset.xlsx", feature_names)
    model = train_model(X, y)
    accuracy = evaluate_model(model, X, y)
    print("Accuracy on training data:", accuracy)
    save_model(model, 'logistic_regression_model.pkl')
    sensor_data = sensor_read.read_sensor_values()
    loaded_model = load_saved_model('logistic_regression_model.pkl')
    sensor_data_with_prediction = predict_freshness(sensor_data, loaded_model)
    print("Sensor Data with Prediction:", sensor_data_with_prediction)


if __name__ == "__main__":
    main()
