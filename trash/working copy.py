import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset from Excel
data = pd.read_excel("your_dataset.xlsx")

# Convert 'Freshness' column to have values of 0 for 'Fresh' and 1 for 'Not Fresh'
data['Freshness'] = data['Freshness'].replace({'Fresh': 0, 'Not Fresh': 1})

# Split data into features and target variable
X = data.drop(columns=['Freshness'])
y = data['Freshness']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the logistic regression model
model = LogisticRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the trained model to disk
joblib.dump(model, 'logistic_regression_model.pkl')

# Now, let's predict the freshness of a new data point
new_data = [[0.15, 0.08, 6.7, 48]]

# Load the saved model from disk
loaded_model = joblib.load('logistic_regression_model.pkl')

# Make prediction using the loaded model
prediction = loaded_model.predict(new_data)

# Print the prediction
if prediction[0] == 0:
    print("Prediction for the input data: Fresh")
else:
    print("Prediction for the input data: Not Fresh")

# Get feature names
feature_names = X.columns

# Get the coefficients (weights) of the model
coefficients = model.coef_[0]

# Plot the coefficients
plt.figure(figsize=(10, 6))
plt.barh(feature_names, coefficients)
plt.xlabel('Coefficient Value')
plt.ylabel('Feature')
plt.title('Coefficients for separating Fresh and Not Fresh')
plt.show()
