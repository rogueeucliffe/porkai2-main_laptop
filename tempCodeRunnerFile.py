import cv2

def capture_video(camera_index=1):
    # Create a VideoCapture object to capture video from the camera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Display the frame
        cv2.imshow('Frame', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object
    cap.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Set the camera index (0 for default camera, change if necessary)
    camera_index = 1

    # Capture a video from the specified camera and display it
    capture_video(camera_index)
