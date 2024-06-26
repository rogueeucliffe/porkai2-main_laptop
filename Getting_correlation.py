import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset from Excel
data = pd.read_excel("your_dataset.xlsx")

# Convert 'Freshness' column to have values of 0 for 'Fresh' and 1 for 'Not Fresh'
data["Freshness"] = data["Freshness"].replace({"Fresh": 0, "Not Fresh": 1})

# Split data into features and target variable
X = data.drop(columns=["Freshness"])
y = data["Freshness"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

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
joblib.dump(model, "logistic_regression_model_new.pkl")


# Get feature names
feature_names = X.columns

# Get the coefficients (weights) of the model
coefficients = model.coef_[0]

# Print the coefficients along with their corresponding feature names
print("Coefficients for separating Fresh and Not Fresh:")
for feature, coef in zip(feature_names, coefficients):
    print(f"{feature}: {coef}")
