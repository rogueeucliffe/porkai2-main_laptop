import cv2

def capture_image(camera_index=1, image_path='test.jpg'):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        return

    height, width, _ = frame.shape

    start_x = (width - 120) // 2
    start_y = (height - 120) // 2
    end_x = start_x + 120
    end_y = start_y + 120

    cropped_frame = frame[start_y:end_y, start_x:end_x]

    cv2.imwrite(image_path, cropped_frame)
    print("Cropped image saved as", image_path)

    cap.release()

if __name__ == "__main__":
    camera_index = 1
    image_path = 'test.jpg'
    capture_image(camera_index, image_path)