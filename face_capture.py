import cv2

cap = cv2.VideoCapture(0)  

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

image_captured = False

while not image_captured:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not capture a frame.")
        exit()

    cv2.imshow("Press 'a' to capture an image", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 97:  # 'a' key is pressed
        cv2.imwrite("captured_image.jpg", frame)

        image_captured = True
        print("Image captured and saved as 'captured_image.jpg'")

cap.release()

cv2.destroyAllWindows()
