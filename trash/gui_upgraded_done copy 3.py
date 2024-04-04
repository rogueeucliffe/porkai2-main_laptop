from pathlib import Path
import cv2
from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Button, PhotoImage
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

start_x = 0
start_y = 0

def on_drag(event):
    x = window.winfo_pointerx() - start_x
    y = window.winfo_pointery() - start_y
    window.geometry("+{}+{}".format(x, y))

def on_click(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

window = Tk()

window.geometry("862x519")
window.configure(bg="#FFB700")

window.bind("<B1-Motion>", on_drag)
window.bind("<Button-1>", on_click)

canvas = Canvas(
    window,
    bg="#FFB700",
    height=519,
    width=862,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    431.0000000000001,
    0.0,
    862.0000000000001,
    519.0,
    fill="#FFFFFF",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    646.0000000000001,
    474.0,
    image=image_image_1)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    646.0000000000001,
    474.0,
    image=image_image_2)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    646.0000000000001,
    474.0,
    image=image_image_3)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    730.0000000000001,
    398.0,
    image=image_image_4)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    568.0000000000001,
    398.0,
    image=image_image_5)

canvas.create_rectangle(
    442.0000000000001,
    14.0,
    856.0000000000001,
    295.0,
    fill="#000000",
    outline="")

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    775.0000000000001,
    474.0,
    image=image_image_6)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    216.0000000000001,
    260.0,
    image=image_image_7)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

def start_camera():
    cap = cv2.VideoCapture(0)

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)

            frame = frame.resize((414, 281), Image.LANCZOS)

            frame = ImageTk.PhotoImage(frame)
            canvas.create_image(442.0000000000001, 14.0, anchor="nw", image=frame, tags=("camera_output",))
            canvas.frame = frame
            canvas.after(10, update_frame)
        else:
            cap.release()

    update_frame()

new_text = []


def start():
    canvas.delete("text")
    start_camera()
    start_preheating()
    canvas.after(5000, read_data_and_update_canvas)

def read_data_and_update_canvas():

    canvas.delete(image_1)
    canvas.create_image(
        646.0000000000001,
        474.0,
        image=image_image_2
    )

    # Call the function from main_copy.py
    new_text = get_sensor_data_with_prediction()  # Using the function here
    if new_text:
        update_canvas_with_new_text(new_text)
    else:
        print("Error: new_text list is empty or incomplete.")
    
def start_preheating():

    canvas.create_image(
    646.0000000000001,
    474.0,
    image=image_image_1)

    canvas.delete(image_3)
    canvas.delete(image_2)

    canvas.create_text(
        755.0000000000001,
        464.0,
        anchor="nw",
        text="Preheating",
        fill="#FFFFFF",
        font=("AlfaSlabOne Regular", 15 * -1),
        tags=("text",)
    )

def update_canvas_with_new_text():
    canvas.delete("text")

    canvas.create_text(
        493.0000000000001,
        324.0,
        anchor="nw",
        text=str(new_text[0]),
        fill="#000000",
        font=("AlfaSlabOne Regular", 15 * -1),
        tags=("text",)
    )

    canvas.create_text(
        637.0000000000001,
        324.0,
        anchor="nw",
        text=str(new_text[1]),
        fill="#000000",
        font=("AlfaSlabOne Regular", 15 * -1),
        tags=("text",)
    )

    canvas.create_text(
        781.0000000000001,
        324.0,
        anchor="nw",
        text=str(new_text[2]),
        fill="#000000",
        font=("AlfaSlabOne Regular", 15 * -1),
        tags=("text",)
    )

    canvas.create_text(
        556.0000000000001,
        386.0,
        anchor="nw",
        text=str(new_text[3]),
        fill="#000000",
        font=("AlfaSlabOne Regular", 15 * -1),
        tags=("text",)
    )

    canvas.create_text(
        718.0000000000001,
        386.0,
        anchor="nw",
        text=str(new_text[4]),
        fill="#000000",
        font=("AlfaSlabOne Regular", 15 * -1),
        tags=("text",)
    )

    canvas.create_text(
        755.0000000000001,
        464.0,
        anchor="nw",
        text=str(new_text[5]),
        fill="#FFFFFF",
        font=("AlfaSlabOne Regular", 15 * -1),
        tags=("text",)
    )

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=start,
    relief="flat"
)
button_1.place(
    x=453.0000000000001,
    y=446.0,
    width=129.0,
    height=50.0
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    505.0000000000001,
    337.0,
    image=image_image_8)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    649.0000000000001,
    337.0,
    image=image_image_9)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    793.0000000000001,
    337.0,
    image=image_image_10)

window.resizable(False, False)
window.mainloop()

# main_copy.py

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
    sensor_data = read_sensor_values()
    loaded_model = load_saved_model('logistic_regression_model.pkl')
    prediction = predict_freshness(sensor_data, loaded_model)
    return prediction

def read_sensor_values():
    # Implement your sensor reading code here
    # This is a placeholder
    return [0, 0, 0, 0, 0]  # Replace this with actual sensor data
