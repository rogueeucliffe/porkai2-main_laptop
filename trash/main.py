import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset from the Excel file
data = pd.read_excel("your_dataset.xlsx")

# Explicitly set feature names including 'Temperature'
feature_names = ['Ammonia', 'Methane', 'pH_level', 'Lightness_L', 'Temperature']

# Rename columns to match the specified feature names and add the 'Freshness' column
data.columns = feature_names + ['Freshness']

# Split data into features (X) and target variable (y)
X = data.drop(columns=['Freshness'])  # Features (independent variables)
y = data['Freshness']  # Target variable (dependent variable)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the logistic regression model
model = LogisticRegression()

# Train the model with explicit feature names
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the trained model to disk
joblib.dump(model, 'logistic_regression_model.pkl')

# Now, let's predict the freshness of a new data point
new_data = [[0.25, 0.133, 6.5, 42, 23]]

# Load the saved model from disk
loaded_model = joblib.load('logistic_regression_model.pkl')

# Make prediction using the loaded model
prediction = loaded_model.predict(new_data)

# Print the prediction
print("Prediction for the input data:", prediction)
