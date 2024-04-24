# gui.py

from pathlib import Path
import cv2
from PIL import Image, ImageTk
import main_copy
from tkinter import Tk, Canvas, Button, PhotoImage

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
    cap = cv2.VideoCapture(1)

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
    canvas.after(1000, read_data_and_update_canvas)

def start2():
    print("start2")
    canvas.delete("text")
    start_camera()
    start_preheating()
    canvas.after(1000, read_data_and_update_canvas2)

def read_data_and_update_canvas2():
    
    canvas.delete("text")
    canvas.delete(image_1)
    canvas.create_image(
        646.0000000000001,
        474.0,
        image=image_image_2
    )
    canvas.create_text(
        755.0000000000001,
        464.0,
        anchor="nw",
        text="Evaluating",
        fill="#FFFFFF",
        font=("AlfaSlabOne Regular", 15 * -1),
        tags=("text",)
    )
    
    # print("Sensor Data with Prediction:", main_copy.sensor_data_with_prediction)
    new_text = main_copy.get_sensor_data_with_prediction()
    print(new_text)
    if new_text:

        new_text = new_text[0]  # Extracting the array from the tuple
        new_text[0] , new_text[1] ,  new_text[2]  =  new_text[1] , new_text[2] , new_text[0] 
        # new_text[3] , new_text[4]  =  new_text[4] , new_text[3] 
        update_canvas_with_new_text(new_text)
        print(new_text = new_text[4])
    else:
        print("Error: new_text list is empty or incomplete.")
   
    

def read_data_and_update_canvas():
    
    canvas.delete("text")
    canvas.delete(image_1)
    canvas.create_image(
        646.0000000000001,
        474.0,
        image=image_image_2
    )
    canvas.create_text(
        755.0000000000001,
        464.0,
        anchor="nw",
        text="Evaluating",
        fill="#FFFFFF",
        font=("AlfaSlabOne Regular", 15 * -1),
        tags=("text",)
    )
    
    new_text = main_copy.get_sensor_data_with_prediction()
    print(new_text)
    if new_text:

        new_text = new_text[0]  # Extracting the array from the tuple

        update_canvas_with_new_text(new_text)
        print(new_text)
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

def update_canvas_with_new_text(new_text):
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
        text=str(new_text[3]),
        fill="#000000",
        font=("AlfaSlabOne Regular", 15 * -1),
        tags=("text",)
    )

    canvas.create_text(
        556.0000000000001,
        386.0,
        anchor="nw",
        text=str(int(new_text[4])),
        fill="#000000",
        font=("AlfaSlabOne Regular", 15 * -1),
        tags=("text",)
    )

    canvas.create_text(
        718.0000000000001,
        386.0,
        anchor="nw",
        text=str(new_text[2]),
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

def toggle_command():
    global command_toggle
    if command_toggle == "start":
        start()
        command_toggle = "start2"
    elif command_toggle == "start2":
        start2()
        command_toggle = "start2"

# Initialize the command_toggle variable
command_toggle = "start"

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=toggle_command,
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
