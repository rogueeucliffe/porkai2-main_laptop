import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import sensor_read  # Import the sensor_read module

# Load the dataset from the Excel file
data = pd.read_excel("your_dataset.xlsx")

# Explicitly set feature names including 'Temperature'
feature_names = ['Ammonia', 'Methane', 'pH_level', 'Lightness_L', 'Temperature']

# Rename columns to match the specified feature names and add the 'Freshness' column
data.columns = feature_names + ['Freshness']

# Split data into features (X) and target variable (y)
X = data.drop(columns=['Freshness'])  # Features (independent variables)
y = data['Freshness']  # Target variable (dependent variable)

# Initialize the logistic regression model
model = LogisticRegression()

# Train the model
model.fit(X, y)

# Make predictions on the test set
y_pred = model.predict(X)

# Calculate accuracy on the training data
accuracy = accuracy_score(y, y_pred)
print("Accuracy on training data:", accuracy)

# Save the trained model to disk
joblib.dump(model, 'logistic_regression_model.pkl')

# Now, let's predict the freshness using sensor data
sensor_data = sensor_read.read_sensor_values()  # Read sensor data
print("Sensor Data:", sensor_data)

# Reshape sensor_data to match the format of X (2D array)
sensor_data = [sensor_data]  # Wrap sensor data in a list

# Load the saved model from disk
loaded_model = joblib.load('logistic_regression_model.pkl')

# Make prediction using the loaded model
prediction = loaded_model.predict(sensor_data)

# Print the prediction
print("Prediction for the sensor data:", prediction)
