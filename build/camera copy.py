import cv2

def capture_image(camera_index=1, image_path='test.jpg'):
    # Create a VideoCapture object to capture images from the camera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        return

    # Save the captured frame as an image
    cv2.imwrite(image_path, frame)
    print("Image saved as", image_path)

    # Release the VideoCapture object
    cap.release()

if __name__ == "__main__":
    # Set the camera index (0 for default camera, change if necessary)
    camera_index = 1

    # Set the path where the image will be saved
    image_path = 'test.jpg'

    # Capture an image from the specified camera and save it
    capture_image(camera_index, image_path)
