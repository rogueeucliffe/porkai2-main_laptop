import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from sklearn.linear_model import LogisticRegression
import joblib

class FreshnessPredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Freshness Prediction Dashboard")

        # Load the trained model
        self.model = joblib.load('logistic_regression_model.pkl')

        # Create input fields
        self.ammonia_label = ttk.Label(root, text="Ammonia:")
        self.ammonia_label.grid(row=0, column=0, padx=5, pady=5)
        self.ammonia_entry = ttk.Entry(root)
        self.ammonia_entry.grid(row=0, column=1, padx=5, pady=5)

        self.methane_label = ttk.Label(root, text="Methane:")
        self.methane_label.grid(row=1, column=0, padx=5, pady=5)
        self.methane_entry = ttk.Entry(root)
        self.methane_entry.grid(row=1, column=1, padx=5, pady=5)

        self.ph_label = ttk.Label(root, text="pH Level:")
        self.ph_label.grid(row=2, column=0, padx=5, pady=5)
        self.ph_entry = ttk.Entry(root)
        self.ph_entry.grid(row=2, column=1, padx=5, pady=5)

        self.lightness_label = ttk.Label(root, text="Lightness:")
        self.lightness_label.grid(row=3, column=0, padx=5, pady=5)
        self.lightness_entry = ttk.Entry(root)
        self.lightness_entry.grid(row=3, column=1, padx=5, pady=5)

        self.temperature_label = ttk.Label(root, text="Temperature:")
        self.temperature_label.grid(row=4, column=0, padx=5, pady=5)
        self.temperature_entry = ttk.Entry(root)
        self.temperature_entry.grid(row=4, column=1, padx=5, pady=5)

        # Create predict button
        self.predict_button = ttk.Button(root, text="Predict", command=self.predict_freshness)
        self.predict_button.grid(row=5, columnspan=2, padx=5, pady=5)

        # Create output label
        self.output_label = ttk.Label(root, text="")
        self.output_label.grid(row=6, columnspan=2, padx=5, pady=5)

        # Add frame with image
        self.frame_with_image = tk.Frame(root, width=200, height=100, bg="red")
        self.frame_with_image.grid(row=0, column=2, rowspan=7, padx=10, pady=10)
        self.add_image_to_frame("test.jpg")

    def add_image_to_frame(self, image_path):
        image = Image.open(image_path)
        image = image.resize((200, 100))
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(self.frame_with_image, image=photo)
        label.image = photo
        label.pack()

    def predict_freshness(self):
        # Get input values
        ammonia = float(self.ammonia_entry.get())
        methane = float(self.methane_entry.get())
        ph_level = float(self.ph_entry.get())
        lightness = float(self.lightness_entry.get())
        temperature = float(self.temperature_entry.get())

        # Make prediction
        prediction = self.model.predict([[ammonia, methane, ph_level, lightness, temperature]])

        # Display prediction
        self.output_label.config(text=f"Predicted Freshness: {prediction[0]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FreshnessPredictionApp(root)
    root.mainloop()
